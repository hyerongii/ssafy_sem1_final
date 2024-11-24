from rest_framework.response import Response
from .serializers import ThemeSerializer, ArticleSerializer, CommentSerializer, UserSerializer
from django.contrib.auth import get_user_model
from .utils import get_d_stock_chart_data_day, get_theme_price_series, get_current_stock_price, get_current_us_stock_price, get_domestic_stock_chartdata_period, get_oversea_stock_chartdata_day, get_oversea_stock_chartdata_period, get_domestic_stock_consensus, get_oversea_stock_main_info, get_stocks_info
from utils.token import get_access_token,get_access_to_websocket  # 프로젝트 레벨의 token 유틸리티 import
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
# Create your views here.
# 혜령 디버깅 추가
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import UserProfile, UserInterest, Interest, Theme, Stock, Article, Comment
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist


User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_user_info(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)  # user_pk로 User 객체 가져오기 (없으면 404 반환)
    serializer = UserSerializer(user)  # User 객체를 직렬화
    return Response(serializer.data)  # JSON 형태로 반환

# CSRF 보호 비활성화
# @csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
# 3가지 입력값 분석해서 6가지 테마 추천
@transaction.atomic
def analyze(request):
    if request.method != 'POST':
        return JsonResponse({"error": "GET 요청은 허용되지 않습니다."}, status=405)

    try:
        data = json.loads(request.body)
        user = request.user
        nickname = user.nickname

        # UserProfile 처리
        user_profile, created = UserProfile.objects.update_or_create(
            user=user,
            defaults={
                'mbti': data.get('mbti'),
                'period': data.get('period'),
                'token': get_access_token()
            }
        )

        # Interest 처리
        interest_names = data.get('interest', [])
        UserInterest.objects.filter(user=user).delete()

        # Interest 객체들을 이름으로 조회
        interests = Interest.objects.filter(name__in=interest_names)

        # 이름과 ID를 매핑하는 딕셔너리 생성
        interest_id_map = {interest.name: interest.id for interest in interests}

        # UserInterest 객체 생성
        user_interests = [
            UserInterest(user=user, interest_id=interest_id_map.get(interest_name))
            for interest_name in interest_names
            if interest_name in interest_id_map
        ]

        # bulk_create를 사용하여 한 번에 생성
        UserInterest.objects.bulk_create(user_interests)

        # 테마 및 주식 정보 수집
        all_stocks = {}  # 전역 주식 정보 저장
        processed_stocks = set()  # 전역 수준에서 처리된 주식 코드 추적
        themes_info = []
        theme_names = set(interest_names)

        # 필요한 경우 추가 테마 선택
        if len(theme_names) < 6:
            additional_themes = Theme.objects.exclude(name__in=theme_names).order_by('?')[:6-len(theme_names)]
            theme_names.update(theme.name for theme in additional_themes)

        for theme_name in theme_names:
            try:
                theme = Theme.objects.get(name=theme_name)
                unique_stocks = {}  # 테마 내 중복 제거용 임시 딕셔너리

                # 먼저 모든 주식 정보를 수집
                for stock in theme.stock_set.all():
                    if stock.code not in unique_stocks:  # 테마 내 중복 체크
                        try:
                            if stock.code not in processed_stocks:  # 전역 중복 체크
                                current_price = get_stock_price(user_profile.token, stock)
                                if current_price > 0 and stock.price != current_price:
                                    stock.price = current_price
                                    stock.save()

                                stock_info = {
                                    "name": stock.name,
                                    "code": stock.code,
                                    "price": current_price,
                                    "id": stock.id
                                }
                                all_stocks[stock.code] = stock_info
                                processed_stocks.add(stock.code)
                            else:
                                stock_info = all_stocks[stock.code]

                            unique_stocks[stock.code] = stock_info

                        except Exception as e:
                            print(f"종목 {stock.code}의 가격 조회 실패: {e}")
                            continue

                # 테마별 정보를 한 번만 추가
                themes_info.append({
                    "theme_name": theme.name,
                    "stocks": list(unique_stocks.values()),
                    "description": theme.description,
                })

            except ObjectDoesNotExist:
                print(f"테마 {theme_name}을/를 찾을 수 없습니다.")

        # 6개로 제한
        themes_info = themes_info[:6]

        # 동일한 MBTI 사용자의 테마 추천
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

