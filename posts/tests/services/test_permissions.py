from django.test import TestCase

from posts.services.permissions import(
    check_can_get_post,
    check_can_create_post,
    check_can_update_post,
    check_can_delete_post
)
from posts.models import PostType as PostTypeModel, Post as PostModel
from user.models import UserType as UserTypeModel, User as UserModel

class TestPostPermission(TestCase):
    """
    Post의 permission들을 검증하는 클래스
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
    
    # 
    def test_check_can_get_post_when_general_user_get_general_post(self):
        """
        게시판 Get에 대한 권한을 체크하는 check_can_get_post Service 검증
        게시글 타입 : General
        유저 타입 : General
        """
        post_type_id = PostTypeModel.objects.get(post_type="General").id
        general_user = UserModel.objects.get(username = "general")
        self.assertEqual(check_can_get_post(post_type_id, general_user), True)

    def test_check_can_get_post_when_menager_user_get_general_post(self):
        """
        게시판 Get에 대한 권한을 체크하는 check_can_get_post Service 검증
        게시글 타입 : General
        유저 타입 : Manager
        """
        post_type_id = PostTypeModel.objects.get(post_type="General").id
        manager_user = UserModel.objects.get(username = "manager")
        self.assertEqual(check_can_get_post(post_type_id, manager_user), True)

    def test_check_can_get_post_when_general_user_get_admin_post(self):
        """
        게시판 Get에 대한 권한을 체크하는 check_can_get_post Service 검증
        게시글 타입 : Admin
        유저 타입 : General
        """
        post_type_id = PostTypeModel.objects.get(post_type="Admin").id
        general_user = UserModel.objects.get(username = "general")
        self.assertEqual(check_can_get_post(post_type_id, general_user), False)

    def test_check_can_get_post_when_manager_user_get_admin_post(self):
        """
        게시판 Get에 대한 권한을 체크하는 check_can_get_post Service 검증
        게시글 타입 : Admin
        유저 타입 : Manager
        """
        post_type_id = PostTypeModel.objects.get(post_type="Admin").id
        manager_user = UserModel.objects.get(username = "manager")
        self.assertEqual(check_can_get_post(post_type_id, manager_user), True)

    def test_check_can_get_post_when_general_user_get_notice_post(self):
        """
        게시판 Get에 대한 권한을 체크하는 check_can_get_post Service 검증
        게시글 타입 : Notice
        유저 타입 : General
        """
        post_type_id = PostTypeModel.objects.get(post_type="Notice").id
        general_user = UserModel.objects.get(username = "general")
        self.assertEqual(check_can_get_post(post_type_id, general_user), True)

    def test_check_can_get_post_when_manager_user_get_notice_post(self):
        """
        게시판 Get에 대한 권한을 체크하는 check_can_get_post Service 검증
        게시글 타입 : Notice
        유저 타입 : Manager
        """
        post_type_id = PostTypeModel.objects.get(post_type="Notice").id
        manager_user = UserModel.objects.get(username = "manager")
        self.assertEqual(check_can_get_post(post_type_id, manager_user), True)