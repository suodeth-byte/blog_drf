from rest_framework import serializers
from myblog.models import Post

from django.contrib.auth.models import User


class PostListingField(serializers.RelatedField):
    def to_representation(self, value):
        return "Title: {}\n {}\n ".format(value.title, value.content)


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['title', 'date_created', 'content']

    # def to_representation(self, instance):
    #     return "Title: {}|  By {} \\n Content: {}".format(instance.title, instance.author.username, instance.content)

    # def create(self, validated_data):
    #     return Post.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True)
    # posts = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['posts', 'username', 'first_name', 'last_name', 'email']
