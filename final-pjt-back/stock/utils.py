import requests
from django.conf import settings
from .models import Theme, IndustryCode, Article, Stock
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone
import random
from stock.models import UserInterest, UserProfile, Interest

def get_industry_price_series(access_token, industry_code, start_date, end_date):
    """
    한국투자증권 API를 통해 업종별 종가 시계열 데이터를 가져오는 함수
    
    Args:
        industry_code (str): 업종코드 (00021: 금융업)
        start_date (str): 조회 시작일자 (YYYYMMDD)
        end_date (str): 조회 종료일자 (YYYYMMDD)
    
    Returns:
        dict: 상태 및 시계열 데이터를 포함한 JSON
        형태의 응답
    """
    
    base_url = settings.KIS_BASE_URL
    path = "/uapi/domestic-stock/v1/quotations/inquire-daily-indexchartprice"
    url = f"{base_url}{path}"

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "authorization": f"Bearer {access_token}",
        "appkey": settings.KIS_APP_KEY,
        "appsecret": settings.KIS_APP_SECRET,
        "tr_id": "FHKUP03500100"
    }

    params = {
        "FID_COND_MRKT_DIV_CODE": "U",
        "FID_INPUT_ISCD": industry_code,
        "FID_INPUT_DATE_1": start_date,
        "FID_INPUT_DATE_2": end_date,
        "FID_PERIOD_DIV_CODE": "D"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data['rt_cd'] == '0':
            price_data = []
            
            for item in data['output2']:
                price_data.append({
                    'date': item['stck_bsop_date'],
                    'close': float(item['bstp_nmix_prpr']),
                })
            
            # 날짜순으로 정렬
            price_data.sort(key=lambda x: x['date'])
            
            return {
                'status': 'success',
                'data': price_data
            }
            
        else:
            raise Exception(f"API Error: {data['msg1']}") 
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request Failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")



def get_theme_price_series(access_token, theme_name, start_date, end_date):
    try:
        # theme.pk == industrycode의 interest_id 만족하는 모든 api_request_code를 리스트에 담기
        theme = Theme.objects.get(name=theme_name)
        industry_codes = IndustryCode.objects.filter(
            interest_id=theme.pk
        ).values_list('api_request_code', flat=True)
        combined_data = {}
        
        # 각 업종별 데이터 수집
        for code in industry_codes:
            data = get_industry_price_series(access_token, code, start_date, end_date)
            # 각 날짜별 데이터 통합
            for item in data['data']:
                date = item['date']
                if date not in combined_data:
                    combined_data[date] = {'prices': [], 'changes': []}
                combined_data[date]['prices'].append(item['close'])
        
        # 평균 계산 및 결과 구성
        result_data = []
        for date, values in combined_data.items():
            avg_price = sum(values['prices']) / len(values['prices'])
            result_data.append({
                'date': date,
                'average_close': avg_price,
            })
        
        # 날짜순 정렬
        result_data.sort(key=lambda x: x['date'])
        
        # 등락률 계산
        for i in range(1, len(result_data)):
            prev_price = result_data[i-1]['average_close']
            curr_price = result_data[i]['average_close']
            change_rate = ((curr_price - prev_price) / prev_price) * 100
            result_data[i]['change_rate'] = change_rate
        
        return {
            'status': 'success',
            'data': result_data
        }
            
    except Theme.DoesNotExist:
        raise Exception(f"Theme '{theme_name}' not found")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")
    

def get_current_stock_price(access_token, stock_code):
    """
    한국투자증권 API를 통해 주식의 현재가를 조회하는 함수
    """
    base_url = settings.KIS_BASE_URL
    path = "/uapi/domestic-stock/v1/quotations/inquire-price"
    url = f"{base_url}{path}"

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "authorization": f"Bearer {access_token}",
        "appkey": settings.KIS_APP_KEY,
        "appsecret": settings.KIS_APP_SECRET,
        "tr_id": "FHKST01010100"
    }

    params = {
        "FID_COND_MRKT_DIV_CODE": "J",
        "FID_INPUT_ISCD": stock_code,
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['rt_cd'] == '0':
            return float(data['output']['stck_prpr'])  # 현재가 반환
        else:
            raise Exception(f"API Error: {data['msg1']}")
            
    except Exception as e:
        print(f"Error getting price for stock {stock_code}: {str(e)}")
        return 0  # 에러 발생 시 0 반환
    
def get_current_us_stock_price(access_token, stock_code, stock_excd):
    """
    한국투자증권 API를 통해 미국 주식의 현재가를 조회하는 함수
    Args:
        access_token (str): 접근 토큰
        stock_code (str): 종목 코드
    Returns:
        float: 현재가 (에러 발생 시 0 반환)
    """
    base_url = settings.KIS_BASE_URL
    path = "/uapi/overseas-price/v1/quotations/price"
    url = f"{base_url}{path}"

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "authorization": f"Bearer {access_token}",
        "appkey": settings.KIS_APP_KEY,
        "appsecret": settings.KIS_APP_SECRET,
        "tr_id": "HHDFS00000300"
    }

    params = {
        "AUTH": "",
        "EXCD": stock_excd,
        "SYMB": stock_code,
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['rt_cd'] == '0' and 'output' in data and 'last' in data['output']:
            last_price = data['output']['last']
            if last_price and last_price.strip():
                return float(last_price)
            else:
                raise Exception(f"Invalid price data for stock {stock_code}: {last_price}")
        else:
            raise Exception(f"API Error: {data.get('msg1', 'Unknown error')}")
            
    except Exception as e:
        print(f"Error getting price for US stock {stock_code}: {str(e)}")
        return 0

# 09시부터 현재 시간까지의 모든 차트 데이터를 받아오는 함수 / 현재 사용 X
# def get_domestic_stock_chartdata_day(access_token, stock_code, current_time):
#     base_url = settings.KIS_BASE_URL
#     path = "/uapi/domestic-stock/v1/quotations/inquire-time-itemconclusion"
#     url = f"{base_url}{path}"

#     headers = {
#         "Content-Type": "application/json; charset=utf-8",
#         "authorization": f"Bearer {access_token}",  
#         "appkey": settings.KIS_APP_KEY,
#         "appsecret": settings.KIS_APP_SECRET,
#         "tr_id": "FHPST01060000"
#     }

#     # 현재 시간을 10분 단위로 반올림
#     current = datetime.strptime(current_time, "%H%M%S")
#     current = current.replace(minute=(current.minute // 10) * 10, second=0, microsecond=0)
    
#     # 장 시작 시간을 09:00:00으로 설정
#     start_time = datetime.strptime("090000", "%H%M%S")
#     end_time = datetime.strptime("160000", "%H%M%S")
    
#     if current > end_time:
#         current = end_time  

#     # 10분 간격으로 모든 시간대 생성
#     time_slots = []
#     temp_time = start_time
#     while temp_time <= current:
#         time_slots.append(temp_time.strftime("%H%M%S"))
#         temp_time += timedelta(minutes=10)
    
#     chart_data = []
    
#     # 10분 단위로 API 호출 (API 한 번 호출로 30개 데이터를 더 조밀하게 수신)
#     for i in range(len(time_slots)):
#         query_time = datetime.strptime(time_slots[i], "%H%M%S")
        
#         params = {
#             "FID_COND_MRKT_DIV_CODE": "J",
#             "FID_INPUT_ISCD": stock_code,
#             "FID_INPUT_HOUR_1": query_time.strftime("%H%M%S"),
#         }
        
#         try:
#             response = requests.get(url, headers=headers, params=params)
#             data = response.json()
            
#             if data['rt_cd'] == '0' and data['output2']:
#                 target_time = datetime.strptime(time_slots[i], "%H%M%S")
#                 # 해당 시간대와 가장 가까운 데이터 찾기
#                 closest_data = min(
#                     [item for item in data['output2'] 
#                      if datetime.strptime(item['stck_cntg_hour'], "%H%M%S") <= target_time],
#                     key=lambda x: abs(datetime.strptime(x['stck_cntg_hour'], "%H%M%S") - target_time),
#                     default=None
#                 )
                
#                 if closest_data:
#                     chart_data.append({
#                         'time': time_slots[i],
#                         'price': float(closest_data['stck_prpr'])
#                     })

#         except Exception as e:
#             print(f"Error at {query_time}: {str(e)}")

#     return sorted(chart_data, key=lambda x: x['time'])

# def get_d_stock_chart_data_day_for_realtime(access_token, stock_code, current_time):
#     base_url = settings.KIS_BASE_URL
#     path = "/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice"
#     url = f"{base_url}{path}"

#     headers = {
#         "Content-Type": "application/json; charset=utf-8",
#         "authorization": f"Bearer {access_token}",
#         "appkey": settings.KIS_APP_KEY,
#         "appsecret": settings.KIS_APP_SECRET,
#         "tr_id": "FHKST03010200"
#     }

#     # current_time이 153000(장이 마감되는 시간)을 초과하면 153000으로 설정
#     if int(current_time) > 153000:
#         current_time = "153000"
#     print(current_time)

#     # 주말일 경우 금요일 날짜로 설정
#     today = datetime.now()
#     if today.weekday() >= 5:  # 토요일(5) 또는 일요일(6)
#         days_to_friday = today.weekday() - 4
#         friday_date = today - timedelta(days=days_to_friday)
#         current_date = friday_date.strftime("%Y%m%d")
#     else:
#         current_date = today.strftime("%Y%m%d")

#     # current_time에서 1시간 전 시간 계산 (HHMMSS 형식)
#     time_format = "%H%M%S"
#     start_time = '090000'
#     current_datetime = datetime.strptime(current_time, time_format)
#     one_hour_ago = (current_datetime - timedelta(minutes=30)).strftime(time_format)

#     if int(one_hour_ago) < 90000:
#         one_hour_ago = start_time
#         print(type(one_hour_ago))

#     params = {
#         "FID_ETC_CLS_CODE": "",
#         "FID_COND_MRKT_DIV_CODE": "J",
#         "FID_INPUT_ISCD": stock_code,
#         "FID_INPUT_HOUR_1": current_time,
#         "FID_PW_DATA_INCU_YN": "N",
#     }

#     chart_data = []
#     try:
#         response = requests.get(url, headers=headers, params=params)
#         response.raise_for_status()
#         data = response.json()

#         if data['rt_cd'] == '0':  # Successful response
#             for item in data['output2']:
#                 time_value = item['stck_cntg_hour']

#                 # Stop if data is outside the requested range
#                 if time_value < one_hour_ago:
#                     break

#                 chart_data.append({
#                     'time': time_value,
#                     'price': float(item['stck_prpr'])
#                 })


#         else:  # Handle API error
#             raise Exception(f"API Error: {data['msg1']}")
#         print(chart_data)
#         return chart_data

#     except Exception as e:
#         print(f"Error getting price for stock {stock_code}: {str(e)}")
#         return []

def get_d_stock_chart_data_day_for_realtime(access_token, stock_code, current_time):
    base_url = settings.KIS_BASE_URL
    path = "/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice"
    url = f"{base_url}{path}"

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "authorization": f"Bearer {access_token}",
        "appkey": settings.KIS_APP_KEY,
        "appsecret": settings.KIS_APP_SECRET,
        "tr_id": "FHKST03010200"
    }

    # current_time이 153000(장이 마감되는 시간)을 초과하면 153000으로 설정
    if int(current_time) > 153000:
        current_time = "153000"

    # 주말일 경우 금요일 날짜로 설정
    today = datetime.now()
    if today.weekday() >= 5:  # 토요일(5) 또는 일요일(6)
        days_to_friday = today.weekday() - 4
        friday_date = today - timedelta(days=days_to_friday)
        current_date = friday_date.strftime("%Y%m%d")
    else:
        current_date = today.strftime("%Y%m%d")

    # 주식 시장의 시작 시간
    start_time = '090000'
    
    # chart_data 초기화
    chart_data = []

    # 반복적으로 데이터를 요청하며 chart_data에 추가
    while int(current_time) >= int(start_time):
        params = {
            "FID_ETC_CLS_CODE": "",
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": stock_code,
            "FID_INPUT_HOUR_1": current_time,
            "FID_PW_DATA_INCU_YN": "N",
        }
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            if data['rt_cd'] == '0':  
                for item in data['output2']:
                    time_value = item['stck_cntg_hour']
                    price_value = float(item['stck_prpr'])
                    
                    # 중복 데이터 방지: 이미 저장된 시간은 추가하지 않음
                    if not any(d['time'] == time_value for d in chart_data):
                        chart_data.append({
                            'time': time_value,
                            'price': price_value
                        })
            else:  # Handle API error
                raise Exception(f"API Error: {data['msg1']}")
        except Exception as e:
            print(f"Error getting price for stock {stock_code}: {str(e)}")
            return []

        # 30분 전으로 시간 감소
        current_datetime = datetime.strptime(current_time, "%H%M%S") - timedelta(minutes=30)
        current_time = current_datetime.strftime('%H%M%S')

        # 장 시작 시간 이전으로 가면 종료
        if int(current_time) < int(start_time):
            break

    return chart_data


