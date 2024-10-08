from django.db import models
from django.conf import settings
from django.utils.text import slugify

from ckeditor.fields import RichTextField


# instructor
class Instructor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    bio = models.TextField()
    email = models.EmailField(unique=True)
    hire_date = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
# Category
class Category(models.Model):
    name = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
# subcategory
class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# course                        
class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    course_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    program_overview = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name='courses', on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, related_name='courses', on_delete=models.CASCADE, null=True, blank=True)
    Instructor = models.ForeignKey('Instructor', related_name='courses', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    brochure_file = models.FileField(upload_to='brochures/', blank=True, null=True)
    thumbnail_image = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    # curriculum = models.TextField(blank=True, null=True)
    curriculum =RichTextField()

    # featured
    featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            print('slug not provided worked')
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     # Delete the brochure file from S3 if it exists
    #     if self.brochure_file:
    #         print('deteting thumbnail')
    #         self.brochure_file.delete(save=False)
    #     # Delete the thumbnail image from S3 if it exists
    #     if self.thumbnail_image:
    #         print('deteting thumbnail')
    #         self.thumbnail_image.delete(save=False)     
        
    #     super().delete(*args, **kwargs)

    def clear_files(self):
        """Clear files from S3 but keep the object."""
        print(self)
        if self.brochure_file:
            print('deteting brochure clear')
            self.brochure_file.delete(save=False)
            self.brochure_file = None  # Set to None in the model
        
        if self.thumbnail_image:
            print('deteting thumbnail clear')
            self.thumbnail_image.delete(save=False)
            self.thumbnail_image = None  # Set to None in the model
        
        self.save()  # Save the object without files

    def __str__(self):
        return self.title

# plan
class Plan(models.Model):
    PLAN_CHOICES = [
        ('plus', 'Plus'),
        ('premium', 'Premium'),
    ]
    course = models.ForeignKey('Course', related_name='plans', on_delete=models.CASCADE)
    name = models.CharField(max_length=10, choices=PLAN_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('course', 'name')

    def __str__(self):
        return f"{self.course.title} - {self.name} Plan"

# enrollment
class Enrollment(models.Model):

    TYPE_CHOICES = [
        ('demo', 'Demo'),
        ('full', 'Full Course'),
    ]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='full')
    enrollment_number = models.CharField(max_length=20, unique=True, blank=True)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='enrollments', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', related_name='enrollments', on_delete=models.CASCADE) 
    plan = models.ForeignKey('Plan', related_name='enrollments', on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_due = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) #remove null blank

    class Meta:
        unique_together = ('student', 'plan')  

    def __str__(self):
        return f"{self.enrollment_number} - {self.student.email} - {self.plan.name} Plan"

    def save(self, *args, **kwargs):

        if self.payment_due is None:
            print("enrollment payment_due save")
            self.payment_due = self.plan.price

        if not self.enrollment_number:
            self.enrollment_number = self.generate_enrollment_number()
        super().save(*args, **kwargs)

    def generate_enrollment_number(self):

        org_prefix = 'B1-IAM'
        course_code = self.course.course_code

        sequence_number = Enrollment.objects.filter(course=self.course).count() + 1
        return f"{org_prefix}-{course_code}-{sequence_number:03d}"    
        
    def get_plan_price(self):
        return self.plan.price    


# orders 
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]
    # enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, default=1)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE) 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # The total amount for the order
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    order_id = models.CharField(max_length=255, blank=True, null=True)
    signature = models.CharField(max_length=255, blank=True, null=True)

    # class Meta:
    #     unique_together = ('student', 'plan')  


    def __str__(self):
        return f"Order {self.id} - {self.status}"




# ratings 
class Rating(models.Model):
    course = models.ForeignKey(Course, related_name='ratings', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Rating {self.rating} for {self.course.title}"

# vidoes
class Video(models.Model):
    playlist = models.ForeignKey('VideoPlaylist', related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    url = models.URLField() 

    def __str__(self):
        return self.title

# playlist
class VideoPlaylist(models.Model):
    instructor = models.ForeignKey(Instructor, related_name='playlists', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

