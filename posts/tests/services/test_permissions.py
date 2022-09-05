from multiprocessing.sharedctypes import Value
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
        for num in range(len(post_name_list)):
            PostModel.objects.create(
            user = manager_user if num <2 else general_user,
            title = post_name_list[num] + " 제목",
            content = post_name_list[num] + " 내용",
            post_type = PostTypeModel.objects.get(post_type=post_type_list[num])
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

    def test_check_can_get_post_when_manager_user_get_general_post(self):
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

    def test_check_can_get_post_with_correct_post_type_(self):
        """
        게시판 Get에 대한 권한을 체크하는 check_can_get_post Service post type이 정확한지 검증
        게시글 id 타입: int, float, True
        """
        true_post_type_id_list= [1, 3.5, True]
        user = UserModel.objects.get(username = "general")
        for item in true_post_type_id_list:
            
            self.assertEqual(check_can_get_post(item, user), True)


    def test_check_can_get_post_with_incorrect_post_type_printing_value_error(self):
        """
        게시판 Get에 대한 권한을 체크하는 check_can_get_post Service 검증 
        post type이 정확하지 않아 value 에러를 출력할때
        게시글 id 타입: String
        """
        false_post_type_id_list=["","string"]
        user = UserModel.objects.get(username = "general")
        for item in false_post_type_id_list:
            with self.assertRaises(ValueError):
                check_can_get_post(item, user)

    def test_check_can_get_post_with_incorrect_post_type_printing_type_error(self):
        """
        게시판 Get에 대한 권한을 체크하는 check_can_get_post Service 검증 
        post type이 없거나 정확하지 않아 type error를 출력할때
        게시글 id 타입: 복소수
        """
        false_post_type_id_list=[2+5j]
        user = UserModel.objects.get(username = "general")
        for item in false_post_type_id_list:
            with self.assertRaises(TypeError):
                check_can_get_post(item, user)

    def test_check_can_get_post_with_incorrect_post_type_matching_query_error(self):
        """
        게시판 Get에 대한 권한을 체크하는 check_can_get_post Service 검증
        post type이 없거나 정확하지 않아 matching query error를 출력할때
        게시글 id: post type에 해당하지 않는 정수
        """
        false_post_type_id_list=[-3,5]
        user = UserModel.objects.get(username = "general")
        for item in false_post_type_id_list:
            with self.assertRaises(PostTypeModel.DoesNotExist):
                check_can_get_post(item, user)

    def test_check_can_get_post_with_incorrect_user_type_(self):
        """
        게시판 Get에 대한 권한을 체크하는 check_can_get_post Service 검증
        user type이 없거나 정확하지 않아 attribute error를 출력할때
        게시글 id 타입: string, float, usertype에 해당하지 않는 정수
        """
        false_user_type_list=["string", 12, 3.5, ""]
        post = PostTypeModel.objects.get(post_type="General").id
        for user in false_user_type_list:
            with self.assertRaises(AttributeError):
                check_can_get_post(post, user)

    def test_check_can_create_post_when_general_user_get_general_post(self):
        """
        게시판 POST 에 대한 권한을 체크하는 check_can_create_post Service 검증
        게시글 타입 : General
        유저 타입 : General
        """
        post_type_id = PostTypeModel.objects.get(post_type="General").id
        general_user = UserModel.objects.get(username = "general")
        self.assertEqual(check_can_create_post(general_user, post_type_id), True)

    def test_check_can_create_post_when_manager_user_get_general_post(self):
        """
        게시판 POST 에 대한 권한을 체크하는 check_can_create_post Service 검증
        게시글 타입 : General
        유저 타입 : Manager
        """
        post_type_id = PostTypeModel.objects.get(post_type="General").id
        manager_user = UserModel.objects.get(username = "manager")
        self.assertEqual(check_can_create_post(manager_user, post_type_id), True)

    def test_check_can_create_post_when_general_user_get_admin_post(self):
        """
        게시판 POST 에 대한 권한을 체크하는 check_can_create_post Service 검증
        게시글 타입 : Admin
        유저 타입 : General
        """
        post_type_id = PostTypeModel.objects.get(post_type="Admin").id
        general_user = UserModel.objects.get(username = "general")
        self.assertEqual(check_can_create_post(general_user, post_type_id), False)

    def test_check_can_create_post_when_manager_user_get_admin_post(self):
        """
        게시판 POST 에 대한 권한을 체크하는 check_can_create_post Service 검증
        게시글 타입 : Admin
        유저 타입 : Manager
        """
        post_type_id = PostTypeModel.objects.get(post_type="Admin").id
        manager_user = UserModel.objects.get(username = "manager")
        self.assertEqual(check_can_create_post(manager_user, post_type_id), True)

    def test_check_can_create_post_when_general_user_get_notice_post(self):
        """
        게시판 POST 에 대한 권한을 체크하는 check_can_create_post Service 검증
        게시글 타입 : Notice
        유저 타입 : General
        """
        post_type_id = PostTypeModel.objects.get(post_type="Notice").id
        general_user = UserModel.objects.get(username = "general")
        self.assertEqual(check_can_create_post(general_user, post_type_id), False)

    def test_check_can_create_post_when_manager_user_get_notice_post(self):
        """
        게시판 POST 에 대한 권한을 체크하는 check_can_create_post Service 검증
        게시글 타입 : Notice
        유저 타입 : Manager
        """
        post_type_id = PostTypeModel.objects.get(post_type="Notice").id
        manager_user = UserModel.objects.get(username = "manager")
        self.assertEqual(check_can_create_post(manager_user, post_type_id), True)

    def test_check_can_create_post_with_incorrect_user_type_(self):
        """
        게시판 POST 에 대한 권한을 체크하는 check_can_create_post Service 검증
        user type이 정확하지 않아 attribute error를 출력할때
        게시글 타입 : string, float 복소수, post_type id에 해당하지 않는 정수
        """
        false_user_type_list=["string", 12, 3.5, ""]
        post = PostTypeModel.objects.get(post_type="General").id
        for user in false_user_type_list:
            with self.assertRaises(AttributeError):
                check_can_create_post(user, post)
                
    def test_check_can_create_post_with_incorrect_post_type_(self):
        """
        게시판 POST 에 대한 권한을 체크하는 check_can_create_post Service 검증
        post type이 정확하지 않아 attribute error를 출력할때
        게시글 타입 : string, float 복소수, post_type id에 해당하지 않는 정수
        """
        false_post_type_list=["","string",3, 2+5j, 1.5]
        user = UserModel.objects.get(username = "general")
        for item in false_post_type_list:
            with self.assertRaises(AttributeError):
                check_can_get_post(user, item)

    def test_check_can_update_post_when_general_user_get_general_post(self):
        """
        게시판 Update에 대한 권한을 체크하는 check_can_get_post Service 검증
        게시글 타입 : General
        유저 타입 : General
        """
        post_type_id = PostTypeModel.objects.get(post_type="General").id
        general_user = UserModel.objects.get(username = "general")
        self.assertEqual(check_can_update_post(general_user, post_type_id), True)

    def test_check_can_update_post_when_manager_user_get_general_post(self):
        """
        게시판 Update에 대한 권한을 체크하는 check_can_get_post Service 검증
        게시글 타입 : General
        유저 타입 : Manager
        """
        post_type_id = PostTypeModel.objects.get(post_type="General").id
        manager_user = UserModel.objects.get(username = "manager")
        self.assertEqual(check_can_update_post(manager_user, post_type_id), False)

    def test_check_can_update_post_when_general_user_get_admin_post(self):
        """
        게시판 Update에 대한 권한을 체크하는 check_can_get_post Service 검증
        게시글 타입 : Admin
        유저 타입 : General
        """
        post_type_id = PostTypeModel.objects.get(post_type="Admin").id
        general_user = UserModel.objects.get(username = "general")
        self.assertEqual(check_can_update_post(general_user, post_type_id), False)

    def test_check_can_update_post_when_manager_user_get_admin_post(self):
        """
        게시판 Update에 대한 권한을 체크하는 check_can_get_post Service 검증
        게시글 타입 : Admin
        유저 타입 : Manager
        """
        post_type_id = PostTypeModel.objects.get(post_type="Admin").id
        manager_user = UserModel.objects.get(username = "manager")
        self.assertEqual(check_can_update_post(manager_user, post_type_id), True)

    def test_check_can_update_post_when_general_user_get_notice_post(self):
        """
        게시판 Update에 대한 권한을 체크하는 check_can_get_post Service 검증
        게시글 타입 : Notice
        유저 타입 : General
        """
        post_type_id = PostTypeModel.objects.get(post_type="Notice").id
        general_user = UserModel.objects.get(username = "general")
        self.assertEqual(check_can_update_post(general_user, post_type_id), False)

    def test_check_can_update_post_when_manager_user_get_notice_post(self):
        """
        게시판 Update에 대한 권한을 체크하는 check_can_get_post Service 검증
        게시글 타입 : Notice
        유저 타입 : Manager
        """
        post_type_id = PostTypeModel.objects.get(post_type="Notice").id
        manager_user = UserModel.objects.get(username = "manager")
        self.assertEqual(check_can_update_post(manager_user, post_type_id), True)

    def test_check_can_update_post_when_user_is_author(self):
        """
        게시판 Update에 대한 권한을 체크하는 check_can_get_post Service 검증
        게시글 타입 : Notice
        유저 타입 : Manager
        """
        post_type_id = PostTypeModel.objects.get(post_type="General").id
        general_user = UserModel.objects.get(username = "general")
        self.assertEqual(check_can_update_post(general_user, post_type_id), True)

    def test_check_can_update_post_when_user_is_not_author(self):
        """
        게시판 Update에 대한 권한을 체크하는 check_can_get_post Service 검증
        게시글 타입 : Notice
        유저 타입 : Manager
        """
        post_type_id = PostTypeModel.objects.get(post_type="General").id
        general_user = UserModel.objects.get(username = "manager")
        self.assertEqual(check_can_update_post(general_user, post_type_id), False)

    def test_check_can_delete_post_when_general_user_get_general_post(self):
        """
        게시판 Delete에 대한 권한을 체크하는 check_can_get_post Service 검증
        게시글 타입 : General
        유저 타입 : General
        """
        post_type_id = PostTypeModel.objects.get(post_type="General").id
        general_user = UserModel.objects.get(username = "general")
        self.assertEqual(check_can_delete_post(general_user, post_type_id), True)

    def test_check_can_delete_post_when_manager_user_get_general_post(self):
        """
        게시판 Delete에 대한 권한을 체크하는 check_can_get_post Service 검증
        게시글 타입 : General
        유저 타입 : Manager
        """
        post_type_id = PostTypeModel.objects.get(post_type="General").id
        manager_user = UserModel.objects.get(username = "manager")
        self.assertEqual(check_can_delete_post(manager_user, post_type_id), True)

    def test_check_can_delete_post_when_general_user_get_admin_post(self):
        """
        게시판 Delete에 대한 권한을 체크하는 check_can_get_post Service 검증
        게시글 타입 : Admin
        유저 타입 : General
        """
        post_type_id = PostTypeModel.objects.get(post_type="Admin").id
        general_user = UserModel.objects.get(username = "general")
        self.assertEqual(check_can_delete_post(general_user, post_type_id), False)

    def test_check_can_delete_post_when_manager_user_get_admin_post(self):
        """
        게시판 Delete에 대한 권한을 체크하는 check_can_get_post Service 검증
        게시글 타입 : Admin
        유저 타입 : Manager
        """
        post_type_id = PostTypeModel.objects.get(post_type="Admin").id
        manager_user = UserModel.objects.get(username = "manager")
        self.assertEqual(check_can_delete_post(manager_user, post_type_id), True)

    def test_check_can_delete_post_when_general_user_get_notice_post(self):
        """
        게시판 Delete에 대한 권한을 체크하는 check_can_get_post Service 검증
        게시글 타입 : Notice
        유저 타입 : General
        """
        post_type_id = PostTypeModel.objects.get(post_type="Notice").id
        general_user = UserModel.objects.get(username = "general")
        self.assertEqual(check_can_delete_post(general_user, post_type_id), False)

    def test_check_can_delete_post_when_manager_user_get_notice_post(self):
        """
        게시판 Delete에 대한 권한을 체크하는 check_can_get_post Service 검증
        게시글 타입 : Notice
        유저 타입 : Manager
        """
        post_type_id = PostTypeModel.objects.get(post_type="Notice").id
        manager_user = UserModel.objects.get(username = "manager")
        self.assertEqual(check_can_delete_post(manager_user, post_type_id), True)

    def test_check_can_delete_post_when_author(self):
        """
        게시판 Delete에 대한 권한을 체크하는 check_can_get_post Service 검증
        게시글 타입: User가 작성한 게시글
        유저 타입 : General
        """
        post_type_id = PostTypeModel.objects.get(user=1).id
        user = UserModel.objects.get(username = "general")
        self.assertEqual(check_can_delete_post(user, post_type_id), True)

    def test_check_can_delete_post_when_not_author(self):
        """
        게시판 Delete에 대한 권한을 체크하는 check_can_get_post Service 검증
        게시글 타입: User가 작성한 게시글
        유저 타입 : General
        """
        post_type_id = PostTypeModel.objects.get(user=2).id
        user = UserModel.objects.get(username = "general")
        self.assertEqual(check_can_delete_post(user, post_type_id), True)