# def get_d_stock_chart_data_day(access_token, stock_code, current_time):
#     base_url = settings.KIS_BASE_URL
#     path = "/uapi/domestic-stock/v1/quotations/inquire-time-dailychartprice"
#     url = f"{base_url}{path}"

#     headers = {
#         "Content-Type": "application/json; charset=utf-8",
#         "authorization": f"Bearer {access_token}",  
#         "appkey": settings.KIS_APP_KEY,
#         "appsecret": settings.KIS_APP_SECRET,
#         "tr_id": "FHKST03010230"
#     }

#     # 현재 날짜와 시간 계산
#     today = datetime.now()
#     weekday = today.weekday()  # 월=0, 화=1, ..., 토=5, 일=6

#     # 토요일 또는 일요일인 경우 금요일 날짜 계산
#     if weekday == 5:  # 토요일
#         target_date = today - timedelta(days=1)
#     elif weekday == 6:  # 일요일
#         target_date = today - timedelta(days=2)
#     else:
#         target_date = today

#     # 금요일 데이터 요청 시 시간 범위 설정 (09:00 ~ 15:30)
#     if weekday in [5, 6]:  # 토요일 또는 일요일
#         start_time = "0900"
#         end_time = "1530"
#         date_str = target_date.strftime("%Y%m%d")
#     else:
#         # 평일 데이터 요청 시 09:00 ~ 15:30
#         start_time = current_time
#         end_time = "1530"
#         date_str = today.strftime("%Y%m%d")

