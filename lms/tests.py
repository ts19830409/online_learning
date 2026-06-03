from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from lms.models import Course, Lesson
from users.models import Subscription


class LessonCRUDTests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='test@test.ru', password='test123')
		self.course = Course.objects.create(title='Test Course', owner=self.user)
		self.lesson_data = {
			'title': 'Test Lesson',
			'description': 'Test Description',
			'video_link': 'https://youtube.com/watch?v=test',
			'course': self.course.pk
		}
		self.client.force_authenticate(user=self.user)
	
	def test_create_lesson(self):
		response = self.client.post(reverse('lesson-list-create'), self.lesson_data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
	
	def test_get_lesson_list(self):
		Lesson.objects.create(title='Test', course=self.course, owner=self.user)
		response = self.client.get(reverse('lesson-list-create'))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
	
	def test_update_lesson(self):
		lesson = Lesson.objects.create(title='Test', course=self.course, owner=self.user)
		response = self.client.patch(reverse('lesson-detail', args=[lesson.pk]), {'title': 'Updated'})
		self.assertEqual(response.status_code, status.HTTP_200_OK)
	
	def test_delete_lesson(self):
		lesson = Lesson.objects.create(title='Test', course=self.course, owner=self.user)
		response = self.client.delete(reverse('lesson-detail', args=[lesson.pk]))
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
	
	def test_invalid_video_link(self):
		data = self.lesson_data.copy()
		data['video_link'] = 'https://google.com'
		response = self.client.post(reverse('lesson-list-create'), data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SubscriptionTests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='test@test.ru', password='test123')
		self.course = Course.objects.create(title='Test Course', owner=self.user)
		self.client.force_authenticate(user=self.user)
	
	def test_subscribe(self):
		response = self.client.post(reverse('subscription'), {'course_id': self.course.pk})
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['message'], 'Подписка добавлена')
		self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())
	
	def test_unsubscribe(self):
		Subscription.objects.create(user=self.user, course=self.course)
		response = self.client.post(reverse('subscription'), {'course_id': self.course.pk})
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['message'], 'Подписка удалена')
		self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())