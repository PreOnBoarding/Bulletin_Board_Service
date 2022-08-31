from django.contrib import admin
from .models import (
    PostType,
    Post,
    PostUpdatedLog
)

admin.site.register(PostType)
admin.site.register(Post)
admin.site.register(PostUpdatedLog)