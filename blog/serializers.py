from rest_framework import serializers
from .models import BlogCategory, BlogPost, BlogComment


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'name']


class BlogCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BlogComment
        fields = ['id', 'user', 'comment', 'created_at']


class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    category = BlogCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=BlogCategory.objects.all(), source='category', write_only=True
    )
    comments = BlogCommentSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'content', 'image',
            'category', 'category_id', 'author', 'created_at',
            'updated_at', 'comments'
        ]
