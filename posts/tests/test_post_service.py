from django.test import TestCase
from rest_framework import exceptions

from posts.models import PostType as PostTypeModel, Post as PostModel
from user.models import UserType as UserTypeModel, User as UserModel

from posts.services.post_service import(
    get_post,
    create_post,
    update_post,
    delete_post
)


NOTICE=1
ADMIN=2
GENERAL=3

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
            user_type = UserTypeModel.objects.get(user_type="general")
            )
        manager_user = UserModel.objects.create(
            username="manager", 
            password="manager_password",
            gender = "male",
            age = "30",
            phone = "010-1111-1111",
            user_type = UserTypeModel.objects.get(user_type="manager")
            )
        # 공지사항, 운영게시판, 자유게시판 생성
        post_name_list = ["공지사항", "운영게시판", "자유게시판"]
        for A in range(3):
            PostModel.objects.create(
            user = manager_user if A <2 else general_user,
            title = post_name_list[A] + " 제목",
            content = post_name_list[A] + " 내용",
            post_type = PostTypeModel.objects.get(post_type=post_type_list[A])
        )
        

    def test_get_post(self):
        """
        post_type에 따라 게시판을 불러오는 service 검증
        case : 정상적으로 작동 했을 경우
        """
        with self.assertNumQueries(1):
            get_post(NOTICE)

    def test_create_post(self):
        """
        post_type별로 게시물을 저장하는 service 검증
        case : 정상적으로 작동 했을 경우
        """
        manager_user = UserModel.objects.get(username = "manager")
        post_type = GENERAL
        request_date = {
            "user" : manager_user.id,
            "title" : "제목",
            "content" : "내용"}
        with self.assertNumQueries(3):
            create_post(request_date, post_type, manager_user)

    def test_update_post(self):
        """
        생성되어있는 게시물을 업데이트하는 service 검증
        case : 정상적으로 작동 했을 경우
        """
        general_user = UserModel.objects.get(username = "general")
        general_post_id = PostModel.objects.get(content = "자유게시판 내용").id
        update_post_data = {"title" : "제목수정"}
        with self.assertNumQueries(5):
            update_post(general_user, general_post_id, update_post_data)

    def test_delete_post(self):
        """
        생성되어있는 게시물을 삭제하는 service 검증
        case : 정상적으로 작동 했을 경우
        """
        general_post_id = PostModel.objects.get(content = "자유게시판 내용").id
        with self.assertNumQueries(3):
            delete_post(general_post_id)



