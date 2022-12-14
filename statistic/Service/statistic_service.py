from datetime import datetime, timedelta

from user.models import User, UserLog

def get_gender_statistics():
    """
        남여별 유저 로그인 횟수 통계 함수
    Args:
        None
    Return :
        male_count(int), female_count(int) : 로그인한 남자의 수, 여자의 수
    """ 
    male_count = UserLog.objects.filter(user__gender="male").count()
    female_count = UserLog.objects.filter(user__gender="female").count() 
    return male_count,female_count

def get_age_statistics():
    """
        나이별 유저 수 통계 함수

    Return :
        count_by_age (dict) : 나이구간별 유저 수
    """
    count_by_age = dict()

    for i in range(10):
        start_age = i * 10
        end_age = start_age + 9

        count = User.objects.filter(age__gte=start_age, age__lte=end_age).count()
        str_range = f"{start_age}~{end_age}"
        count_by_age[str_range] = count
    
    count = User.objects.filter(age__gte=100).count()
    str_range = f"100~"
    count_by_age[str_range] = count

    return count_by_age

def get_logintime_statistics():
    """
        접속 시간별 유저 수 통계 함수

    Return :
        count_by_logintime (dict) : 접속 시간별 유저 수
    """
    count_by_logintime = dict()
    
    for i in range(12):
        start_time = i * 2
        end_time = start_time + 2
        count = UserLog.objects.filter(login_date__hour__gte=start_time, login_date__hour__lt=end_time).count()
        str_time = f"{start_time}~{end_time}"
        count_by_logintime[str_time] = count
        

    return count_by_logintime