def get_stock_price(token, stock):
    if stock.code.isdecimal():
        current_price = get_current_stock_price(token, stock.code)
    else:
        current_price = get_current_us_stock_price(token, stock.code, stock.excd)
        if current_price > 0:
            current_price = current_price * 1391.50
    return max(current_price, 0)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_token(request):
    
    websocket_token = get_access_to_websocket()
    return JsonResponse({'websocket_token': websocket_token})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
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
        
        # 중복 제거를 위한 처리
        stocks = theme.stock_set.all()
        unique_stocks = {}
        
        for stock in stocks:
            # 1. Stock 모델을 조회해 stock.code가 동일한 모든 인스턴스 파악
            duplicate_stocks = Stock.objects.filter(code=stock.code)
            # 2. 해당 인스턴스의 모든 stock.per / stock.pbr / stock.eps 수정
            stock_info = get_stocks_info(access_token, stock.code, stock.excd)
            per = stock_info[0]['PER']
            pbr = stock_info[0]['PBR']
            eps = stock_info[0]['EPS']
            
            for duplicate_stock in duplicate_stocks:
                duplicate_stock.per = per
                duplicate_stock.pbr = pbr
                duplicate_stock.eps = eps
                duplicate_stock.save()
            # 동일한 코드를 가진 주식이 없는 경우에만 추가
            if stock.code not in unique_stocks:
                unique_stocks[stock.code] = stock
        
        # Theme 객체의 stock_set을 중복이 제거된 주식들로 업데이트
        theme.stock_set.set(unique_stocks.values())
        
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
    

def get_recommended_themes(request):
    # 목표: 기존에 추천받았던 이력이 있는 유저는 "추천받은 테마" 탭을 누르면 
    # 기존에 추천받았던 테마를 곧바로 보여주도록 하고자 함.
    # 만약 기존에 추천받았던 이력이 없는 유저가 해당 탭을 누르는 경우
    # "아직 추천받은 테마가 없어요! 개인화된 분석을 진행해 주세요!" 알림창 띄우기(접근제한)
    # 1. UserInterest 테이블에 user_id와 interest_id 값이 저장되어 있음
    # 2. 해당 테이블은 "user_id 1의 관심 테마는 1,2,5 interest_id 이다" 라는 의미를 가지고 있음
    # 3. 유저가 "추천받은 테마" 탭을 누르는 경우 해당 함수가 실행됨
    # 4. user_id를 식별하기
    # 5. user_id를 이용해 UserInterest 테이블을 filtering
    # 6. interest_id를 이용해 Theme 테이블의 테마명(name) 값과 해당 theme와 관계된 stock을 리스트에 담아서 반환
    # 7. 단 아래의 형식으로 반환할 것. themes_info 에는 theme_name 키값과, stocks 키값(리스트)과 description 키값을 가짐.
    # return JsonResponse({
    #     "message": "저장이 완료되었습니다.",
    #     "recommended_themes": themes_info,
    # })

    # user_id를 식별하기
    user = request.user  # 로그인된 유저를 가져옴 (Django의 기본 인증 시스템 사용 가정)
    
    if not user.is_authenticated:
        return JsonResponse({
            "message": "로그인이 필요합니다.",
        }, status=401)

    # user_id를 이용해 UserInterest 테이블을 filtering
    user_interests = UserInterest.objects.filter(user_id=user.id)
    
    if not user_interests.exists():
        # 추천받은 이력이 없는 경우
        return JsonResponse({
            "message": "아직 추천받은 테마가 없어요! 개인화된 분석을 진행해 주세요!",
        }, status=404)

    # interest_id를 이용해 Theme 테이블의 테마명(name) 값과 관련 주식(stock)을 리스트에 담음
    themes_info = []
    for user_interest in user_interests:
        theme = get_object_or_404(Theme, id=user_interest.interest_id)
        related_stocks = Stock.objects.filter(theme_id=theme.id)  # Theme과 연결된 Stock 가져오기
        
        themes_info.append({
            "theme_name": theme.name,
            "description": theme.description,  # Theme의 설명 필드 (모델에 포함되어 있다고 가정)
            "stocks": list(related_stocks.values_list('name', flat=True))  # 주식 이름만 리스트로 변환
        })

    # JSON 응답 반환
    return JsonResponse({
        "message": "저장이 완료되었습니다.",
        "recommended_themes": themes_info,
    })

