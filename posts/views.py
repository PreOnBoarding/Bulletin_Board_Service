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



class PostView(APIView):
    """
    모든게시판의 CRUD를 담당하는 View
    """


    def get(self, request, post_type):
        user_type = request.user.user_type_id  
        get_posts_serializer = get_post(post_type, user_type)
        if get_posts_serializer:
            return Response(get_posts_serializer, status=status.HTTP_200_OK)
        return Response({"detail": "접근 권한이 없습니다."},status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, post_type):
        user_type = request.user.user_type_id
        if create_post(request.data, post_type, user_type):
            return Response({"detail" : POST_TYPE_LIST[post_type] + "에 게시물을 작성했습니다."}, status=status.HTTP_200_OK)
        return Response({"detail": "접근 권한이 없습니다."},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request, post_id):
        user_type = request.user.user_type_id
        updated_data = update_post(post_id, request.data, user_type)
        if updated_data:
            return Response(updated_data, status=status.HTTP_200_OK)
        return Response({"detail": "접근 권한이 없습니다."},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request, post_id):
        user = request.user
        if delete_post(post_id, user):
            return Response({"detail" : "게시판의 글이 삭제되었습니다"}, status=status.HTTP_200_OK)
        return Response({"detail": "접근 권한이 없습니다."},status=status.HTTP_400_BAD_REQUEST)
