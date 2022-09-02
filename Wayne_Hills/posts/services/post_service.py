from typing import Union, Dict
from posts.serializers import PostSerializer, PostUpdateLogSerializer
from posts.models import Post as PostModel
from .permissions import is_manager, is_general
from user.models import User as UserModel

NOTICE=1
ADMIN=2
GENERAL=3

def get_post(post_type : int) -> PostSerializer:
    """
    모든게시판의 Read를 담당하는 Service
    Args :
        post_type (int): posts.PostType 외래키 (urls에서 받아옴 1=공지, 2=운영, 3=자유)
    Return :
        PostSerializer
    """
    get_posts = PostModel.objects.filter(post_type=post_type)
    get_posts_serializer = PostSerializer(get_posts, many=True).data
    return get_posts_serializer
    

def check_get_post(post_type : int, user : UserModel) -> bool:
    """
    get_post의 접근 권한을 담당하는 Service
    Args:
        post_type (int): posts.PostType 외래키 (urls에서 받아옴 1=공지, 2=운영, 3=자유)
        user (UserModel): user.User 외래키 (request.user를 통해 로그인한 유저 반환)

    Returns:
        bool
    """
    user_type = user.user_type_id  
    if (post_type==ADMIN and is_manager(user_type)) or post_type in [NOTICE,GENERAL]:
        return True
    return False


def create_post(create_post_data : Dict[str, Union[UserModel, str]], post_type : int) -> None:
    """
    Post의 Create를 담당하는 Service
    Args :
        create_post_data (dict) : {
            "user" (User): user.User 외래키,
            "title" (str): 게시글의 제목,
            "content" (str) : 게시글의 내용
        },
        post_type (int): posts.PostType 외래키 (urls에서 받아옴 1=공지, 2=운영, 3=자유)
    Return :
        None
    """
    create_post_data["post_type"] = post_type
    post_serializer = PostSerializer(data = create_post_data)
    post_serializer.is_valid(raise_exception=True)
    post_serializer.save()
        

def check_can_create_post(user : UserModel, post_type : int) -> bool:
    """
    create_post의 접근 권한을 담당하는 Service
    Args:
        user (UserModel): user.User 외래키 (request.user를 통해 로그인한 유저 반환)
        post_type (int): posts.PostType 외래키 (urls에서 받아옴 1=공지, 2=운영, 3=자유)

    Returns:
        bool
    """
    user_type = user.user_type_id
    if is_manager(user_type) or (post_type==GENERAL and is_general(user_type)):
        return True
    return False


def update_post(user : int, post_id : int, update_post_data : Dict[str, str])-> Dict[str, Union[PostSerializer, PostUpdateLogSerializer]]:
    """
    모든게시판의 Update를 담당하는 Service
    update_post에 대한 검증이 이루어지면 update_log를 생성하는 함수에 대한 검증 실행
    두개 모두의 검증이 끝나야 저장
    Args :
        user (UserModel): user.User 외래키 (request.user를 통해 로그인한 유저 반환),
        post_id (int): posts.Post 외래키, url에 담아서 보내줌,
        update_post_data (dict): {
            "title" (str): 게시글의 제목 or
            "content" (str) : 게시글의 내용
        }
    Return :
        dict[str, Union[PostSerializer, PostUpdateLogSerializer]]
    """
    log_data = {"user" : user.id, "post" : post_id}

    update_post = PostModel.objects.get(id=post_id)
    update_post_serializer = PostSerializer(update_post, update_post_data, partial=True)
    update_post_serializer.is_valid(raise_exception=True)

    post_update_log_serializer = PostUpdateLogSerializer(data=log_data)
    post_update_log_serializer.is_valid(raise_exception=True)

    update_post_serializer.save()
    post_update_log_serializer.save()
    return (
        {"update_post" : update_post_serializer.data}, 
        {"update_log" : post_update_log_serializer.data}
        )

def check_can_update_post(user : UserModel, post_id : int):
    """
    update_post의 접근 권한을 담당하는 Service
    Args:
        user (UserModel): user.User 외래키 (request.user를 통해 로그인한 유저 반환),
        post_id (int): posts.Post 외래키, url에 담아서 보내줌
    Returns:
        bool
    """
    user_type = user.user_type_id
    post_type = PostModel.objects.get(id=post_id).post_type
    if is_manager(user_type) or (post_type==GENERAL and is_general(user_type)):
        return True
    return False


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
    

def check_can_delete_post(user : UserModel) -> bool:
    """
    delete_post의 접근 권한을 담당하는 Service
    Args:
        user (UserModel): user.User 외래키 (request.user를 통해 로그인한 유저 반환),
    Returns:
        bool
    """
    user_type = user.user_type_id
    if user_type==1 or (user_type==2 and delete_post.user==user):
        return True
    return False
