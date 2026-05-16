from rest_framework import generics
from users.models import User
from users.serializers import UserSerializer

from users.models import Payment
from users.serializers import PaymentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

class ProfileView(generics.RetrieveUpdateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	
class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date']