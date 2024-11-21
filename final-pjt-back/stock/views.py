from django.shortcuts import render
from rest_framework.response import Response
from .serializers import ThemeSerializer
from .utils import get_theme_price_series, get_current_stock_price, get_current_us_stock_price, get_domestic_stock_chartdata_day, get_domestic_stock_chartdata_period, get_oversea_stock_chartdata_day, get_oversea_stock_chartdata_period, get_domestic_stock_main_info, get_domestic_stock_consensus, get_oversea_stock_main_info
from utils.token import get_access_token,get_access_to_websocket  # 프로젝트 레벨의 token 유틸리티 import
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.
# 혜령 디버깅 추가
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import UserProfile, UserInterest, Interest, Theme, Stock
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta


# CSRF 보호 비활성화
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
# 3가지 입력값 분석해서 6가지 테마 추천
def analyze(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user
            
            # UserProfile 처리
            try:
                user_profile = UserProfile.objects.get(user=user)
                user_profile.mbti = data.get('mbti')
                user_profile.period = data.get('period')
                user_profile.token = get_access_token()
                
                user_profile.save()
            except UserProfile.DoesNotExist:
                user_profile = UserProfile.objects.create(
                    user=user,
                    mbti=data.get('mbti'),
                    period=data.get('period'),
                    token=get_access_token()
                )

            # Interest 처리
            interest_names = data.get('interest', [])
            UserInterest.objects.filter(user=user).delete()
            themes_info = []

            for interest_name in interest_names:
                try:
                    interest = Interest.objects.get(name=interest_name)
                    UserInterest.objects.create(
                        user=user,
                        interest=interest
                    )

                    theme = Theme.objects.get(name=interest_name)
                    stocks = theme.stock_set.all()
                    updated_stocks = []

                    for stock in stocks:
                        try:
                            if stock.code.isdecimal():
                                current_price = get_current_stock_price(user_profile.token, stock.code)
                            else:
                                current_price = get_current_us_stock_price(user_profile.token, stock.code, stock.excd)
                                if current_price > 0:
                                    current_price = current_price * 1391.50
                                else:
                                    current_price = 0

                            # 가격이 변경되었을 때만 저장
                            if current_price > 0 and stock.price != current_price:  
                                stock.price = current_price
                                stock.save()

                            updated_stocks.append({
                                "name": stock.name,
                                "code": stock.code,
                                "price": current_price
                            })
                        except Exception as e:
                            print(f"종목 {stock.code}의 가격 조회 실패: {e}")
                            continue

                    theme_info = {
                        "theme_name": theme.name,
                        "stocks": updated_stocks,
                        "description": theme.description,
                    }
                    themes_info.append(theme_info)

                except Interest.DoesNotExist:
                    continue

            # themes_info 길이 조정
            if len(themes_info) < 6:
                current_themes = [theme["theme_name"] for theme in themes_info]
                needed = 6 - len(themes_info)
                
                additional_themes = Theme.objects.exclude(
                    name__in=current_themes
                ).prefetch_related('stock_set')[:needed]

                for theme in additional_themes:
                    stocks = theme.stock_set.all()
                    updated_stocks = []

                    for stock in stocks:
                        try:
                            if stock.code.isdecimal():
                                current_price = get_current_stock_price(user_profile.token, stock.code)
                            else:
                                current_price = get_current_us_stock_price(user_profile.token, stock.code, stock.excd)
                                if current_price > 0:
                                    current_price = current_price * 1391.50
                                else:
                                    current_price = 0
                                # current_price = get_current_us_stock_price(user_profile.token, stock.code) * 1391.50
                            if current_price > 0 and stock.price != current_price:  
                                stock.price = current_price
                                stock.save()

                            updated_stocks.append({
                                "name": stock.name,
                                "code": stock.code,
                                "price": current_price
                            })
                        except Exception as e:
                            print(f"종목 {stock.code}의 가격 조회 실패: {e}")
                            continue

                    themes_info.append({
                        "theme_name": theme.name,
                        "stocks": updated_stocks,
                        "description": theme.description,
                    })

            # 6개로 제한
            themes_info = themes_info[:6]

            return JsonResponse({
                "message": "저장이 완료되었습니다.",
                "recommended_themes": themes_info
            })

        except json.JSONDecodeError:
            return JsonResponse({"error": "잘못된 JSON 형식입니다."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "GET 요청은 허용되지 않습니다."}, status=405)

def get_token(request):
    websocket_token = get_access_to_websocket()
    return JsonResponse({'websocket_token': websocket_token})

@api_view(['POST'])
def draw_theme_chart(request):
    try:
        user = request.user
        data = request.data
        user_profile = UserProfile.objects.get(user=user)
        access_token = user_profile.token
        theme_name = data.get('theme_name')
        end_date = data.get('end_date')
        # end_date를 datetime 객체로 변환
        end_date_obj = datetime.strptime(end_date, '%Y%m%d')
        
        # 1년 전 날짜 계산
        start_date_obj = end_date_obj - relativedelta(years=1)
        
        # YYYYMMDD 형식의 문자열로 변환
        start_date = start_date_obj.strftime('%Y%m%d')
        
        # 테마 정보 가져오기
        theme = Theme.objects.get(name=theme_name)
        theme_serializer = ThemeSerializer(theme)
        
        # 차트 데이터 가져오기
        chart_data = get_theme_price_series(
            access_token=access_token,
            theme_name=theme_name,
            start_date=start_date,
            end_date=end_date
        )
        
        # 응답 데이터 구성
        response_data = {
            'theme_info': theme_serializer.data,
            'chart_data': chart_data['data']
        }
        
        return Response(response_data)
    
    except Theme.DoesNotExist:
        return Response({
            'status': 'error',
            'message': f"Theme '{theme_name}' not found"
        }, status=404)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=500)
    

