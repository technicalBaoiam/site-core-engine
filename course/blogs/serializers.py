from rest_framework import serializers
from course.blogs.models import Blog, Comment

class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.first_name')
    
    class Meta:
        model = Comment
        fields = ['id', 'blog_post', 'content', 'user', 'created_at', 'updated_at']           
                    
class BlogSerializer(serializers.ModelSerializer):    
    comments = CommentsSerializer(many=True, read_only=True, required=False)
    author = serializers.StringRelatedField(required=False)
    
    class Meta:
        model = Blog
        fields = ['id', 'title', 'category', 'subcategory', 'description', 'author', 'created_at', 'updated_at', 'comments']