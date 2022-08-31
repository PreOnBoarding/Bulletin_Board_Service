from user.models import User
from user.serializers import UserSerializer

def user_get_service(username:str) -> dict:
    """ 
        사용자이름에 해당하는 유저 정보 반환 함수

    Args:
        username (string): 사용자이름 

    Returns:
        Serializer() : 유저 정보

    Raises:


    """

    user_obj = User.objects.get(username=username)

    user_info = UserSerializer(user_obj).data

    return user_info