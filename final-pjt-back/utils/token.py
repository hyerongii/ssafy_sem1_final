# utils/token.py
import os
import requests
import json
from datetime import datetime, timedelta
from django.conf import settings
from dotenv import load_dotenv, set_key
import time

def get_access_token():
    """
    한국투자증권 API 접근 토큰을 관리하는 함수
    """
    # .env 파일 로드
    load_dotenv()
    
    # 현재 저장된 토큰과 만료시간 확인
    current_token = os.getenv('KIS_ACCESS_TOKEN')
    token_expires = os.getenv('KIS_TOKEN_EXPIRES')
    
    # 토큰 유효성 검사
    if current_token and token_expires:
        try:
            expires_datetime = datetime.strptime(token_expires, '%Y%m%d%H%M%S')
            if datetime.now() + timedelta(minutes=10) < expires_datetime:
                return current_token
        except ValueError:
            pass
    
    # 새로운 토큰 발급 요청
    url = f"{settings.KIS_BASE_URL}/oauth2/tokenP"
    
    headers = {
        "content-type": "application/json"
    }
    
    data = {
        "grant_type": "client_credentials",
        "appkey": settings.KIS_APP_KEY,
        "appsecret": settings.KIS_APP_SECRET
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # HTTP 에러 체크
        
        # 응답 내용 출력하여 디버깅
        # print("API Response:", response.text)
        
        token_data = response.json()
        
        # API 응답 구조 확인
        if 'access_token' not in token_data:
            raise Exception(f"유효하지 않은 응답 형식: {token_data}")
            
        access_token = token_data['access_token']
        # expires_in = token_data.get('expires_in', '')  # expires_in 키 이름 수정
        
        # .env 파일 업데이트
        env_path = os.path.join(settings.BASE_DIR, '.env')
        
        set_key(env_path, 'KIS_ACCESS_TOKEN', access_token)
        # set_key(env_path, 'KIS_TOKEN_EXPIRES', expires_in)
        
        # 환경 변수 즉시 업데이트
        os.environ['KIS_ACCESS_TOKEN'] = access_token
        # os.environ['KIS_TOKEN_EXPIRES'] = expires_in
        
        return access_token
        
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {str(e)}")  # 디버깅을 위한 출력
        raise Exception(f"토큰 발급 요청 실패: {str(e)}")
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {str(e)}")  # 디버깅을 위한 출력
        raise Exception(f"응답 데이터 파싱 실패: {str(e)}")
    except Exception as e:
        print(f"General Error: {str(e)}")  # 디버깅을 위한 출력
        raise Exception(f"토큰 발급 중 오류 발생: {str(e)}")
    

def get_access_to_websocket():
    url = 'https://openapi.koreainvestment.com:9443'
    headers = {"content-type": "application/json"}
    body = {"grant_type": "client_credentials",
            "appkey": settings.KIS_APP_KEY,
            "secretkey": settings.KIS_APP_SECRET}
    PATH = "oauth2/Approval"
    URL = f"{url}/{PATH}"
    time.sleep(0.05)
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    approval_key = res.json()["approval_key"]
    return approval_key