#     params = {
#         "FID_COND_MRKT_DIV_CODE": "J",
#         "FID_INPUT_ISCD": stock_code,
#         "FID_INPUT_DATE_1": date_str,
#         "FID_INPUT_HOUR_1": start_time,
#         "FID_PW_DATA_INCU_YN": "N",
#         "FID_FAKE_TICK_INCU_YN": "N",
#     }

#     chart_data = []
#     try:
#         response = requests.get(url, headers=headers, params=params)
#         response.raise_for_status()
#         data = response.json()

#         if data['rt_cd'] == '0':
#             for item in data['output2']:
#                 time_value = item['stck_cntg_hour']
#                 if start_time <= time_value <= end_time:
#                     chart_data.append({
#                         'time': time_value,
#                         'price': float(item['stck_prpr'])
#                     })
#             return chart_data
#         else:
#             raise Exception(f"API Error: {data['msg1']}")
            
#     except Exception as e:
#         print(f"Error getting price for stock {stock_code}: {str(e)}")
#         return []

def d_get_stock_day_fluctuation_rate(access_token, stock_code):
    base_url = settings.KIS_BASE_URL
    path = "/uapi/domestic-stock/v1/quotations/inquire-daily-price"
    url = f"{base_url}{path}"

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "authorization": f"Bearer {access_token}",  
        "appkey": settings.KIS_APP_KEY,
        "appsecret": settings.KIS_APP_SECRET,
        "tr_id": "FHKST01010400"
    }
    params = {
        "FID_COND_MRKT_DIV_CODE": "J",
        "FID_INPUT_ISCD": stock_code,
        "FID_PERIOD_DIV_CODE": "D",
        "FID_ORG_ADJ_PRC": "1",
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['rt_cd'] == '0':
            for item in data['output']:
                return item['prdy_ctrt']
        else:
            raise Exception(f"API Error: {data['msg1']}")
            
    except Exception as e:
        print(f"Error getting price for stock {stock_code}: {str(e)}")
        return []
    
def o_get_stock_day_fluctuation_rate(access_token, stock_code, stock_excd):
    base_url = settings.KIS_BASE_URL
    path = "/uapi/overseas-price/v1/quotations/price"
    url = f"{base_url}{path}"

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "authorization": f"Bearer {access_token}",
        "appkey": settings.KIS_APP_KEY,
        "appsecret": settings.KIS_APP_SECRET,
        "tr_id": "HHDFS00000300"
    }

    params = {
        "AUTH": "",
        "EXCD": stock_excd,
        "SYMB": stock_code,
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['rt_cd'] == '0' and 'output' in data and 'last' in data['output']:
            rate = data['output']['rate']
            return rate
        else:
            raise Exception(f"API Error: {data.get('msg1', 'Unknown error')}")
            
    except Exception as e:
        print(f"Error getting price for US stock {stock_code}: {str(e)}")
        return 0



def get_domestic_stock_chartdata_period(access_token, stock_code, period):
    base_url = settings.KIS_BASE_URL
    path = "/uapi/domestic-stock/v1/quotations/inquire-daily-price"
    url = f"{base_url}{path}"

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "authorization": f"Bearer {access_token}",  
        "appkey": settings.KIS_APP_KEY,
        "appsecret": settings.KIS_APP_SECRET,
        "tr_id": "FHKST01010400"
    }
    
    # period에 따른 설정값 결정
    period_settings = {
        'W': {'div_code': 'D', 'data_count': 5},    # 일별 데이터 5개 (1주)
        '1M': {'div_code': 'D', 'data_count': 20},  # 일별 데이터 20개 (1달)
        '6M': {'div_code': 'W', 'data_count': 24},  # 주별 데이터 24개 (6달)
        '1Y': {'div_code': 'M', 'data_count': 12}   # 월별 데이터 12개 (1년)
    }
    
    # 기본값 설정 (잘못된 period가 들어왔을 경우 주간 데이터 사용)
    default = period_settings.get(period, period_settings['W'])
    
    params = {
        "FID_COND_MRKT_DIV_CODE": "J",
        "FID_INPUT_ISCD": stock_code,
        "FID_PERIOD_DIV_CODE": default['div_code'],
        "FID_ORG_ADJ_PRC": "1",
    }
    
    chart_data = []
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['rt_cd'] == '0':
            # period에 따른 데이터 개수만큼 슬라이싱
            for item in data['output'][:default['data_count']]:
                chart_data.append({
                    'date': item['stck_bsop_date'],
                    'clpr': float(item['stck_clpr'])
                })
            return chart_data
        else:
            raise Exception(f"API Error: {data['msg1']}")
            
    except Exception as e:
        print(f"Error getting price for stock {stock_code}: {str(e)}")
        return []

