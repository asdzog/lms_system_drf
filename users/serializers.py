from rest_framework import serializers
from users.models import Payment, User
from courses import services


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

    @staticmethod
    def get_stripe_url(instance: Payment):
        product = services.create_stripe_product(instance.paid_course.course_name)
        price_id = services.create_stripe_price(instance.paid_course.price, product['name'])
        url, session_id = services.create_stripe_session(price_id)
        return url, session_id

    class Meta:
        model = Payment
        fields = '__all__'
