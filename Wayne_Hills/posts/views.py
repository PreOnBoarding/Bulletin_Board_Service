from rest_framework.views import APIView
from rest_framework import status, exceptions
from rest_framework.response import Response

from posts.services.post_service import (
    create_post,
    get_post,
    update_post,
    delete_post,
)
POST_TYPE_LIST = ["", "공지사항", "운영게시판", "자유게시판"]

# Create your views here.

class PostView(APIView):
    """
    모든게시판의 CRUD를 담당하는 View
    """

    def get(self, request, post_type):
        get_posts_serializer = get_post(post_type)
        return Response(get_posts_serializer, status=status.HTTP_200_OK)

    def post(self, request, post_type):
        create_post(request.data, post_type)    
        return Response({"detail" : POST_TYPE_LIST[post_type] + "에 게시물을 작성했습니다."}, status=status.HTTP_200_OK)

    def put(self,request, post_id):
        update_post(post_id, request.data)
        return Response({"detail" : "게시판의 글이 수정되었습니다"}, status=status.HTTP_200_OK)

    def delete(self,request, post_id):
        delete_post(post_id)
        return Response({"detail" : "게시판의 글이 삭제되었습니다"}, status=status.HTTP_200_OK)
