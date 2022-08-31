from user.models import User, UserType
from user.serializers import UserSerializer

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

    Returns:
        result (bool) : 회원가입 성공 여부
        result_detail
            : 회원가입 성공시 - None
            : 회원가입 실패시 - 회원가입 실패 사유

    Raises:


    """

    user_type_str = user_info.pop("user_type", "general")

    user_type_obj = UserType.objects.get(user_type=user_type_str)
    user_serializer = UserSerializer(data=user_info)
    if user_serializer.is_valid():
        user_serializer.save(user_type=user_type_obj)
        return True, None
    return False, user_serializer.errors
