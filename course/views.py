from rest_framework import generics, viewsets, status
from account.models import User
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter
from .permissions import IsAdminOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# from rest_framework.generics import ListAPIView

from .models import (
    Category, Subcategory, Course,
    Enrollment, Plan,
    #  Order, OrderItem,
    Rating, Instructor,
    Video, VideoPlaylist
)
from .serializers import (
    CategorySerializer, SubcategorySerializer, CourseSerializer,
    OrderSerializer,
    RatingSerializer, EnrollmentSerializer, InstructorSerializer,
    VideoSerializer, VideoPlaylistSerializer
)

# category

class CategoryViewSet(viewsets.ModelViewSet):
    
        permission_classes = [IsAdminOrReadOnly]
        queryset = Category.objects.all()
        serializer_class = CategorySerializer
    
class SubcategoryViewSet(viewsets.ModelViewSet):
    
        permission_classes = [IsAdminOrReadOnly]
        queryset = Subcategory.objects.all()
        serializer_class = SubcategorySerializer


# course

class CourseListCreateView(generics.ListCreateAPIView):
    
    permission_classes = [IsAdminOrReadOnly]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    # filter_backends = [SearchFilter]
    # search_fields = ['title', 'subcategory']
    
    def get_queryset(self):
        queryset = Course.objects.all()
        category = self.request.query_params.get('category', None)
        subcategory = self.request.query_params.get('subcategory', None)
        search = self.request.query_params.get('search', None)

        if category:
               queryset = queryset.filter(category_id=category)
            
        if subcategory:
               queryset = queryset.filter(subcategory_id=subcategory)

        if search:
               queryset = queryset.filter(title__icontains=search)
        # except Exception as e:
        #        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        return queryset
    
class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    # filter_backends = [SearchFilter]
    # search_fields = ['subcategory']

# enrollment

class EnrollInCourseView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)

    # its not needed to do this way ListAPIView
    # def post(self, request, *args, **kwargs):
    #     course_id = request.data.get('course_id')
    #     plan_name = request.data.get('plan_name')
        
    #     course = get_object_or_404(Course, id=course_id)
    #     plan = get_object_or_404(Plan, course=course, name=plan_name)
        
    #     if Enrollment.objects.filter(student=request.user, course=course, plan=plan).exists():
    #         return Response({'error': 'Already enrolled in this course with this plan'}, status=status.HTTP_400_BAD_REQUEST)
        
    #     enrollment = Enrollment.objects.create(
    #         student=request.user,
    #         course=course,
    #         plan=plan
    #     )
        
    #     serializer = self.get_serializer(enrollment)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

# orders and payments

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    # queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        order = serializer.save()
        return Response(serializer.data)



# ratings

class RatingListCreateView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class RatingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer



# Instructor

class InstructorListCreateView(generics.ListCreateAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer

class InstructorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer

# videos

class VideoListCreateView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class VideoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class VideoPlaylistListCreateView(generics.ListCreateAPIView):
    queryset = VideoPlaylist.objects.all()
    serializer_class = VideoPlaylistSerializer

class VideoPlaylistDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VideoPlaylist.objects.all()
    serializer_class = VideoPlaylistSerializer



