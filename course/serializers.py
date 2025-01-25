from rest_framework import serializers
from django.db.models import Avg
from .models import (
    Category, Subcategory, Course,
    Rating, Enrollment, Plan, Instructor,
    Order,
    Video, VideoPlaylist,
    Slider, SliderItem,
    Wishlist, Certificate
)
from utils.videos_and_sharable_link import get_videos_course, share_certificate_link

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
        
class CourseEnrollmentSerializer(serializers.Serializer):
    course_status = serializers.ChoiceField(choices=['ongoing', 'recent', 'enrolled', 'not_enrolled', 'completed'], required=False)
    
    def validate_filter(self, attrs):
        if attrs not in ['ongoing', 'recent', 'enrolled', 'not_enrolled', 'completed']:
            raise serializers.ValidationError("Invalid filter type!!")
        return attrs

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
    playlist = serializers.PrimaryKeyRelatedField(queryset=VideoPlaylist.objects.all())  

    class Meta:
        model = Video
        fields = ['id', 'playlist', 'title', 'description', 'video_file']

# playlist
class VideoPlaylistSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True) 

    class Meta:
        model = VideoPlaylist
        fields = ['id', 'instructor', 'title', 'description', 'videos']

# limited course-detail for app 
class CourseLimitSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'subcategory', 'category']
    
# limited enroll-detail for app 
class EnrollLimitSerializer(serializers.ModelSerializer):
    course = CourseLimitSerializer(many=False, read_only=True)
    videos = serializers.SerializerMethodField()   
    
    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'videos', 'enrollment_number']
        
    def get_videos(self, obj):
        course = obj.course
        if course:
            course_id = course.id
            videos = get_videos_course(course_id)
            return VideoSerializer(videos, many=True).data
        return []
    
# slider    
class SliderImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    
    class Meta:
        model = Slider
        fields = '__all__'
        
class SliderItemSerializer(serializers.ModelSerializer):
    sliders = SliderImageSerializer(many=True)
    
    class Meta:
        model = SliderItem
        fields = ['id', 'title', 'caption', 'order', 'sliders']
        
    def create(self, validated_data):
        sliders_data = validated_data.pop('sliders', [])
        slider_item = SliderItem.objects.create(**validated_data)
        
        for slider_data in sliders_data:
            Slider.objects.create(image=slider_data.get('image'), url=slider_data.get('url'), slider_item=slider_item)
            
        return slider_item
    
    def update(self, instance, validated_data):
        sliders_data = validated_data.pop('sliders', [])
        instance.title = validated_data.get('title', instance.title)
        instance.caption = validated_data.get('caption', instance.caption)
        instance.order = validated_data.get('order', instance.order)
        
        instance.save()
        
        for slider_data in sliders_data:
            slider_id = slider_data.get('id')
            if slider_id:
                slider_instance = Slider.objects.get(id=slider_id, slider_item=instance)
                slider_instance.image = slider_data.get('image', slider_instance.image)
                slider_instance.url = slider_data.get('url', slider_instance.url)
                slider_instance.save()
        
        return instance
    
# wishlist    
class WishlistSerializer(serializers.ModelSerializer):
    course_rating = serializers.SerializerMethodField()
    image = serializers.URLField(source='course.thumbnail_image', read_only=True)
    course_category = serializers.CharField(source='course.subcategory', read_only=True)
    learners_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Wishlist
        fields = ['id','course', 'course_category', 'image', 'learners_count', 'course_rating']

    def get_course_rating(self, obj):
        ratings = obj.course.ratings.all()
        if ratings.exists():
            return ratings.aggregate(average_rating=Avg('rating'))['average_rating']
        return None
    
    def get_learners_count(self, obj):
        return Enrollment.objects.filter(course=obj.course).count()

class CertificateSerializer(serializers.ModelSerializer):
    share_link = serializers.SerializerMethodField()
    
    class Meta:
        model = Certificate
        fields = ['id', 'title', 'description', 'certificate_file', 'created_at', 'share_link']
        
    def get_share_link(self, attr):
        return share_certificate_link(attr.id)