# https://apiportal.koreainvestment.com/apiservice/apiservice-oversea-stock-quotations#L_852d7e45-4f34-418b-b6a1-a4552bbcdf90
def get_oversea_stock_chartdata_day(access_token,stock_code,excd):
    base_url = settings.KIS_BASE_URL
    path = "/uapi/overseas-price/v1/quotations/inquire-time-itemchartprice"
    url = f"{base_url}{path}"

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "authorization": f"Bearer {access_token}",
        "appkey": settings.KIS_APP_KEY,
        "appsecret": settings.KIS_APP_SECRET,
        "tr_id": "HHDFS76950200"
    }
    params = {
        "AUTH": "",
        "EXCD": excd,
        "SYMB": stock_code,
        "NMIN": "10",
        # 전일 포함 여부
        "PINC": "0",
        # 레코드 요청 개수
        "NREC": "120", 
        "NEXT":"",
        "NREC":"",
        "FILL":"",
        "KEYB":""
    }
    chart_data = []
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if data['rt_cd'] == '0':
            
            for item in data['output2']:
                chart_data.append({
                    'time': item['xhms'],
                    'price': item['last']
                })
            return chart_data
        else:
            raise Exception(f"API Error: {data['msg1']}")
        
    except Exception as e:
        print(f"Error getting price for stock {stock_code}: {str(e)}")
        return []  # 에러 발생 시 0 반환
    
