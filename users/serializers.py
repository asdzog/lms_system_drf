from rest_framework import serializers
from users.models import Payment, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]

    def create(self, validated_data):
        user = User(email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user


class PaymentSerializer(serializers.ModelSerializer):
    payment_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
