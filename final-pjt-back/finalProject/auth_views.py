from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            # 기본 TokenObtainPairView 동작 수행
            return super().post(request, *args, **kwargs)
        except ValidationError as e:
            # 요청 데이터에서 username 가져오기
            username = request.data.get("username")

            # 아이디 존재 여부 확인
            if not User.objects.filter(username=username).exists():
                return Response(
                    {"detail": "등록되지 않은 아이디입니다."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            
            # 비밀번호 오류 처리
            return Response(
                {"detail": "비밀번호가 올바르지 않습니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )