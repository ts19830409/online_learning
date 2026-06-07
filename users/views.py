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
from lms.services import create_stripe_product, create_stripe_price, create_stripe_session
from django.conf import settings


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


class PaymentCreateView(APIView):
	def post(self, request):
		course_id = request.data.get('course_id')
		course = get_object_or_404(Course, pk=course_id)
		
		# Создаём продукт и цену в Stripe
		stripe_product_id = create_stripe_product(course)
		stripe_price_id = create_stripe_price(stripe_product_id, float(course.price)) if hasattr(course,
		                                                                                         'price') else create_stripe_price(
			stripe_product_id, 1000)
		
		# Создаём сессию оплаты
		session_id, payment_url = create_stripe_session(
			stripe_price_id,
			success_url='http://127.0.0.1:8000/',
			cancel_url='http://127.0.0.1:8000/',
		)
		
		# Сохраняем платёж в базе
		payment = Payment.objects.create(
			user=request.user,
			course=course,
			amount=course.price if hasattr(course, 'price') else 1000,
			payment_method='transfer',
			stripe_session_id=session_id,
		)
		
		return Response({
			'payment_id': payment.pk,
			'payment_url': payment_url,
		})