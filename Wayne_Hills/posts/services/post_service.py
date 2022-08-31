from posts.serializers import GeneralPostSerializer


def create_general_post(create_post_data:dict[str|str]) -> None:
    """
    자유게시판의 Create를 담당하는 Service
    Args:
        create_post ={
            "user" (User): user.User 외래키,
            "post_type" (PostType) : posts.PostType 외래키,
            "title" (str): 게시글의 제목,
            "content" (str) : 게시글의 내용
        }
    Return:
        None
    """
    general_post_serializer = GeneralPostSerializer(data = create_post_data)
    general_post_serializer.is_valid(raise_exception=True)
    general_post_serializer.save()