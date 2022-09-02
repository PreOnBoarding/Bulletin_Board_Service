from django.test import TestCase
from rest_framework import exceptions

from posts.models import PostType as PostTypeModel, Post as PostModel
from user.models import UserType as UserTypeModel, User as UserModel



class TestPostService(TestCase):
    """
    post의 service들을 검증하는 클래스
    """

    @classmethod
    def setUpTestData(cls):
        user_type_list = ["manager", "general"]
        post_type_list = ["Notice", "Admin", "General"]
        

        for post_type in post_type_list:
            PostTypeModel.objects.create(post_type=post_type)
        for user_type in user_type_list:
            UserTypeModel.objects.create(user_type=user_type)
        
        general_user = UserModel.objects.create(
            username="general", 
            password="general_password",
            gender = "male",
            age = "30",
            phone = "010-0000-0000",
            user_type = "general"
            )
        manager_user = UserModel.objects.create(
            username="manager", 
            password="manager_password",
            gender = "male",
            age = "30",
            phone = "010-1111-1111",
            user_type = "manager"
            )
        # 공지사항, 운영게시판, 자유게시판 생성
        post_name_list = ["공지사항", "운영게시판", "자유게시판"]
        for A in range(2):
            PostModel.objects.create(
            user = manager_user if A >2 else general_user,
            title = post_name_list[A] + " 제목",
            content = post_name_list[A] + " 내용",
            post_type = PostTypeModel.objects.get(post_type=post_type_list[A]).id
        )
        