def get_oversea_stock_chartdata_period(access_token, stock_code, period):
    base_url = settings.KIS_BASE_URL
    path = "/uapi/overseas-price/v1/quotations/inquire-daily-chartprice"
    url = f"{base_url}{path}"

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "authorization": f"Bearer {access_token}",
        "appkey": settings.KIS_APP_KEY,
        "appsecret": settings.KIS_APP_SECRET,
        "tr_id": "FHKST03030100"
    }

    current_date = datetime.today()
    # period에 따라 start_date 계산
    if period == 'W':
        start_date = current_date - timedelta(days=5)
    elif period == '1M':
        start_date = current_date - timedelta(days=20) 
    elif period == '6M':
        start_date = current_date - timedelta(days=120)
    elif period == '1Y':
        start_date = current_date - timedelta(days=240)
    else:
        start_date = current_date
    
    # 날짜 형식 변환 (YYYYmmdd)
    current_date = current_date.strftime("%Y%m%d")
    start_date = start_date.strftime("%Y%m%d")

    params = {
        "FID_COND_MRKT_DIV_CODE": "N",
        "FID_INPUT_ISCD": stock_code,
        "FID_INPUT_DATE_1": start_date,
        "FID_INPUT_DATE_2": current_date, 
        "FID_PERIOD_DIV_CODE": "0",
    }
    chart_data = []
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['rt_cd'] == '0':
            for item in data['output2']:
                chart_data.append({
                    # 혜령 : 미국주식 차트 불러올 시 date, khms 여기서 에러 발생하는중
                    'date': item['stck_bsop_date'],
                    'clpr': float(item['ovrs_nmix_prpr'])
                })
            return chart_data
        else:
            raise Exception(f"API Error: {data['msg1']}")
        
    except Exception as e:
        print(f"Error getting price for stock {stock_code}: {str(e)}")
        return 0  # 에러 발생 시 0 반환
    

