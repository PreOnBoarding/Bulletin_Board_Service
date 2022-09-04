from posts.models import Post as PostModel, PostType
from user.models import User as UserModel

USER_MANAGER="manager"
USER_GENERAL="general"

POST_NOTICE= "Notice"
POST_ADMIN= "Admin"
POST_GENERAL= "General"

def take_user_type(user : UserModel):
    """
    유저의 타입이 무엇인지 srt로 반환해주는 함수
    Args:
        user (UserModel): user obj
    Returns:
        USER_MANAGER or "general"
    """
    return user.user_type.user_type    

def user_is_manager(user_type:str)->bool:
    """
    유저의 타입이 manager인가를 체크
    """
    return bool(user_type==USER_MANAGER)

def user_is_general(user_type:str)->bool:
    """
    유저의 타입이 general인가를 체크
    """
    return bool(user_type==USER_GENERAL)

def post_is_notice(post_type:str)->bool:
    """
    게시물의 타입이 notice인가를 체크
    """
    return bool(post_type==POST_NOTICE)
    
def post_is_admin(post_type:str)->bool:
    """
    게시물의 타입이 admin인가를 체크
    """
    return bool(post_type==POST_ADMIN)

def post_is_general(post_type:str)->bool:
    """
    게시물의 타입이 genera인가를 체크
    """
    return bool(post_type==POST_GENERAL)

def is_author(user, post_id)->bool:
    """
    유저가 게시물 작성자인가를 체크
    """
    post_obj = PostModel.objects.get(id=post_id).post_type.post_type
    return bool(user==post_obj.user)


def check_can_get_post(post_type_id : int, user : UserModel) -> bool:
    """
    get_post의 접근 권한을 담당하는 Service
    Args:
        post_type (int): posts.PostType 외래키 (urls에서 받아옴 1=공지, 2=운영, 3=자유)
        user (UserModel): user.User 외래키 (request.user를 통해 로그인한 유저 반환)
    Returns:
        bool
    """
    user_type = take_user_type(user)
    post_type = PostType.objects.get(id=post_type_id).post_type
    if (
        (post_is_admin(post_type) and user_is_manager(user_type)) 
        or
        post_is_notice(post_type)
        or 
        post_is_general(post_type)):
        return True
    return False


def check_can_create_post(user : UserModel, post_type_id : int) -> bool:
    """
    create_post의 접근 권한을 담당하는 Service
    Args:
        user (UserModel): user.User 외래키 (request.user를 통해 로그인한 유저 반환)
        post_type (int): posts.PostType 외래키 (urls에서 받아옴 1=공지, 2=운영, 3=자유)
    Returns:
        bool
    """
    user_type = take_user_type(user)
    post_type = PostType.objects.get(id=post_type_id).post_type
    if (
        user_is_manager(user_type) 
        or 
        (user_is_general(user_type) and post_is_general(post_type))):
        return True
    return False


def check_can_update_post(user : UserModel, post_id : int):
    """
    update_post의 접근 권한을 담당하는 Service
    Args:
        user (UserModel): user.User 외래키 (request.user를 통해 로그인한 유저 반환),
        post_id (int): posts.Post 외래키, url에 담아서 보내줌
    Returns:
        bool
    """
    user_type = take_user_type(user)
    post_type = PostModel.objects.get(id=post_id).post_type.post_type
    if (
        (user_is_manager(user_type) and post_is_notice(post_type))
        or 
        (is_author(user, post_id))):
        return True
    return False


def check_can_delete_post(user : UserModel, post_id : int) -> bool:
    """
    delete_post의 접근 권한을 담당하는 Service
    Args:
        user (UserModel): user.User 외래키 (request.user를 통해 로그인한 유저 반환),
    Returns:
        bool
    """
    user_type = take_user_type(user)
    post_type = PostModel.objects.get(id=post_id).post_type.post_type
    if (
        (user_is_manager(user_type) and (post_is_notice(post_type) or post_is_general(post_type)))
        or 
        is_author(user, post_id)):
        return True
    return False