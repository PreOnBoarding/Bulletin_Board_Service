from django.db import models


POST_TYPE_CHOICES = [
    ("Notice", "공지사항"),
    ("Admin", "운영게시판"),
    ("General", "자유게시판"),
]

class PostType(models.Model):
    """
    게시판의 종류를 담는 모델 (공지사항, 운영게시판, 자유게시판)
    """
    post_type = models.CharField("게시판 타입", max_length=10, choices=POST_TYPE_CHOICES, default="General")

    def __str__(self):
        return self.post_type


class Post(models.Model):
    """
    모든 게시판을 담는 모델 post_type으로 종류를 나눌 뿐 모두 Post모델 해당
    """
    user = models.ForeignKey("user.User", verbose_name="작성자", on_delete=models.CASCADE)
    post_type = models.ForeignKey(PostType, verbose_name="게시판 타입", on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=100)
    content = models.TextField("내용", max_length=2000)
    created_at = models.DateTimeField("게시글 등록 일자", auto_now_add=True)

    def __str__(self):
        return self.title


class PostUpdatedLog(models.Model):
    """
    게시판을 Update 할 때 업데이트 로그를 담는 모델 (Post update시 Create)
    """
    user = models.ForeignKey("user.User", verbose_name="수정자", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name="게시글", on_delete=models.CASCADE)
    updated_at = models.DateTimeField("게시글 업데이트 일자", auto_now_add=True)

    def __str__(self):
        return f"{self.post} 최근 업데이트 일자 : {self.updated_at}"