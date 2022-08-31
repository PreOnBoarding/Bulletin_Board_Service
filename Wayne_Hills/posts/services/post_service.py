from posts.serializers import PostSerializer
from posts.models import Post as PostModel


def get_post(post_type) -> PostSerializer:
    """
    모든게시판의 Read를 담당하는 Service
    Args :
        "post_type" : posts.PostType 외래키 (urls에서 받아옴 1=공지, 2=운영, 3=자유)
    Return :
        PostSerializer
    """
    get_posts = PostModel.objects.filter(post_type=post_type)
    get_posts_serializer = PostSerializer(get_posts, many=True).data
    return get_posts_serializer

def create_post(create_post_data:dict[str|str], post_type : int) -> None:
    """
    Post의 Create를 담당하는 Service
    Args :
        create_post_data ={
            "user" (User): user.User 외래키,
            "title" (str): 게시글의 제목,
            "content" (str) : 게시글의 내용
        }
    Return :
        None
    """
    create_post_data["post_type"] = post_type
    post_serializer = PostSerializer(data = create_post_data)
    post_serializer.is_valid(raise_exception=True)
    post_serializer.save()

def update_post(post_id : int, update_post_data: dict[str|str]):
    """
    모든게시판의 Update를 담당하는 Service
    Args :
        "post_id" (int): posts.Post 외래키, url에 담아서 보내줌,
        update_post_data = {
            "title" (str): 게시글의 제목 or
            "content" (str) : 게시글의 내용
        }
    Return :
        None
    """
    update_post = PostModel.objects.get(id=post_id)
    update_post_serializer = PostSerializer(update_post, update_post_data, partial=True)
    update_post_serializer.is_valid(raise_exception=True)
    update_post_serializer.save()

def delete_post(post_id : int)-> None:
    """
    모든게시판의 Delete를 담당하는 Service
    Args :
        "post_id" (int): posts.Post 외래키, url에 담아서 보내줌
    Return :
        None
    """
    delete_post = PostModel.objects.get(id=post_id)
    delete_post.delete()
