from rest_framework import generics
from users.models import User
from users.serializers import UserSerializer
from users.models import Payment
from users.serializers import PaymentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from lms.models import Course
from users.models import Subscription
from rest_framework.views import APIView
from rest_framework.response import Response

class ProfileView(generics.RetrieveUpdateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer


class PaymentListView(generics.ListAPIView):
	queryset = Payment.objects.all()
	serializer_class = PaymentSerializer
	filter_backends = [DjangoFilterBackend, OrderingFilter]
	filterset_fields = ['course', 'lesson', 'payment_method']
	ordering_fields = ['payment_date']


class RegisterView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [AllowAny]


class SubscriptionView(APIView):
	def post(self, request):
		user = request.user
		course_id = request.data.get('course_id')
		course = get_object_or_404(Course, pk=course_id)
		
		subscription = Subscription.objects.filter(user=user, course=course)
		
		if subscription.exists():
			subscription.delete()
			message = 'Подписка удалена'
		else:
			Subscription.objects.create(user=user, course=course)
			message = 'Подписка добавлена'
		
		return Response({'message': message})
