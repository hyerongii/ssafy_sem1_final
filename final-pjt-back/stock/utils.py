import requests
from django.conf import settings
from .models import Theme, IndustryCode

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
        print(industry_codes)
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
    # # 종목 코드의 길이에 따라 거래소 결정
    # if len(stock_code) <= 3 or stock_code == 'RBRX'  or stock_code == 'SPOT' or stock_code == 'HST':
    #     excd = "NYS"  # 뉴욕증권거래소
    # elif len(stock_code) >= 4 or stock_code == 'EA':
    #     excd = "NAS"  # 나스닥
    # else:
    #     excd = "AMS"  # 아멕스 (현재는 NYSE American)

    params = {
        "AUTH": "",
        "EXCD": stock_excd,  # 동적으로 설정된 거래소 코드
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