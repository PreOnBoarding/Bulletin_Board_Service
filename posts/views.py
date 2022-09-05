from rest_framework.views import APIView
from rest_framework import status, exceptions
from rest_framework.response import Response
from posts.models import Post as PostModel
from posts.services.post_service import (
    get_post,
    create_post,
    update_post,
    delete_post,
)
from posts.services.permissions import (
    check_can_get_post,
    check_can_create_post,
    check_can_update_post,
    check_can_delete_post,
)

POST_TYPE_LIST = ["", "공지사항", "운영게시판", "자유게시판"]

class PostView(APIView):
    """
    모든게시판의 CRUD를 담당하는 View
    """
    def get(self, request, post_type):
        try:
            if check_can_get_post(post_type, request.user):
                get_posts_serializer = get_post(post_type)
                return Response(get_posts_serializer, status=status.HTTP_200_OK)
            return Response({"detail" : "접근 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError: 
            return Response({"detail" : "로그인을 하고 이용해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
    
    def post(self, request, post_type):
        try:
            if check_can_create_post(request.user, post_type):
                create_post(request.data, post_type, request.user)
                return Response({"detail" : POST_TYPE_LIST[post_type] + "에 게시물을 작성했습니다."}, status=status.HTTP_200_OK)
            return Response({"detail" : "접근 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.ValidationError:
            return Response({"detail" : "접근 권한은 있지만, 형식에 맞지 않는 요소가 있습니다."}, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError: 
            return Response({"detail" : "로그인을 하고 이용해주세요."}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, post_id):
        user = request.user
        try:
            if check_can_update_post(user, post_id):
                if request.data == {}:
                    return Response({"detail" : "수정할 내용이 없습니다."},status=status.HTTP_400_BAD_REQUEST)
                updated_log = update_post(user, post_id, request.data)
                return Response(updated_log, status=status.HTTP_200_OK)
            return Response({"detail" : "접근 권한이 없습니다."},status=status.HTTP_400_BAD_REQUEST)
        except PostModel.DoesNotExist:
            return Response({"detail" : "수정할 게시글이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        except AttributeError: 
            return Response({"detail" : "로그인을 하고 이용해주세요."}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, post_id):
        try:
            if check_can_delete_post(request.user, post_id):
                delete_post(post_id)
                return Response({"detail" : "게시판의 글이 삭제되었습니다."}, status=status.HTTP_200_OK)
            return Response({"detail": "접근 권한이 없습니다."},status=status.HTTP_400_BAD_REQUEST)
        except PostModel.DoesNotExist:
            return Response({"detail" : "삭제할 게시글이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        except AttributeError: 
            return Response({"detail" : "로그인을 하고 이용해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
