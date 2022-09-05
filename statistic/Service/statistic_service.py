from user.models import UserLog

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