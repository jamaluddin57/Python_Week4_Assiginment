from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q

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

    def validate(self, data):
        """
        Perform bulk validation for both email and username to avoid duplicate queries.
        """
        email = data.get('email', None)
        username = data.get('username', None)
        user_id = self.instance.id if self.instance else None

        # If both email and username are provided, perform a bulk query
        if email or username:
            # Construct a query to check if either email or username already exists (excluding the current instance)
            filters = Q()
            if email:
                filters |= Q(email=email)
            if username:
                filters |= Q(username=username)
            
            # Exclude the current instance when updating
            if user_id:
                filters &= ~Q(id=user_id)

            # Check if any other user exists with the same email or username
            if User.objects.filter(filters).exists():
                if email and User.objects.filter(email=email).exclude(id=user_id).exists():
                    raise ValidationError({'email': 'Email is already taken.'})
                if username and User.objects.filter(username=username).exclude(id=user_id).exists():
                    raise ValidationError({'username': 'Username is already taken.'})

        return data

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
