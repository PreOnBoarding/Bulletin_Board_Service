from django.test import TestCase
from rest_framework import exceptions

from user.models import (
    User,
    UserType,
    UserLog,
)
from user.Service.user_service import (
    user_get_service,
    user_post_service,
    user_update_service,
    user_delete_service,
)

from django.db import connection
from django.test.utils import CaptureQueriesContext


class UserServiceView(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        TestCase를 위한 TestDB에 데이터 저장
        """
        user_type_list = ["manager", "general"]

        for user_type in user_type_list:
            UserType.objects.create(user_type=user_type)

        general_user = User.objects.create(
            username="general",
            password="general_password",
            gender="male",
            age="30",
            phone="010-0000-0000",
            user_type=UserType.objects.get(user_type="general")
        )
        manager_user = User.objects.create(
            username="manager",
            password="manager_password",
            gender="female",
            age="45",
            phone="010-1111-1111",
            user_type=UserType.objects.get(user_type="manager"))

    # 회원가입 기능 테스트

    def test_user_create_service(self):
        """ 
        회원가입 기능 테스트

        case : 정상 작동
        """

        user_info = {
            "username": "test",
            "password": "test_password",
            "gender": "female",
            "age": "45",
            "phone": "010-1212-1212",
            "user_type": "general"
        }

        count_1 = User.objects.all().count()

        with self.assertNumQueries(5):
            user_post_service(user_info)

        count_2 = User.objects.all().count()

        self.assertEqual(count_1 + 1, count_2)

    def test_user_create_when_does_not_create_object(self):
        """ 
        회원가입 기능 테스트

        case : 유저 오브젝트가 제대로 생성되지 않았을 경우
        """

        user_info = {
            "username": "test",
            "password": "test_password",
            "gender": "female",
            "age": "45",
            "phone": "010-1212-1212",
            "user_type": "general"
        }

        count_1 = User.objects.all().count()

        with self.assertRaises(AssertionError):
            with self.assertNumQueries(4):
                user_post_service(user_info)

        count_2 = User.objects.all().count()

        with self.assertRaises(AssertionError):
            self.assertNotEqual(count_1 + 1, count_2)

    def test_user_create_when_does_not_exist_user_type(self):
        """
        회원가입 기능 테스트

        case : 유저 타입이 존재하지 않을 경우
        """
        user_info = {
            "username": "test",
            "password": "test_password",
            "gender": "female",
            "age": "45",
            "phone": "010-1212-1212",
            "user_type": "null"
        }

        with self.assertRaises(UserType.DoesNotExist):
            user_post_service(user_info)

    def test_user_create_when_duplicate_of_username(self):
        """
        회원가입 기능 테스트

        case : 유저 이름이 중복될 경우
        """
        user_info = {
            "username": "general",
            "password": "test_password",
            "gender": "female",
            "age": "45",
            "phone": "010-1212-1212",
            "user_type": "general"
        }

        with self.assertRaisesMessage(
            exceptions.ValidationError,
            "{'username': [ErrorDetail(string='user with this 사용자 아이디 already exists.', code='unique')]}"
        ):
            user_post_service(user_info)

    def test_user_create_when_duplicate_of_phone(self):
        """
        회원가입 기능 테스트

        case : 유저 폰 번호가 중복될 경우
        """
        user_info = {
            "username": "test",
            "password": "test_password",
            "gender": "female",
            "age": "45",
            "phone": "010-0000-0000",
            "user_type": "general"
        }

        with self.assertRaisesMessage(
            exceptions.ValidationError,
            "{'phone': [ErrorDetail(string='user with this 폰 번호 already exists.', code='unique')]}"
        ):
            user_post_service(user_info)

    def test_user_create_when_username_is_out_of_range(self):
        """
        회원가입 기능 테스트

        case : 유저 이름이 12글자를 초과할 경우
        """
        user_info = {
            "username": "testtesttesttest",
            "password": "test_password",
            "gender": "female",
            "age": "45",
            "phone": "010-1212-1212",
            "user_type": "general"
        }

        with self.assertRaisesMessage(
            exceptions.ValidationError,
            "{'username': [ErrorDetail(string='Ensure this field has no more than 12 characters.', code='max_length')]"
        ):
            user_post_service(user_info)

    def test_user_create_when_username_is_blank(self):
        """
        회원가입 기능 테스트

        case : 유저 이름이 빈칸일 경우
        """
        user_info = {
            "username": "",
            "password": "test_password",
            "gender": "female",
            "age": "45",
            "phone": "010-1212-1212",
            "user_type": "general"
        }

        with self.assertRaisesMessage(
            exceptions.ValidationError,
            "{'username': [ErrorDetail(string='This field may not be blank.', code='blank')]}"
        ):
            user_post_service(user_info)

    def test_user_create_when_password_is_blank(self):
        """
        회원가입 기능 테스트

        case : 비밀번호가 빈칸일 경우
        """
        user_info = {
            "username": "test",
            "password": "",
            "gender": "female",
            "age": "45",
            "phone": "010-1212-1212",
            "user_type": "general"
        }

        with self.assertRaisesMessage(
            exceptions.ValidationError,
            "{'password': [ErrorDetail(string='This field may not be blank.', code='blank')]}"
        ):
            user_post_service(user_info)

    def test_user_create_when_phone_is_out_of_format(self):
        """
        회원가입 기능 테스트

        case : 비밀번호 형식이 맞지 않을 경우
        """
        user_info = {
            "username": "test",
            "password": "",
            "gender": "female",
            "age": "45",
            "phone": "010-12-1212",
            "user_type": "general"
        }

        with self.assertRaisesMessage(
            exceptions.ValidationError,
            "'phone': [ErrorDetail(string='Enter a valid value.', code='invalid')]"
        ):
            user_post_service(user_info)

    # 유저 정보 조회 기능 테스트

    def test_user_get_service(self):
        """
        유저 정보 조회 기능 테스트

        case : 정상 작동
        """

        with self.assertNumQueries(2):
            user_info = user_get_service("manager")

        self.assertEqual("manager", user_info["username"])

    def test_user_get_when_username_is_not_exist(self):
        """
        유저 정보 조회 기능 테스트

        case : 유저 이름이 존재하지 않을 경우
        """

        with self.assertRaises(User.DoesNotExist):
            user_get_service("manager1")
