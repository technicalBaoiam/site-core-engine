from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    
    # category and subcategory
    CategoryViewSet, SubcategoryViewSet,
    
    # course
    CourseListCreateView, CourseDetailView, CoursePlanListView, FeaturedCourseList, ShareLinkView,
   
    # enrollment
    EnrollInCourseView,  
    
    # rating
    RatingListCreateView, RatingDetailView,

    # instructor
    InstructorListCreateView, InstructorDetailView,

    # videos 
    VideoListCreateView, VideoDetailView,
    VideoPlaylistListCreateView, VideoPlaylistDetailView, VideoDownloadView,
    
    SliderItemDetailView, SliderItemView,
    
    WishlistAPIView, WishlistDeleteView,
    
    CertificateListView, CertificateDownloadView, CertificateDetailView
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
  
    # Category Subcategory orders and orderitems URLs included although not necessary to include
    path('', include(router.urls)),

    # Course URLs
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<slug:slug>/', CourseDetailView.as_view(), name='course-detail'),
    path('courses/featured/', FeaturedCourseList.as_view(), name='featured-courses'),
    path('courses/share/<slug:slug>/', ShareLinkView.as_view(), name='share-course-link'),


    # Enrollment
    path('enroll/', EnrollInCourseView.as_view(), name='enroll-in-course'),

    # Plan
    path('course/<int:pk>/plan/', CoursePlanListView.as_view(), name='course-plan'),


    # Order URLs
    path('orders/', OrderListCreateView.as_view(), name='order-create'),
    # Demo session order
    path('orders/demo-session/', DemoSessionOrderView.as_view(), name='demo-session-order'),
    # Verify Payment URL
    path('orders/verify_payment/', VerifyPaymentView.as_view(), name='verify-payment'),


    # Blogs and Comments URLs
    path('blogs/', BlogCreateListView.as_view(), name="blog-list-create"),
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name="blog-detail"),
    path('blogs/<int:blog_post_id>/comment/', CommentCreateView.as_view(), name="comment-list-create"),
    path('blogs/<int:blog_post_id>/comment/<int:pk>/', CommentDetailView.as_view(), name="comment-detail"),

    # Rating URLs
    path('ratings/', RatingListCreateView.as_view(), name='rating-list-create'),
    path('ratings/<int:pk>/', RatingDetailView.as_view(), name='rating-detail'),

    # Instructor URLs
    path('instructors/', InstructorListCreateView.as_view(), name='instructor-list-create'),
    path('instructors/<int:pk>/', InstructorDetailView.as_view(), name='instructor-detail'),

    # Video URLs
    path('videos/', VideoListCreateView.as_view(), name='video-list-create'),
    path('videos/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
    path('videos/<int:pk>/download/', VideoDownloadView.as_view(), name='video-download'),

    # Video Playlist URLs
    path('playlists/', VideoPlaylistListCreateView.as_view(), name='playlist-list-create'),
    path('playlists/<int:pk>/', VideoPlaylistDetailView.as_view(), name='playlist-detail'),
    
    # slider
    path('slider/', SliderItemView.as_view(), name='slider-list-create'),
    path('slider/<int:pk>/', SliderItemDetailView.as_view(), name='slider-detail'),
    
    # wishlist URLs
    path('wishlist/', WishlistAPIView.as_view(), name='wishlist-list-create'),
    path('wishlist/<int:pk>/', WishlistDeleteView.as_view(), name='wishlist-delete'),
    
    # certificate urls
    path('certificate/', CertificateListView.as_view(), name='certificate-list'),
    path('certificate/<int:pk>/', CertificateDetailView.as_view(), name='get_certificate'),
    path('certificate/download/<int:pk>/', CertificateDownloadView.as_view(), name='download_certificate'),
]
