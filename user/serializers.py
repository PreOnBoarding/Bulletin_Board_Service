from rest_framework import serializers


from .models import User, UserType, UserLog


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ["user_type"]

class UserLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLog
        fields = ["user", "login_date"]

class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()

    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        return user

    def get_user_type(self, obj):
        if obj.user_type:
            return obj.user_type
        return "None"


    class Meta:
        model = User
        fields = ["user_type", "username", "password", "gender",
         "age", "phone", "joined_date"
        ]

        extra_kwargs = {
            'password': {'write_only': True}
        }

