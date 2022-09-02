from pyexpat import model
from rest_framework import serializers

from .models import Post as PostModel, PostUpdatedLog as PostUpdatedLogModel


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostModel
        fields = "__all__"

class PostUpdateLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostUpdatedLogModel
        fields = "__all__"