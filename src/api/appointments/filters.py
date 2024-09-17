from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Appointment

class AppointmentReportFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='scheduled_at', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='scheduled_at', lookup_expr='lte')
    doctor_name = filters.CharFilter(method='filter_doctor_name')
    is_completed = filters.BooleanFilter(field_name='is_completed')

    class Meta:
        model = Appointment
        fields = ['start_date', 'end_date', 'doctor_name', 'is_completed']

    def filter_doctor_name(self, queryset, name, value):
        return queryset.filter(
            Q(doctor__first_name__icontains=value) | Q(doctor__last_name__icontains=value)
        )

class AppointmentFilter(filters.FilterSet):
    date = filters.DateFilter(field_name='scheduled_at__date') 
    doctor_name = filters.CharFilter(method='filter_doctor_name')
    is_completed = filters.BooleanFilter(field_name='is_completed')

    class Meta:
        model = Appointment
        fields = ['date', 'doctor_name', 'is_completed']
    
    def filter_doctor_name(self, queryset, name, value):
        return queryset.filter(
            Q(doctor__first_name__icontains=value) | Q(doctor__last_name__icontains=value)
        )