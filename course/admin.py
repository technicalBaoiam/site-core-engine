from django.contrib import admin
# Register your models here.
from .models import Category, Subcategory, Course, Plan, Order, Enrollment,  Instructor, Rating,  Video, VideoPlaylist
from course.blogs.models import Blog, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'label', 'description', 'created_at')
    search_fields = ('name', 'label')

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('category',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'subcategory',
                    #'brochure_file', 'thumbnail_image', 'curriculum'
                    )
    search_fields = ('title', 'description')
    list_filter = ('category', 'subcategory')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('course', 'rating', 'comment')
    search_fields = ('course', 'comment')
    list_filter = ('course', 'rating')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'created_at')
    search_fields = ('student__email', 'course__title')
    list_filter = ('course','plan')

@admin.register(Plan)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ( 'course', 'name', 'price')
    list_filter = ('course','name')

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'hire_date')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('hire_date',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'playlist', 'url')
    search_fields = ('title', 'playlist__title', 'url')
    list_filter = ('playlist',)

@admin.register(VideoPlaylist)
class VideoPlaylistAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'description')
    search_fields = ('title', 'description')
    list_filter = ('instructor',)

admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Order)

