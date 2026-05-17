from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
	queryset = Course.objects.all()
	serializer_class = CourseSerializer
	
	def get_permissions(self):
		if self.action == 'create':
			self.permission_classes = [IsAuthenticated, ~IsModerator]
		elif self.action in ['update', 'partial_update', 'retrieve']:
			self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
		elif self.action == 'destroy':
			self.permission_classes = [IsAuthenticated, IsOwner]
		elif self.action == 'list':
			self.permission_classes = [IsAuthenticated]
		return [permission() for permission in self.permission_classes]
	
	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)


class LessonListCreateView(generics.ListCreateAPIView):
	queryset = Lesson.objects.all()
	serializer_class = LessonSerializer
	permission_classes = [IsAuthenticated]
	
	def get_permissions(self):
		if self.request.method == 'POST':
			self.permission_classes = [IsAuthenticated, ~IsModerator]
		return [permission() for permission in self.permission_classes]
	
	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Lesson.objects.all()
	serializer_class = LessonSerializer
	
	def get_permissions(self):
		if self.request.method in ['PUT', 'PATCH']:
			self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
		elif self.request.method == 'DELETE':
			self.permission_classes = [IsAuthenticated, IsOwner]
		else:
			self.permission_classes = [IsAuthenticated]
		return [permission() for permission in self.permission_classes]