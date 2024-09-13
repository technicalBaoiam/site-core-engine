from rest_framework import serializers
from account.models import User
from .models import (
    Category, Subcategory, Course,
    Rating, Enrollment, Plan, Instructor,
    Order,
    Video, VideoPlaylist
)

# Course

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'category', 'description', 'created_at']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories', 'label', 'description', 'created_at']


# student
        
class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price']        

class CourseSerializer(serializers.ModelSerializer):
    plans = PlanSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 
            'category', 'subcategory', 'program_overview', 'brochure_file',
            'thumbnail_image', 'curriculum', 'plans'
        ]


   
class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)  # Directly access the 'title' attribute
    plan_type = serializers.CharField(source='plan.name', read_only=True)  # Directly access the 'title' attribute
    plan_price = serializers.DecimalField(source='plan.price', max_digits=10, decimal_places=2, read_only=True)  # Directly access the 'title' attribute
    # plan = PlanSerializer()
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'plan_type', 'plan_price', 'course_title', 'created_at']
     
# Orders and Payments
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id', 'student', 'plan', 'order_date', 'total_amount', 
            'payment_id', 'order_id', 'signature', 'status'
        ]
        read_only_fields = ['student', 'payment_id', 'order_id', 'signature']

   


# Instructor

class InstructorSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True) 

    class Meta:
        model = Instructor
        fields = [
            'id', 'first_name', 'last_name', 'bio',
            'email', 'hire_date', 'courses'
        ]

class RatingSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField() 

    class Meta:
        model = Rating
        fields = ['id', 'course', 'rating', 'comment']

class VideoSerializer(serializers.ModelSerializer):
    playlist = serializers.StringRelatedField()  

    class Meta:
        model = Video
        fields = ['id', 'playlist', 'title', 'url']

class VideoPlaylistSerializer(serializers.ModelSerializer):
    teacher = serializers.StringRelatedField()  
    videos = VideoSerializer(many=True, read_only=True) 

    class Meta:
        model = VideoPlaylist
        fields = ['id', 'teacher', 'title', 'description', 'videos']





