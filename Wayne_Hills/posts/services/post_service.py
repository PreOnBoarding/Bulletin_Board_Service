from functools import partial
from posts.serializers import GeneralPostSerializer

from posts.models import Post as PostModel


def get_general_post() -> GeneralPostSerializer:
    """
    자유게시판의 Read를 담당하는 Service
    Args :
        None
    Return :
        GeneralPostSerializer
    """
    general_posts = PostModel.objects.filter(post_type=3)
    general_posts_serializer = GeneralPostSerializer(general_posts, many=True).data
    return general_posts_serializer


def create_general_post(create_general_post_data:dict[str|str]) -> None:
    """
    자유게시판의 Create를 담당하는 Service
    Args :
        create_general_post_data ={
            "user" (User): user.User 외래키,
            "post_type" (PostType) : posts.PostType 외래키(자유게시판은 3 고정),
            "title" (str): 게시글의 제목,
            "content" (str) : 게시글의 내용
        }
    Return :
        None
    """
    general_post_serializer = GeneralPostSerializer(data = create_general_post_data)
    general_post_serializer.is_valid(raise_exception=True)
    general_post_serializer.save()

def update_geneal_post(general_post_id : int, update_general_post_data: dict[str|str]):
    """
    자유게시판의 Update를 담당하는 Service
    Args :
        "general_post_id" (int): posts.Post 외래키, url에 담아서 보내줌,
        update_general_post_data = {
            "title" (str): 게시글의 제목 or
            "content" (str) : 게시글의 내용
        }
    Return :
        None
    """
    update_post = PostModel.objects.get(id=general_post_id)
    update_general_post_serializer = GeneralPostSerializer(update_post, update_general_post_data, partial=True)
    update_general_post_serializer.is_valid(raise_exception=True)
    update_general_post_serializer.save()
