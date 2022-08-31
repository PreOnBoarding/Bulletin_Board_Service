from posts.serializers import GeneralPostSerializer

from posts.models import Post as PostModel

def create_general_post(create_post_data:dict[str|str]) -> None:
    """
    자유게시판의 Create를 담당하는 Service
    Args :
        create_post ={
            "user" (User): user.User 외래키,
            "post_type" (PostType) : posts.PostType 외래키(자유게시판은 3 고정),
            "title" (str): 게시글의 제목,
            "content" (str) : 게시글의 내용
        }
    Return :
        None
    """
    general_post_serializer = GeneralPostSerializer(data = create_post_data)
    general_post_serializer.is_valid(raise_exception=True)
    general_post_serializer.save()

def get_general_post():
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