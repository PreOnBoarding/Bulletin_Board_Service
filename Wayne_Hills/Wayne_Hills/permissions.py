from rest_framework.permissions import BasePermission
from django.contrib.auth import authenticate
from rest_framework.exceptions import APIException
from rest_framework import status

class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code=status_code
        super().__init__(detail=detail, code=code)

class IsAdminOrReadOnly(BasePermission):
    """
    admin 사용자는 모두 가능, 조회는 모두 가능
    """
    SAFE_METHODS = ('GET', )

    def has_permission(self, request, view):
        user = request.user
        if not self.SAFE_METHODS and not user.is_authenticated:
            response ={"detail": "서비스를 이용하기 위해 로그인 해주세요."}
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)
        return bool(self.SAFE_METHODS or (user.is_authenticated and user.is_admin))

class IsAuthenticatedOrReadOnly(BasePermission):
    """
    #자유게시판 get/post
    조회: 모두 가능, 작성: 가입된 사람만
    """
    SAFE_METHODS = ('GET', )

    def has_permission(self, request, view):
        user = request.user

        if not self.SAFE_METHODS and not user.is_authenticated:
            response ={"detail": "서비스를 이용하기 위해 로그인 해주세요."}
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)

        return bool(self.SAFE_METHODS or user.is_authenticated)


class IsAdminOrIsAthenticatedPutOnly(BasePermission):
    """
    #자유게시판 put/delete
    수정: 가입된 사람만, 삭제: 가입된 사람 및 운영자
    """
    SAFE_METHODS = ('PUT', )

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            response ={"detail": "서비스를 이용하기 위해 로그인 해주세요."}
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)

        return bool(self.SAFE_METHODS or (user.is_authenticated and user.is_admin))




