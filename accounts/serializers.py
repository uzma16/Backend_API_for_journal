from .models import User
import phonenumbers
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'full_name', 'date_of_birth', 'gender', 'picture', 'phone_number', 'username']

    def get_phone_number(self, instance):
        phone = instance.phone
        if phone is not None:
            country_code = phonenumbers.parse(phone).country_code
            phone_number = phonenumbers.parse(phone).national_number
            return f'+{country_code},{phone_number}'
        return 'null'