def get_domestic_stock_main_info(access_token, stock_code):
    base_url = settings.KIS_BASE_URL
    path = "/uapi/domestic-stock/v1/finance/profit-ratio"
    url = f"{base_url}{path}"

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "authorization": f"Bearer {access_token}",
        "appkey": settings.KIS_APP_KEY,
        "appsecret": settings.KIS_APP_SECRET,
        "tr_id": "FHKST66430400"
    }

    params = {
        "FID_COND_MRKT_DIV_CODE": "J",
        "FID_INPUT_ISCD": stock_code,
        "fid_div_cls_code": "1",
    }
    ratio_data = []
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if data['rt_cd'] == '0':
            for item in data['output']:
                ratio_data.append({
                    'ROI':item['cptl_ntin_rate'],
                    'ROE':item['self_cptl_ntin_inrt'],
                    'ROS':item['sale_ntin_rate']
                })
                break # 가장 최신 결산 이후의 정보만 받아옴
            return ratio_data
        else:
            raise Exception(f"API Error: {data['msg1']}")
            
    except Exception as e:
        print(f"Error getting price for stock {stock_code}: {str(e)}")
        return 0  # 에러 발생 시 0 반환
    

def get_domestic_stock_consensus(access_token, stock_code):
    base_url = settings.KIS_BASE_URL
    path = "/uapi/domestic-stock/v1/quotations/invest-opinion"
    url = f"{base_url}{path}"

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "authorization": f"Bearer {access_token}",
        "appkey": settings.KIS_APP_KEY,
        "appsecret": settings.KIS_APP_SECRET,
        "tr_id": "FHKST663300C0"
    }
    current_date = datetime.today().strftime("%Y%m%d") 
    params = {
        "FID_COND_MRKT_DIV_CODE": "J",
        "FID_INPUT_ISCD": stock_code,
        "FID_COND_SCR_DIV_CODE": "16633",
        "FID_DIV_CLS_CODE": "0",
        "FID_INPUT_DATE_1": "20240101",
        "FID_INPUT_DATE_2": current_date,
        "fid_div_cls_code": "1",
    }
    consensus_data = []
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if data['rt_cd'] == '0':
            for item in data['output']:
                consensus_data.append({
                    'concensus': item["invt_opnn"],
                    'source': item["mbcr_name"]
                })
                
            return consensus_data
        else:
            raise Exception(f"API Error: {data['msg1']}")
            
    except Exception as e:
        print(f"Error getting price for stock {stock_code}: {str(e)}")
        return 0  # 에러 발생 시 0 반환
    


