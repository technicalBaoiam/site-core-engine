from django.db import models
from django.conf import settings
from course.models import Category, Subcategory
User = settings.AUTH_USER_MODEL

class Blog(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="blogs", default=1)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name="blogs", default=1)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    blog_post = models.ForeignKey('Blog', on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'blog_post')  

    def __str__(self):
        return self.user.first_name