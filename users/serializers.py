from rest_framework import serializers
from users.models import User
from users.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'first_name', 'last_name', 'payments']
        read_only_fields = ['id', 'email']