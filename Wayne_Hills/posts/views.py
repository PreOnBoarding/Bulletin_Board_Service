from rest_framework.views import APIView
from rest_framework import status, exceptions
from rest_framework.response import Response

from posts.services.post_service import create_general_post

# Create your views here.

class GeneralPostView(APIView):
    """
    자유게시판의 CRUD를 담당하는 View
    """
    def post(self,request):
        create_general_post(request.data)
        return Response({"detail" : "자유게시판에 게시물을 작성했습니다."}, status=status.HTTP_200_OK)
