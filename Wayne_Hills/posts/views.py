from rest_framework.views import APIView
from rest_framework import status, exceptions
from rest_framework.response import Response

from posts.services.post_service import (
    create_general_post,
    get_general_post,
    update_geneal_post
)

# Create your views here.

class GeneralPostView(APIView):
    """
    자유게시판의 CRUD를 담당하는 View
    """
    def get(self, request):
        general_posts_serializer = get_general_post()
        return Response(general_posts_serializer, status=status.HTTP_200_OK)

    def post(self,request):
        create_general_post(request.data)
        return Response({"detail" : "자유게시판에 게시물을 작성했습니다."}, status=status.HTTP_200_OK)

    def put(self,request, general_post_id):
        update_geneal_post(general_post_id, request.data)
        return Response({"detail" : "자유게시판의 글이 수정되었습니다"}, status=status.HTTP_200_OK)

