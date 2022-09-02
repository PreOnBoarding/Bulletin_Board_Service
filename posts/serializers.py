from rest_framework import serializers

from .models import Post as PostModel


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostModel
        fields = "__all__"