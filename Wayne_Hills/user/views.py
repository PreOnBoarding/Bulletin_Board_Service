from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from user.Service.user_service import (
    user_get_service,
    user_post_service,
    )

# 유저 CRUD 기능
class UserView(APIView):
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