# front에서 해당 종목의 code, 현재시각을 전달받음
# 전달받은 시각 이전까지
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def d_chart(request):

    data = request.data
    stock_code = data.get('stock_code')
    current_time = data.get('current_time')
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    access_token = user_profile.token

    chart_data = get_d_stock_chart_data_day(
        access_token=access_token,
        stock_code=stock_code,
        current_time=current_time,
    )
    response_data = {
        'chart_data': chart_data,
    }
    return Response(response_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def d_main_data(request):
    data = request.data
    stock_code = data.get('stock_code')
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    access_token = user_profile.token

    stock = Stock.objects.filter(code=stock_code).first()
    ratio_data = {
        'PER': stock.per,
        'PBR': stock.pbr,
        'EPS': stock.eps,
    }

    consensus_data = get_domestic_stock_consensus(
        access_token=access_token,
        stock_code=stock_code
    )
    articles_data = get_stock_article_list(stock_code=stock_code)
    response_data = {
        'ratio_data': ratio_data,
        'consensus_data': consensus_data,
        'articles_data': articles_data,
    }
    return Response(response_data)

# front로부터 stock_code를 받음
# @csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def o_chart(request):
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
    
    response_data = {
        'chart_data': chart_data,
    }
    return Response(response_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def o_main_data(request):
    data = request.data
    stock_code = data.get('stock_code')
    stock = Stock.objects.filter(code=stock_code).first()
    excd = stock.excd
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    access_token = user_profile.token

    articles_data = get_stock_article_list(stock_code=stock_code)
    
    ratio_data = get_oversea_stock_main_info(
        access_token=access_token,
        stock_code=stock_code,
        excd=excd
    )

    response_data = {
        'ratio_data': ratio_data,
        'articles_data': articles_data
    }
    return Response(response_data)


# front에게서 stock_code와 period를 받으면 함수 실행
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
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
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
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
    
# @api_view(['DELETE', 'PUT'])
# def stock_article_delete_or_put(request):
#     data = request.data
#     article_id = data.get('article_id')
#     try:
#         article = Article.objects.get(pk=article_id)
        
#         # 작성자 본인 확인
#         if article.author.id != request.user.id:
#             return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
            
#         if request.method == 'DELETE':
#             article.delete()
#             return Response({'message': '게시글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
            
#         elif request.method == 'PUT':
#             serializer = ArticleSerializer(article, data=request.data)
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
#                 return Response(serializer.data)
                
#     except Article.DoesNotExist:
#         return Response({'message': '게시글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE', 'PUT'])
def stock_article_delete_or_put(request):
    data = request.data
    article_id = data.get('article_id')
    
    if not article_id:
        return Response({'message': 'article_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        article = Article.objects.get(pk=article_id)
        
        if article.author.id != request.user.id:
            return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
            
        if request.method == 'DELETE':
            article.delete()
            return Response({'message': '게시글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
            
        elif request.method == 'PUT':
            update_data = {
                'title': data.get('title'),
                'content': data.get('content'),
                'stock_code': data.get('stock_code')
            }
            serializer = ArticleSerializer(article, data=update_data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
                
    except Article.DoesNotExist:
        return Response({'message': '게시글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def get_stock_article_detail(request, article_pk):
    # 1. front에서 요청 시 받은 url의 article_pk를 이용해 조회    
    article = Article.objects.get(pk=article_pk)
    try:
        if request.method == 'GET':
            # 2. 조회한 article에 관계된 comment 조회
            comments = Comment.objects.filter(article=article)
            # 3. 직렬화
            article_serializer = ArticleSerializer(article)
            comment_serializer = CommentSerializer(comments, many=True)
            # 4. Response 데이터 구성
            response_data = {
                "article": article_serializer.data,
                "comments": comment_serializer.data,
            }
            return Response(response_data, status=200)
        # 댓글 쓰기
        elif request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(
                    article=article,
                    user=request.user,
                    stock=article.stock,
                    theme=article.theme
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                
    except Article.DoesNotExist:
        return Response({'message': '게시글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PUT', 'DELETE'])
def comment_update_delete(request, comment_pk):
    try:
        # 1. 댓글 조회
        comment = Comment.objects.get(pk=comment_pk)
        
        # 2. 작성자 본인 확인
        if comment.user.id != request.user.id:
            return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

        # 3. DELETE 요청 처리
        if request.method == 'DELETE':
            comment.delete()
            return Response({'message': '댓글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
        
        # 4. PUT 요청 처리
        elif request.method == 'PUT':
            serializer = CommentSerializer(comment, data=request.data, partial=True)  # 부분 업데이트 허용
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Comment.DoesNotExist:
        return Response({'message': '댓글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)