from rest_framework.views import APIView
from rest_framework import status, exceptions
from rest_framework.response import Response

from posts.services.post_service import (
    get_post,
    check_get_post,
    create_post,
    check_can_create_post,
    update_post,
    check_can_update_post,
    delete_post,
    check_can_delete_post,
)

POST_TYPE_LIST = ["", "공지사항", "운영게시판", "자유게시판"]

class PostView(APIView):
    """
    모든게시판의 CRUD를 담당하는 View
    """
    def get(self, request, post_type):
        if check_get_post(post_type, request.user):
            get_posts_serializer = get_post(post_type)
            return Response(get_posts_serializer, status=status.HTTP_200_OK)
        return Response({"detail": "접근 권한이 없습니다."},status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, post_type):
        if check_can_create_post(request.user, post_type):
            create_post(request.data, post_type)
            return Response({"detail" : POST_TYPE_LIST[post_type] + "에 게시물을 작성했습니다."}, status=status.HTTP_200_OK)
        return Response({"detail": "접근 권한이 없습니다."},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request, post_id):
        user = request.user
        if check_can_update_post(user, post_id):
            updated_log = update_post(user, post_id, request.data)
            return Response(updated_log, status=status.HTTP_200_OK)
        return Response({"detail": "접근 권한이 없습니다."},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request, post_id):
        if check_can_delete_post(request.user):
            delete_post(post_id)
            return Response({"detail" : "게시판의 글이 삭제되었습니다"}, status=status.HTTP_200_OK)
        return Response({"detail": "접근 권한이 없습니다."},status=status.HTTP_400_BAD_REQUEST)
