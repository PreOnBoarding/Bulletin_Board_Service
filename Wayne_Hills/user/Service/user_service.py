from user.models import User, UserType, UserLog
from user.serializers import UserSerializer, UserLogSerializer, GenderStatisticsSerializer

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

def get_gender_statistics():
    """
        남여별 로그인빈도 통계를 Return해주는 함수
    Args:
        None
    Return :
        male_count(int), female_count(int) : 로그인한 남자의 수, 여자의 수
    """ 
    male_count = UserLog.objects.filter(user__gender="male").count()
    female_count = UserLog.objects.filter(user__gender="female").count() 
    return male_count,female_count