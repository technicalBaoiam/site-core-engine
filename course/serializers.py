from rest_framework import serializers
from account.models import User
from .models import (
    Category, Subcategory, Course,
    Rating, Enrollment, Plan, Instructor,
    Order,
    Video, VideoPlaylist
)

# subcategory
class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'category']


#  plans    
class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price']    
       
# course
# class CourseSerializer(serializers.ModelSerializer):

#     plans = PlanSerializer(many=True, read_only=True)

#     class Meta:
#         model = Course
#         fields = [
#             'id', 'title', 'description', 
#             'category', 'subcategory', 'program_overview', 'brochure_file',
#             'thumbnail_image', 'curriculum', 'plans', 'featured'
#         ]

class CourseSerializer(serializers.ModelSerializer):
    subcategory = SubcategorySerializer(read_only=True)
    plans = PlanSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        exclude = ['featured', 'course_code']

# category
class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True, read_only=True)
    courses = CourseSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories', 'label', 'description', 'courses', 'created_at']


# enrollment
class EnrollmentSerializer(serializers.ModelSerializer):

    # later certificate and course completion fiels is to be added here
    plan = PlanSerializer()
    course = CourseSerializer()

    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'course', 'plan', 'created_at', 'updated_at', 'type', 'enrollment_number', 'payment_due'          
        ]
        
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

# ratings
class RatingSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField() 

    class Meta:
        model = Rating
        fields = ['id', 'course', 'rating', 'comment']

# videos
class VideoSerializer(serializers.ModelSerializer):
    playlist = serializers.StringRelatedField()  

    class Meta:
        model = Video
        fields = ['id', 'playlist', 'title', 'url']

# playlist
class VideoPlaylistSerializer(serializers.ModelSerializer):
    teacher = serializers.StringRelatedField()  
    videos = VideoSerializer(many=True, read_only=True) 

    class Meta:
        model = VideoPlaylist
        fields = ['id', 'teacher', 'title', 'description', 'videos']





