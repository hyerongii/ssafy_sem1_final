import requests
from django.conf import settings
from .models import Theme, IndustryCode
from datetime import datetime, timedelta

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
            # print(data)
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

def get_domestic_stock_chartdata_day(access_token, stock_code, current_time):
    base_url = settings.KIS_BASE_URL
    path = "/uapi/domestic-stock/v1/quotations/inquire-time-itemconclusion"
    url = f"{base_url}{path}"

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "authorization": f"Bearer {access_token}",  
        "appkey": settings.KIS_APP_KEY,
        "appsecret": settings.KIS_APP_SECRET,
        "tr_id": "FHPST01060000"
    }

    # 5분 단위로 반올림
    current = datetime.strptime(current_time, "%H%M%S")
    current = current.replace(minute=(current.minute // 5) * 5, second=0, microsecond=0)
    
    start_time = datetime.strptime("090000", "%H%M%S")
    chart_data = []
    
    while current >= start_time:
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": stock_code,
            "FID_INPUT_HOUR_1": current.strftime("%H%M%S"),
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            if data['rt_cd'] == '0' and data['output2']:
                # 현재 시간대에서 가장 가까운 데이터 선택
                closest_data = min(
                    [item for item in data['output2'] 
                     if datetime.strptime(item['stck_cntg_hour'], "%H%M%S") >= start_time],
                    key=lambda item: abs(datetime.strptime(item['stck_cntg_hour'], "%H%M%S") - current),
                    default=None
                )

                if closest_data:
                    chart_data.append({
                        'time': closest_data['stck_cntg_hour'],
                        'price': float(closest_data['stck_prpr'])
                    })

        except Exception as e:
            print(f"Error at {current}: {str(e)}")
        
        current -= timedelta(minutes=5)

    return sorted(chart_data, key=lambda x: x['time'])

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
    default = period_settings.get(period, period_settings['D'])
    
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
        "NMIN": "5",
        # 시차가 있음...이건 추후 더 분석이 필요하다 
        "PINC": "1",
        "NREC": "120", # 5,0,120 함으로써 한국시간 기준 장 시작부터 마감까지의 정보를 받아올 수 있음
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
                    'date': item['khms'],
                    'clpr': item['last']
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
                    'date': item['khms'],
                    'clpr': float(item['last'])
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
            for item in data['output']:
                ratio_data.append({
                    'PER': item['perx'],
                    'PBR': item['pbrx'],
                    'EPS': item['epsx'],
                    'BPS': item['bpsx']
                })
            return ratio_data
        else:
            raise Exception(f"API Error: {data['msg1']}")
            
    except Exception as e:
        print(f"Error getting price for stock {stock_code}: {str(e)}")
        return []