# front에서 해당 종목의 code, 현재시각을 전달받음
# 전달받은 시각 이전까지
@api_view(['POST'])
def d_chart_and_data(request):
    data = request.data
    stock_code = data.get('stock_code')
    current_time = data.get('current_time')
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    access_token = user_profile.token

    chart_data = get_domestic_stock_chartdata_day(
        access_token=access_token,
        stock_code=stock_code,
        current_time=current_time,
    )
    print(type(chart_data))
    ratio_data = get_domestic_stock_main_info(
        access_token=access_token,
        stock_code=stock_code,
    )
    consensus_data = get_domestic_stock_consensus(
        access_token=access_token,
        stock_code=stock_code
    )
    response_data = {
        'chart_data': chart_data,
        'ratio_data': ratio_data,
        'consensus_data': consensus_data
    }
    return Response(response_data)

# front로부터 stock_code를 받음
def o_chart_and_data(request):
    data = request.data
    stock_code = data.get('stock_code')
    stock = Stock.objects.get(code=stock_code)
    excd = stock.excd
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    access_token = user_profile.token

    chart_data = get_oversea_stock_chartdata_day(
        access_token=access_token,
        stock_code=stock_code,
        excd=excd
    )
    ratio_data = get_oversea_stock_main_info(
        access_token=access_token,
        stock_code=stock_code,
        excd=excd
    )

    response_data = {
        'chart_data': chart_data,
        'ratio_data': ratio_data,
    }
    return Response(response_data)

# front에게서 stock_code와 period를 받으면 함수 실행
@api_view(['POST'])
def d_chart_period(request):
    data = request.data
    stock_code = data.get('stock_code')
    period = data.get('period')
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    access_token = user_profile.token

    chart_data = get_domestic_stock_chartdata_period(
        access_token=access_token,
        stock_code=stock_code,
        period=period
    )
    response_data = {
        'chart_data':chart_data
    }
    return Response(response_data)


# front에게서 stock_code, period를 받으면 함수 실행
@api_view(['POST'])
def o_chart_period(request):
    data = request.data
    stock_code = data.get('stock_code')
    period = data.get('period')
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    access_token = user_profile.token

    chart_data = get_oversea_stock_chartdata_period(
        access_token=access_token,
        stock_code=stock_code,
        period=period
    )
    
    response_data = {
        'chart_data':chart_data
    }
    return Response(response_data)