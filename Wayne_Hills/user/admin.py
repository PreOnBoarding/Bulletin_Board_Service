from django.contrib import admin
from .models import User, UserType, UserLog


admin.site.register(User)
admin.site.register(UserType)
admin.site.register(UserLog)