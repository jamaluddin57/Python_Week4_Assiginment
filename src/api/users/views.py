from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User
from .serializers import UserSerializer
from .permissions import IsOwnerOrAdmin
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

class UserListView(generics.ListAPIView):
    """
    API view to retrieve a list of users based on their role.
    Only accessible by admin users.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        """
        Override the get_queryset method to filter users by role.
        """
        user_type = self.kwargs['user_type'].lower()
        if user_type not in [User.DOCTOR,User.PATIENT,User.ADMIN]:
            raise ObjectDoesNotExist("Role not found")
        return User.objects.filter(role=user_type)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a user by ID.
    Accessible by authenticated users who are either the owner or an admin.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    
    def get_object(self):
        """
        Override the get_object method to return the user based on the user_type.
        """
        user_type = self.kwargs['user_type'].lower()
        return User.objects.get(id=self.kwargs['id'], role=user_type)
    
    def get_queryset(self):
        """
        Override the get_queryset method to filter users by role.
        """
        return User.objects.filter(role=self.kwargs['user_type'].lower())
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class RegisterView(generics.CreateAPIView):
    """
    API view to register a new user based on the user_type in the URL.
    Only accessible by admin users.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        """
        Override the perform_create method to set the user's role and password.
        """
        user_type = self.kwargs.get('user_type').lower()  # Get user_type from the URL
        if user_type not in [User.DOCTOR, User.PATIENT]:
            raise serializers.ValidationError("Invalid user type provided.")
        
        # Set the role based on the user_type in the URL
        serializer.save(role=user_type)
