from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from django.db import transaction

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, with conditional fields.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'phone_number', 
                  'date_of_birth', 'gender', 'address', 'specialization', 'role']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},  # Password not required for update
            'specialization': {'required': False},  # Specialization not required for non-doctors
        }

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request', None)

        if request:
            user_type = request.parser_context['kwargs'].get('user_type').lower()
            if user_type != User.DOCTOR:
                # If the user is not a doctor, remove the specialization field
                self.fields.pop('specialization', None)

    def validate_email(self, value):
        if not self.instance and User.objects.filter(email=value).exists():
            raise ValidationError('Email is already taken.')
        if self.instance and User.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise ValidationError('Email is already taken.')
        return value

    def validate_username(self, value):
        if not self.instance and User.objects.filter(username=value).exists():
            raise ValidationError('Username is already taken.')
        if self.instance and User.objects.filter(username=value).exclude(id=self.instance.id).exists():
            raise ValidationError('Username is already taken.')
        return value

    @transaction.atomic
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    @transaction.atomic
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        return super().update(instance, validated_data)
