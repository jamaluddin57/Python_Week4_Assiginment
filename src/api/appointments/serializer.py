from rest_framework import serializers
from .models import Appointment
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from django.db import transaction
from django.core.cache import cache

User = get_user_model()

class UserSummarySerializer(serializers.ModelSerializer):
    """
    Serializer for displaying a summary of user details.
    """
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']

class AppointmentSerializer(serializers.ModelSerializer):
    doctor = UserSummarySerializer(read_only=True)
    patient = UserSummarySerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role=User.DOCTOR), write_only=True, source='doctor')
    patient_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, source='patient')

    class Meta:
        model = Appointment
        fields = ['id', 'scheduled_at', 'is_completed', 'doctor', 'patient', 'doctor_id', 'patient_id']
        read_only_fields = ('created_at', 'updated_at')
        extra_kwargs = {'scheduled_at': {'required': True}}

    def validate_scheduled_at(self, value):
        doctor_id = self.initial_data.get('doctor_id')

        if doctor_id:
            doctor = User.objects.filter(id=doctor_id).first()
        else:
            doctor = self.instance.doctor if self.instance else None

        if doctor and Appointment.objects.filter(doctor=doctor, scheduled_at=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("Doctor already has an appointment at this time.")

        return value

    def validate(self, data):
        # Only validate fields if creating a new instance
        if not self.instance:
            if 'scheduled_at' not in data:
                raise serializers.ValidationError({"scheduled_at": "This field is required."})
            if 'doctor_id' not in self.initial_data:
                raise serializers.ValidationError({"doctor_id": "This field is required."})
            if 'patient_id' not in self.initial_data:
                raise serializers.ValidationError({"patient_id": "This field is required."})
        return data

    @transaction.atomic
    def create(self, validated_data):
        cache.delete_pattern('appointment:*')  # Clear the cache
        return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        cache.delete_pattern('appointment:*')  # Clear the cache
        return super().update(instance, validated_data)

    
class AppointmentReportSerializer(serializers.Serializer):
    """
    Serializer for appointment counts by date, including hyperlinks to filtered appointments.
    """
    date = serializers.DateField(source='scheduled_date')
    count = serializers.IntegerField()
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        """
        Builds the URL for the list view, including the date, doctor_name, and status as query parameters.
        """
        request = self.context.get('request')
        base_url = reverse('appointment-list', request=request)
        query_params = {
            'date': obj['scheduled_date'],
            'doctor_name': request.query_params.get('doctor_name', ''),
            'is_completed': request.query_params.get('is_completed', '')
        }
        return f"{base_url}?date={query_params['date']}&doctor_name={query_params['doctor_name']}&is_completed={query_params['is_completed']}"

    def to_representation(self, instance):
        """
        Customize the representation of the instance.
        """
        representation = super().to_representation(instance)
        request = self.context.get('request')
        representation['filters'] = {
            'doctor_name': request.query_params.get('doctor_name', ''),
            'status': request.query_params.get('status', '')
        }
        return representation
