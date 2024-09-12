from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    
    # category and subcategory
    CategoryViewSet, SubcategoryViewSet,
    
    # course
    CourseListCreateView, CourseDetailView,
   
    # enrollment
    EnrollInCourseView,   
    
    # rating
    RatingListCreateView, RatingDetailView,

    # instructor
    InstructorListCreateView, InstructorDetailView,

    # videos 
    VideoListCreateView, VideoDetailView,
    VideoPlaylistListCreateView, VideoPlaylistDetailView
)


from course.blogs.views import (

    # Blogs
    BlogCreateListView, BlogDetailView,   
    # comments
    CommentCreateView, CommentDetailView
    
    )

from .orders.order_views import OrderListCreateView, VerifyPaymentView, DemoSessionOrderView #OrderItemListCreateView

# for categories route

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubcategoryViewSet)



urlpatterns = [
  
    # Category Subcategory orders and orderitems URLs included
    path('', include(router.urls)),

    # Course URLs
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),

    # Enrollment
    path('enroll/', EnrollInCourseView.as_view(), name='enroll-in-course'),

      # Order URLs
    path('orders/', OrderListCreateView.as_view(), name='order-create'),
    #   demo session order
    path('orders/demo-session/', DemoSessionOrderView.as_view(), name='demo-session-order'),
    # Verify Payment URL
    path('orders/verify_payment/', VerifyPaymentView.as_view(), name='verify-payment'),


    # Blogs and Comments URLs
    path('blogs/', BlogCreateListView.as_view(), name="blog-list-create"),
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name="blog-detail"),
    path('blogs/<int:blog_post_id>/comment/', CommentCreateView.as_view(), name="comment-list-create"),
    path('blogs/<int:blog_post_id>/comment/<int:pk>/', CommentDetailView.as_view(), name="comment-detail"),

   
# to be completed in future ( ratings/instructors/videos )

    # Rating URLs
    path('ratings/', RatingListCreateView.as_view(), name='rating-list-create'),
    path('ratings/<int:pk>/', RatingDetailView.as_view(), name='rating-detail'),

    # Instructor URLs
    path('instructors/', InstructorListCreateView.as_view(), name='instructor-list-create'),
    path('instructors/<int:pk>/', InstructorDetailView.as_view(), name='instructor-detail'),

    # Video URLs
    path('videos/', VideoListCreateView.as_view(), name='video-list-create'),
    path('videos/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),

    # Video Playlist URLs
    path('playlists/', VideoPlaylistListCreateView.as_view(), name='playlist-list-create'),
    path('playlists/<int:pk>/', VideoPlaylistDetailView.as_view(), name='playlist-detail'),
]
