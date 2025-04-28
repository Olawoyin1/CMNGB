from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import BlogPost, BlogCategory, BlogComment
from .serializers import BlogPostSerializer, BlogCategorySerializer, BlogCommentSerializer


class BlogPostListCreateAPIView(APIView):
    def get(self, request):
        posts = BlogPost.objects.all().order_by('-created_at')
        serializer = BlogPostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            return Response({'detail': 'Only admin can create posts'}, status=403)
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class BlogPostDetailAPIView(APIView):
    def get(self, request, slug):
        try:
            post = BlogPost.objects.get(slug=slug)
            serializer = BlogPostSerializer(post)
            return Response(serializer.data)
        except BlogPost.DoesNotExist:
            return Response({'detail': 'Post not found'}, status=404)


class BlogCategoryListAPIView(APIView):
    def get(self, request):
        categories = BlogCategory.objects.all()
        serializer = BlogCategorySerializer(categories, many=True)
        return Response(serializer.data)


class BlogCommentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = BlogPost.objects.get(id=post_id)
        except BlogPost.DoesNotExist:
            return Response({'detail': 'Post not found'}, status=404)

        serializer = BlogCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
