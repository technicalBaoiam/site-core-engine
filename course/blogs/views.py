from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from course.blogs.models import Blog, Comment
from course.blogs.serializers import BlogSerializer, CommentsSerializer
from course.permissions import IsAdminOrReadOnly
from rest_framework.response import Response


class BlogCreateListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = BlogSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)

    def get_queryset(self):
        queryset = Blog.objects.all()
        category_id = self.request.query_params.get("category")
        subcategory_id = self.request.query_params.get("subcategory")

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if subcategory_id:
            queryset = queryset.filter(subcategory_id=subcategory_id)

        return queryset

          
    
class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    
    def get_permissions(self):
        if self.request.method == ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated()]
        elif self.request.method == 'GET':
            return [AllowAny()]   
        else:
            return [IsAuthenticated()]            
    
class CommentCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    
    def get_permissions(self):
        if self.request.method == ['POST', 'PUT', 'PATCH']:
            return [IsAuthenticated()]
        elif self.request.method == 'GET':
            return [AllowAny()]   
        else:
            return [IsAuthenticated()]

    def perform_create(self, serializer):
        user = self.request.user 
        serializer.validated_data['user'] = user  # Authenticated user
        serializer.save()
    
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        else:
            return [IsAuthenticated()]