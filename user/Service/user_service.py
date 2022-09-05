from  django.contrib.auth.hashers import make_password

from user.models import User, UserType, UserLog
from user.serializers import UserSerializer, UserLogSerializer

def user_get_service(username: int):
    """ 
        사용자이름에 해당하는 유저 정보 반환 함수

    Args:
        username (str): 사용자이름 

    Returns:
        user_info (dict) : 유저 정보

    Raises:


    """

    user_obj = User.objects.get(username=username)

    user_info = UserSerializer(user_obj).data

    return user_info


def user_post_service(user_info: dict):
    """ 
        사용자정보로 회원가입하는 함수

    Args:
        user_info (dict): 회원가입할 유저 정보 


    Raises:


    """

    user_type_str = user_info.pop("user_type", "general")

    user_type_obj = UserType.objects.get(user_type=user_type_str)
    user_serializer = UserSerializer(data=user_info)
    user_serializer.is_valid(raise_exception=True)
    user_serializer.save(user_type=user_type_obj)


def user_update_service(user_obj: User, update_info: dict):
    """
        회원 정보 수정 함수
    
    Args:
        user_obj (User): 수정할 유저 오브젝트
        update_info (dict): 수정 정보 

    Returns:
        result (bool) : 회원탈퇴(비활성화) 성공 여부

    Raises:
    
    """

    # 현재 비밀번호 일치 여부 확인 코드
    cur_password = update_info.pop("old_password", None)
    print(cur_password)
    if not user_obj.check_password(cur_password):
        return False

    # 새로운 비밀번호 수정정보에 추가
    new_password = update_info.pop("new_password", None)
    if new_password:
        update_info["password"] = new_password

    user_serializer = UserSerializer(user_obj, data=update_info, partial=True)
    user_serializer.is_valid(raise_exception=True)
    user_serializer.save()

    return True



def user_delete_service(user_obj: User):
    """회원탈퇴 기능 함수    

    Args:
        user_obj (User): 탈퇴할 유저 오브젝트

    Returns:
        result (bool) : 회원탈퇴(비활성화) 성공 여부
    
    """

    user_obj.is_active = False
    user_obj.save()

    return not user_obj.is_active

def create_user_log(user):
    """
        로그인이 되었을 때 자동으로 UserLog를 생성해주는 함수
    Args:
        user (User): serializers_jwt.py에서 받아오는 user
    Return :
        None
    """
    request_data = {"user" : user.id}
    user_log_serializer = UserLogSerializer(data=request_data)
    user_log_serializer.is_valid(raise_exception=True)
    user_log_serializer.save()

