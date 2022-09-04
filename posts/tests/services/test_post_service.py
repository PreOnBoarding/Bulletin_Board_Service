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

DOSE_NOT_EXIST_NUM = 0

class TestPostService(TestCase):
    """
    post의 service들을 검증하는 클래스
    """

    @classmethod
    def setUpTestData(cls):
        """
        TestCase를 위한 TestDB에 데이터 저장
        """
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
        post_type에 따라 게시판을 불러오는 get_post service 검증
        case : 정상적으로 작동 했을 경우
        """
        with self.assertNumQueries(1):
            get_post(NOTICE)

    def test_create_post(self):
        """
        post_type별로 게시물을 저장하는 create_post service 검증
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

    def test_create_post_when_does_not_exist_post_type(self):
        """
        post_type별로 게시물을 저장하는 create_post service 검증
        case : 존재하지 않는 post_type을 넣었을 경우
        """
        post_type = DOSE_NOT_EXIST_NUM
        manager_user = UserModel.objects.get(username = "manager")
        request_date = {
            "user" : DOSE_NOT_EXIST_NUM,
            "title" : "제목",
            "content" : "내용"}
        with self.assertRaises(exceptions.ValidationError):
            create_post(request_date, post_type, manager_user)

    def test_create_post_when_does_not_has_title(self):
        """
        post_type별로 게시물을 저장하는 create_post service 검증
        case : title이 비어있는 경우
        """
        post_type = DOSE_NOT_EXIST_NUM
        manager_user = UserModel.objects.get(username = "manager")
        request_date = {
            "user" : DOSE_NOT_EXIST_NUM,
            "content" : "내용"}
        with self.assertRaises(exceptions.ValidationError):
            create_post(request_date, post_type, manager_user)

    def test_create_post_when_does_not_has_content(self):
        """
        post_type별로 게시물을 저장하는 create_post service 검증
        case : content가 비어있는 경우
        """
        post_type = DOSE_NOT_EXIST_NUM
        manager_user = UserModel.objects.get(username = "manager")
        request_date = {
            "user" : DOSE_NOT_EXIST_NUM,
            "title" : "제목",}
        with self.assertRaises(exceptions.ValidationError):
            create_post(request_date, post_type, manager_user)

    def test_update_post(self):
        """
        생성되어있는 게시물을 업데이트하는 update_post service 검증
        case : 정상적으로 작동 했을 경우
        """
        general_user = UserModel.objects.get(username = "general")
        general_post_id = PostModel.objects.get(content = "자유게시판 내용").id
        update_post_data = {"title" : "제목수정"}
        with self.assertNumQueries(5):
            update_post(general_user, general_post_id, update_post_data)

    def test_update_post_when_post_id_does_not_exist(self):
        """
        생성되어있는 게시물을 업데이트하는 update_post service 검증
        case : 수정할 post_id가 존재하지 않는 id인 경우
        """
        general_user = UserModel.objects.get(username = "general")
        post_id = DOSE_NOT_EXIST_NUM
        update_post_data = {"title" : "제목수정"}
        with self.assertRaises(PostModel.DoesNotExist):
            update_post(general_user, post_id, update_post_data)

    def test_update_post_when_update_data_does_not_exist(self):
        """
        생성되어있는 게시물을 업데이트하는 update_post service 검증
        case : 수정할 내용이 비어있는 경우
        if문으로 request.data를 검증 후 비었다면 예외처리로 해결
        """
        general_user = UserModel.objects.get(username = "general")
        general_post_id = PostModel.objects.get(content = "자유게시판 내용").id
        update_post_data = {}
        with self.assertNumQueries(5):
            update_post(general_user, general_post_id, update_post_data)

    def test_delete_post(self):
        """
        생성되어있는 게시물을 삭제하는 delete_post service 검증
        case : 정상적으로 작동 했을 경우
        """
        general_post_id = PostModel.objects.get(content = "자유게시판 내용").id
        with self.assertNumQueries(3):
            delete_post(general_post_id)

    def test_delete_post_when_post_id_does_not_exist(self):
        """
        생성되어있는 게시물을 삭제하는 delete_postservice 검증
        case : 삭제할 post_id가 존재하지 않는 id인 경우
        """
        post_id = DOSE_NOT_EXIST_NUM
        with self.assertRaises(PostModel.DoesNotExist):
            delete_post(post_id)



