"""
URL configuration for finalProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .auth_views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('stock.urls')),
    # path('api/v1/', include('stock.urls')),
    # 라이브러리에서 제공하는 경로 설정
    # 이 URL 세트에는 다음과 같은 엔드포인트가 포함됨.
    # 로그아웃: /accounts/logout/
    # 사용자 상세 정보: /accounts/user/
    # 비밀번호 변경: /accounts/password/change/
    # 회원탈퇴: /accounts/user/ (DELETE 메서드 사용)
    path('accounts/', include('dj_rest_auth.urls')),
    # 회원가입과 관련된 라이브러리 경로 설정
    path('accounts/signup/', include('dj_rest_auth.registration.urls')),
    # JWT토큰 기반 로그인기능   
    path('accounts/login/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
]
