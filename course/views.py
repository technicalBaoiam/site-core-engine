from rest_framework import generics, viewsets, status, exceptions, views
from account.models import User
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .permissions import IsAdminOrReadOnly
from rest_framework.response import Response
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from datetime import timedelta
from django.http import StreamingHttpResponse, FileResponse

from .models import (
    Category, Subcategory, Course,
    Enrollment, Plan,
    #  Order, OrderItem,
    Rating, Instructor,
    Video, VideoPlaylist,
    Slider, SliderItem,
    Wishlist, Certificate
)

from .serializers import (
    CategorySerializer, SubcategorySerializer, CourseSerializer,
    OrderSerializer, PlanSerializer,
    RatingSerializer, EnrollmentSerializer, EnrollLimitSerializer, CourseEnrollmentSerializer,
    VideoSerializer, VideoPlaylistSerializer, InstructorSerializer,
    SliderItemSerializer,
    WishlistSerializer, CertificateSerializer
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

# featured courses
class FeaturedCourseList(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Course.objects.filter(featured=True)
    serializer_class = CourseSerializer       

class CoursePlanListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PlanSerializer

    def get_queryset(self):
        course_id = self.kwargs['pk']
        return Plan.objects.filter(course=course_id)
        
            
    
# class CourseDetailView(generics.RetrieveAPIView):
#     permission_classes = [AllowAny]
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
    
    # filter_backends = [SearchFilter]
    # search_fields = ['subcategory']

class CourseDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        course = self.get_object()  # Fetch the course details
        related_courses = self.get_related_courses(course)  # Fetch related courses

        # Prepare the response data
        response_data = {
            'course': CourseSerializer(course).data,
            'related_courses': CourseSerializer(related_courses, many=True).data,
        }
        return Response(response_data)

    def get_related_courses(self, course):
        # Fetch related courses based on the current course's category
        return Course.objects.filter(subcategory_id=course.subcategory_id).exclude(id=course.id)
# enrollment

class EnrollInCourseView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    # serializer_class = EnrollmentSerializer
    
    def get_serializer_class(self):
        if 'course_status' in self.request.query_params:
            return EnrollLimitSerializer
        return EnrollmentSerializer

    def get_queryset(self):
        user = self.request.user
        course_status = self.request.query_params.get('course_status')
        
        if not course_status:
            return Enrollment.objects.filter(student=user)
        
        # Validate the filter_type parameter using the serializer
        if course_status is None:
            raise exceptions.ValidationError({"course_status": "This field may not be null."})
        
        validation_serializer = CourseEnrollmentSerializer(data={'course_status': course_status})
        validation_serializer.is_valid(raise_exception=True)

        queryset = Enrollment.objects.filter(student=user)

        if course_status == 'ongoing':
            queryset = queryset.filter(completion_status__in=['pending', 'in_progress'])
        elif course_status == 'recent':
            queryset = queryset.filter(created_at__gte=now() - timedelta(days=30))
        elif course_status == 'completed':
            queryset = queryset.filter(completion_status='completed')
        elif course_status == 'enrolled':
            queryset = Enrollment.objects.filter(student=user, course__isnull=False)
        # elif course_status == 'not_enrolled':
        #     enrolled_course_ids = Enrollment.objects.filter(student=user).values_list('course_id', flat=True)
        #     queryset = Course.objects.exclude(id__in=enrolled_course_ids)
        else:
            queryset = Enrollment.objects.none()

        return queryset

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
    permission_classes = [IsAdminOrReadOnly]

class VideoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAdminOrReadOnly]

class VideoPlaylistListCreateView(generics.ListCreateAPIView):
    queryset = VideoPlaylist.objects.all()
    serializer_class = VideoPlaylistSerializer
    permission_classes = [IsAdminOrReadOnly]

class VideoPlaylistDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VideoPlaylist.objects.all()
    serializer_class = VideoPlaylistSerializer
    permission_classes = [IsAdminOrReadOnly]

class VideoDownloadView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        video_file = video.video_file.open()
        
        # a generator to stream the file(support large_file_size)
        def file_iterator(file, chunk_size=8192):
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                yield chunk
                
        response = StreamingHttpResponse(file_iterator(video_file), content_type='video/mp4')
        response['Content-Disposition'] = f'attachment; filename="{video.title}.mp4"'
        return response

class SliderItemView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SliderItem.objects.all()
    serializer_class = SliderItemSerializer
    parser_classes = [MultiPartParser, FormParser]

class SliderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SliderItem.objects.all()
    serializer_class = SliderItemSerializer
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

class WishlistAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Wishlist.objects.filter(user=user)
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class WishlistDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Wishlist.objects.filter(user=user)
    
class ShareLinkView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        course_slug = kwargs.get('slug')
        course = get_object_or_404(Course, slug=course_slug)
        
        shareable_link = f'http://localhost:8000/api/courses/{course.slug}/'  # need to change domain_name accordingly
        
        return Response({
            'course_name': course.title,
            'share_link': shareable_link
            })
        
# certificate
class CertificateListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    
    def get_queryset(self):
        user = self.request.user
        # queryset = super().get_queryset()        
        queryset = Certificate.objects.filter(user=user)
        return queryset

class CertificateDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = Certificate.objects.filter(user=user)
        return queryset
    
    def get_object(self):
        try:
            return super().get_object()
        except Certificate.DoesNotExist:
            return Response({'detail': 'Certificate not found'}, status=status.HTTP_404_NOT_FOUND)
    
class CertificateDownloadView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Certificate.objects.all()
    lookup_field = 'pk'
    
    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            file_path = instance.certificate_file.path
            response = FileResponse(open(file_path, 'rb'), as_attachment=True)  # can add file_content e.g. content_type='application/pdf'
            response['Content-Disposition'] = f'attachment; filename="{instance.certificate_file.name}"'
            return response
        except Certificate.DoesNotExist:
            return Response({'detail': 'Certificate not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)