from rest_framework import permissions, status, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from user.serializers_jwt import TokenObtainPairSerializer

from user.Service.user_service import (
    user_get_service,
    user_post_service,
    user_update_service,
    user_delete_service,
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
        try:
            user_post_service(request.data)
            return Response({"detail": "회원가입 성공"}, status=status.HTTP_200_OK)
        except AssertionError:
            return Response({"detail": "회원가입에 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 회원정보 수정기능
    def put(self, request):
        user_obj = request.user

        try:
            if user_update_service(user_obj, request.data):
                return Response( {"detail": "회원정보 수정 성공"}, status=status.HTTP_200_OK)
            return Response({"detail" : "현재 비밀번호가 옳바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"detail" : "회원정보 수정에 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 회원탈퇴 기능
    def delete(self, request):
        user_obj = request.user
        if user_delete_service(user_obj):
            return Response({"detail" : "회원 탈퇴 성공"}, status=status.HTTP_200_OK)
        return Response({"detail" : "회원 탈퇴에 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)
    

class TokenObtainPairView(TokenObtainPairView):
    """
    Login을 구현하는 View
    내부에서 UserLog를 생성하는 함수 내장
    """
    serializer_class = TokenObtainPairSerializer
    