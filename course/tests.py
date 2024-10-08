from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Course, Category, Subcategory

class CourseAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.featured_course = Course.objects.create(
            title="Featured Course",
            description="A featured course",
            featured=True
        )
        self.regular_course = Course.objects.create(
            title="Regular Course",
            description="A non-featured course",
            featured=False
        )
    
    def test_get_featured_courses(self):
        url = reverse('featured-courses')  # URL for featured courses
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one featured course
        self.assertEqual(response.data[0]['title'], self.featured_course.title)
        
class CourseCategoryAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Category 1", description="Category description")
        self.subcategory = Subcategory.objects.create(name="Subcategory 1", category=self.category)
        self.course = Course.objects.create(
            title="Test Course",
            description="A test course",
            category=self.category,
            subcategory=self.subcategory
        )

    def test_get_courses_by_category(self):
        url = reverse('course-list-create') + f'?category={self.category.id}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one course in the category
        self.assertEqual(response.data[0]['title'], self.course.title)

    def test_get_courses_by_subcategory(self):
        url = reverse('course-list-create') + f'?subcategory={self.subcategory.id}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one course in the subcategory
        self.assertEqual(response.data[0]['title'], self.course.title)

class CourseDetailAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            title="Test Course Detail",
            description="Detailed test course"
        )

    def test_get_course_detail(self):
        url = reverse('course-detail', args=[self.course.id])
        response = self.client.get(url)
        
        print(response.data)  # Print the response data for debugging

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['course']['title'], self.course.title)

class SearchCoursesAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Category 1", description="Category description")
        self.course_1 = Course.objects.create(
            title="Human Resource Management",
            description="A course about HR management",
            category=self.category
        )
        self.course_2 = Course.objects.create(
            title="Finance Management",
            description="A course about financial management",
            category=self.category
        )

    def test_search_courses_by_name(self):
        url = reverse('course-list-create') + f'?search=Human Resource'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one course should match the search term
        self.assertEqual(response.data[0]['title'], self.course_1.title)


class ListAllCoursesWithCategoriesAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.category_1 = Category.objects.create(name="Category 1", description="Category 1 description")
        self.category_2 = Category.objects.create(name="Category 2", description="Category 2 description")
        
        self.course_1 = Course.objects.create(
            title="Course in Category 1",
            description="A course in the first category",
            category=self.category_1
        )
        self.course_2 = Course.objects.create(
            title="Course in Category 2",
            description="A course in the second category",
            category=self.category_2
        )

    def test_list_all_courses_with_categories(self):
        url = reverse('category-list')  # URL for listing all categories and their courses
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two categories

        # Check if the correct courses are in the right categories
        self.assertEqual(len(response.data[0]['courses']), 1)
        self.assertEqual(response.data[0]['courses'][0]['title'], self.course_1.title)
        self.assertEqual(len(response.data[1]['courses']), 1)
        self.assertEqual(response.data[1]['courses'][0]['title'], self.course_2.title)
