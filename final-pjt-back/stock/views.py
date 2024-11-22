from rest_framework.response import Response
from .serializers import ThemeSerializer
from django.contrib.auth import get_user_model
from .utils import get_theme_price_series, get_current_stock_price, get_current_us_stock_price, get_domestic_stock_chartdata_day, get_domestic_stock_chartdata_period, get_oversea_stock_chartdata_day, get_oversea_stock_chartdata_period, get_domestic_stock_main_info, get_domestic_stock_consensus, get_oversea_stock_main_info
from utils.token import get_access_token,get_access_to_websocket  # 프로젝트 레벨의 token 유틸리티 import
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.
# 혜령 디버깅 추가
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import UserProfile, UserInterest, Interest, Theme, Stock, Article
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random

User = get_user_model()
# CSRF 보호 비활성화
# @csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
# 3가지 입력값 분석해서 6가지 테마 추천
def analyze(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user
            user_id = user.pk
            user_for_nickname = User.objects.get(id=user_id)
            nickname = user_for_nickname.nickname
            
            
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
            # 나랑 동일한 mbti의 사람들은 무슨 테마를 추천받았을까?
            same_theme_names = get_same_mbti_theme(request)
            return JsonResponse({
                "message": "저장이 완료되었습니다.",
                "recommended_themes": themes_info,
                "same_theme_names": same_theme_names,
                "nickname": nickname
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

    ratio_data = get_domestic_stock_main_info(
        access_token=access_token,
        stock_code=stock_code,
    )
    consensus_data = get_domestic_stock_consensus(
        access_token=access_token,
        stock_code=stock_code
    )
    articles_data = get_stock_article_list(stock_code=stock_code)
    print(articles_data)
    response_data = {
        'chart_data': chart_data,
        'ratio_data': ratio_data,
        'consensus_data': consensus_data,
        'articles_data': articles_data,
    }
    return Response(response_data)

# front로부터 stock_code를 받음
# @csrf_exempt
@api_view(['POST'])
def o_chart_and_data(request):
    data = request.data
    stock_code = data.get('stock_code')
    stock = Stock.objects.filter(code=stock_code).first()
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


def get_same_mbti_theme(request):
    try:
        # 1. 현재 유저의 user_id를 조인키로 UserProfile의 mbti 조회
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        me_mbti = user_profile.mbti
        # 2. 해당 유저의 user_id를 제외한 다른 유저의 mbti가 
        # 현재 유저의 mbti와 동일한 경우의 user_id를 리스트에 저장
        same_mbti_user_list = UserProfile.objects.filter(
            mbti=me_mbti
        ).exclude(
            user=user
        ).values_list('user_id', flat=True)

        # 3. 해당 리스트 중 랜덤한 user_id를 선택하여
        # UserInterest 테이블의 interest_id를 반환
        if same_mbti_user_list:
            random_user_id = random.choice(same_mbti_user_list)
            interest_ids = UserInterest.objects.filter(
                user_id=random_user_id
            ).values_list('interest_id', flat=True)
            # 4. interest_id를 조인키로 
            # Interest 테이블의 name을 리스트에 담아 반환
            interest_names = list(Interest.objects.filter(
                id__in=interest_ids
            ).values_list('name', flat=True))
            # 딕셔너리 형태로 반환
            return {
                'status': 'success',
                'interests': interest_names
            }
        
        return {
            'status': 'success',
            'interests': []
        }
        
    except UserProfile.DoesNotExist:
        return {
            'status': 'error',
            'message': 'User profile not found',
            'interests': []
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'interests': []
        }
    
def get_stock_article_list(stock_code):
    try:
        # 1. 현재 조회하고 있는 stock 확인
        stock = Stock.objects.filter(code=stock_code).first()
        
        if not stock:
            return {
                'status': 'error',
                'message': 'Stock not found',
                'articles': []
            }
            
        # 2. stock을 참조하고 있는 article 리스트 조회
        articles = Article.objects.filter(
            stock_id=stock.pk
        ).values(
            'id',
            'title',
            'content',
            'author__nickname',  # User 모델의 nickname
            'created_at',
            'updated_at',
            'like_article',
            'theme__name'  # Theme 모델의 name
        ).order_by('-created_at')  # 최신순 정렬
        
        # QuerySet을 리스트로 변환하여 JSON serializable하게 만듦
        article_list = list(articles)
        
        # datetime 객체를 문자열로 변환
        for article in article_list:
            article['created_at'] = article['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            article['updated_at'] = article['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
        
        return {
            'status': 'success',
            'stock_name': stock.name,
            'articles': article_list
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'articles': []
        }
    
@api_view(['POST'])
# @csrf_exempt
# @permission_classes([IsAuthenticated])
def create_stock_article(request):
    try:
        data = request.data
        stock_code = data.get('stock_code')
        
        # 1. 주식 정보 확인
        stock = Stock.objects.filter(code=stock_code).first()
        if not stock:
            return JsonResponse({
                'status': 'error',
                'message': '존재하지 않는 주식 코드입니다.'
            })
            
        # 2. 게시글 생성에 필요한 데이터 받아오기
        title = data.get('title')
        content = data.get('content')
        
        # 3. 필수 필드 검증
        if not all([title, content]):
            return JsonResponse({
                'status': 'error',
                'message': '필수 필드가 누락되었습니다.'
            })
        
        user = request.user
        user_id = user.pk
        user_for_article = User.objects.get(id=user_id)
        
        # 4. 게시글 생성 (theme는 stock의 theme 사용)
        article = Article.objects.create(
            stock=stock,
            theme=stock.theme,  # stock에 연결된 theme 사용
            author=user_for_article,
            title=title,
            content=content
        )
        
        # 5. 응답 데이터 구성
        response_data = {
            'status': 'success',
            'article_id': article.id,
            'message': '게시글이 성공적으로 작성되었습니다.'
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })