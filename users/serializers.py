from rest_framework import serializers
from users.models import User
from users.models import Payment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'first_name', 'last_name']
        read_only_fields = ['id', 'email']
        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'