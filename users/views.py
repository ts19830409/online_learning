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
import stripe

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
		amount = float(course.price) if course.price else 0
		
		# Создаём продукт и цену в Stripe
		stripe_product_id = create_stripe_product(course)
		stripe_price_id = create_stripe_price(stripe_product_id, amount)
		
		# Создаём сессию оплаты
		session_id, payment_url = create_stripe_session(
			stripe_price_id,
			success_url='http://127.0.0.1:8000/',
			cancel_url='http://127.0.0.1:8000/',
		)
		
		# Сохраняем платёж
		payment = Payment.objects.create(
			user=request.user,
			course=course,
			amount=amount,
			payment_method='transfer',
			stripe_session_id=session_id,
			stripe_product_id=stripe_product_id,
			stripe_price_id=stripe_price_id,
			payment_url=payment_url,
			status='pending',
		)
		
		return Response({
			'payment_id': payment.pk,
			'payment_url': payment_url,
			'status': payment.status,
		})


class PaymentStatusView(APIView):
	def get(self, request, payment_id):
		payment = get_object_or_404(Payment, pk=payment_id)
		
		if not payment.stripe_session_id:
			return Response({'error': 'Нет ID сессии Stripe'}, status=400)
		
		try:
			session = stripe.checkout.Session.retrieve(payment.stripe_session_id)
			payment.status = session.payment_status
			payment.save()
			return Response({
				'payment_id': payment.pk,
				'status': payment.status,
				'amount': str(payment.amount),
			})
		except stripe.error.StripeError as e:
			return Response({'error': str(e)}, status=400)


