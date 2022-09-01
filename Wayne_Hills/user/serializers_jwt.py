from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.Service.user_service import create_user_log
class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        create_user_log(user)
        token['username'] = user.username

        return token