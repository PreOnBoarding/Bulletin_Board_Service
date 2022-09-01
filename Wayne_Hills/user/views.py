from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from user.serializers_jwt import TokenObtainPairSerializer

from user.Service.user_service import (
    user_get_service,
    user_post_service,
    get_gender_statistics,
    )

# 유저 CRUD 기능
class UserView(APIView):
    """
    User의 CRUD를 담당하는 View
    """
    permission_classes = [permissions.AllowAny]

    # 유저 조회 기능
    def get(self, request, username):
        res = user_get_service(username)


        return Response({"username": username, "res": res}, status=status.HTTP_200_OK)

    # 회원가입 기능
    def post(self, request):
        result, result_detail = user_post_service(request.data)
            
        if result:
            return Response({"detail": "회원가입 성공"}, status=status.HTTP_200_OK)

        return Response(result_detail, status=status.HTTP_400_BAD_REQUEST)

class TokenObtainPairView(TokenObtainPairView):
    """
    Login을 구현하는 View
    내부에서 UserLog를 생성하는 함수 내장
    """
    serializer_class = TokenObtainPairSerializer
    
class GenderStatisticsView(APIView):

    def get(self, request):
        gender_statistics_serializer = get_gender_statistics()
        return Response(gender_statistics_serializer, status=status.HTTP_200_OK)
