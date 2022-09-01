from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator

class UserType(models.Model):
    USER_CHOICES = (
        ("manager", "운영자"),
        ("general", "일반 사용자"),
    )

    user_type = models.CharField("유저 유형", max_length=100, choices=USER_CHOICES)

    def __str__(self):
        return self.user_type

class UserLog(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    login_date = models.DateTimeField("로그인", auto_now_add=True)

    def __str__(self):
        return self.user

class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # python manage.py createsuperuser 사용 시 해당 함수가 사용됨
    def create_superuser(self, username, password=None):
        user =  self.model(
            username=username,
            gender="undefined"
        ) 
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    GENDER_CHOICES = (
        ("male", "남성"),
        ("female", "여성"),
        ("undefined", "미선택"),
    )
    phone_validator = RegexValidator(regex = r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')


    user_type = models.ForeignKey(UserType, on_delete=models.SET_NULL, null=True)
    
    username = models.CharField("사용자 아이디", max_length=12, unique=True)
    password = models.CharField("비밀번호", max_length=128)
    gender = models.CharField("성별", max_length=20, choices=GENDER_CHOICES, default="undefined")
    age = models.IntegerField("나이", default=0)
    phone = models.CharField("폰 번호", validators=[phone_validator], max_length=13, unique=True, null=True, blank=True)
    joined_date = models.DateTimeField("가입일", auto_now_add=True)
    
    def __str__(self):
        return f"{self.username}"

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin