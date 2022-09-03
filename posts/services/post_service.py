from typing import Union, Dict
from posts.serializers import PostSerializer, PostUpdateLogSerializer
from posts.models import Post as PostModel
from user.models import User as UserModel



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
    

def create_post(create_post_data : Dict[str, str], post_type : int, user : UserModel) -> None:
    """
    Post의 Create를 담당하는 Service
    Args :
        create_post_data (dict) : {
            "title" (str): 게시글의 제목,
            "content" (str) : 게시글의 내용
        },
        post_type (int): posts.PostType 외래키 (urls에서 받아옴 1=공지, 2=운영, 3=자유)
        user (UserModel) : user.User 외래키 (request.user로 받아옴)
    Return :
        None
    """
    create_post_data["post_type"] = post_type
    create_post_data["user"] = user.id
    post_serializer = PostSerializer(data = create_post_data)
    post_serializer.is_valid(raise_exception=True)
    post_serializer.save()
        

def update_post(user : UserModel, post_id : int, update_post_data : Dict[str, str])-> Dict[str, Union[PostSerializer, PostUpdateLogSerializer]]:
    """
    모든게시판의 Update를 담당하는 Service
    update_post에 대한 검증이 이루어지면 update_log를 생성하는 함수에 대한 검증 실행
    두개 모두의 검증이 끝나야 저장
    Args :
        user (UserModel): user.User (request.user를 통해 로그인한 유저 반환),
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
    