def get_oversea_stock_main_info(access_token, stock_code, excd):
    base_url = settings.KIS_BASE_URL
    path = "/uapi/overseas-price/v1/quotations/price-detail"
    url = f"{base_url}{path}"

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "authorization": f"Bearer {access_token}",
        "appkey": settings.KIS_APP_KEY,
        "appsecret": settings.KIS_APP_SECRET,
        "tr_id": "HHDFS76200200"
    }

    params = {
        "AUTH": "",
        "EXCD": excd,
        "SYMB": stock_code,
    }

    ratio_data = []
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if data['rt_cd'] == '0':
            ratio_data.append({
                'PER': data['output']['perx'],
                'PBR': data['output']['pbrx'],
                'EPS': data['output']['epsx'],
                'BPS': data['output']['bpsx']
            })
            return ratio_data
        else:
            raise Exception(f"API Error: {data['msg1']}")
            
    except Exception as e:
        print(f"Error getting price for stock {stock_code}: {str(e)}")
        return []

def create_dummy_data():
    User = get_user_model()
    mbti_types = ['ISTJ', 'ISFJ', 'INFJ', 'INTJ', 'ISTP', 'ISFP', 'INFP', 'INTP',
                  'ESTP', 'ESFP', 'ENFP', 'ENTP', 'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ']
    period_choices = ['SHORT', 'MEDIUM', 'LONG']  # ENUM 필드의 선택지에 맞게 수정
    
    # 300명의 더미 유저 생성
    for i in range(2, 300):  # 1번 유저는 이미 존재하므로 2부터 시작
        username = f'test_user_{i}'
        email = f'test{i}@example.com'
        
        # User 생성
        user = User.objects.create_user(
            username=username,
            email=email,
            password='password123',
            nickname=f'닉네임{i}',
            date_joined=timezone.now()
        )
        
        # UserProfile 생성
        UserProfile.objects.create(
            user=user,
            mbti=random.choice(mbti_types),
            period=random.choice(period_choices),
            token='dummy_token'
        )

def create_user_interests():
    User = get_user_model()
    users = User.objects.all()
    interests = Interest.objects.all()
    
    # 각 유저당 3~5개의 관심사 랜덤 할당
    for user in users:
        interest_count = random.randint(3, 5)
        selected_interests = random.sample(list(interests), interest_count)
        
        for interest in selected_interests:
            UserInterest.objects.create(
                user=user,
                interest=interest
            )

# 각각의 주식의 정보를 업데이트
def get_stocks_info(access_token,stock_code,excd):
    # 국내 주식의 경우
    if stock_code.isdecimal():
        base_url = settings.KIS_BASE_URL
        path = "/uapi/domestic-stock/v1/quotations/inquire-price"
        url = f"{base_url}{path}"

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "authorization": f"Bearer {access_token}",
            "appkey": settings.KIS_APP_KEY,
            "appsecret": settings.KIS_APP_SECRET,
            "tr_id": "FHKST01010100"
        }

        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": stock_code,
        }

        result_data = []
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            if data['rt_cd'] == '0':
                result_data.append({
                    'PER': data['output']['per'],
                    'PBR': data['output']['pbr'],
                    'EPS': data['output']['eps'],
                    'BPS': data['output']['bps'],
                })
                return result_data
            else:
                raise Exception(f"API Error: {data['msg1']}")
            
        except Exception as e:
            print(f"Error getting price for stock {stock_code}: {str(e)}")
            return 0  # 에러 발생 시 0 반환
    else:

        base_url = settings.KIS_BASE_URL
        path = "/uapi/overseas-price/v1/quotations/price-detail"
        url = f"{base_url}{path}"

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "authorization": f"Bearer {access_token}",
            "appkey": settings.KIS_APP_KEY,
            "appsecret": settings.KIS_APP_SECRET,
            "tr_id": "HHDFS76200200"
        }

        params = {
            "AUTH": "",
            "EXCD": excd,
            "SYMB": stock_code,
        }

        result_data = []
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            if data['rt_cd'] == '0':
                
                result_data.append({
                    'PER': data['output']['perx'],
                    'PBR': data['output']['pbrx'],
                    'EPS': data['output']['epsx'],
                    'BPS': data['output']['bpsx']
                })
                return result_data
            else:
                raise Exception(f"API Error: {data['msg1']}")
                
        except Exception as e:
            print(f"Error getting price for stock {stock_code}: {str(e)}")
            return []