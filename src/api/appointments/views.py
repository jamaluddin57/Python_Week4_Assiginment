from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Appointment
from .serializer import AppointmentSerializer, AppointmentReportSerializer
from django.db.models import Q, Count
from .permissions import IsAppointmentOwnerOrSuperuser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .filters import AppointmentReportFilter, AppointmentFilter
from django.core.cache import cache

class AppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AppointmentFilter

    def get_queryset(self):
        """
        Return the queryset of appointments based on user and query parameters.
        """
        user = self.request.user
        queryset = Appointment.objects.select_related('doctor', 'patient')
        condition = Q()

        if not user.is_superuser:
            condition &= Q(doctor=user) | Q(patient=user)

        return queryset.filter(condition)

    def list(self, request, *args, **kwargs):
        """
        Override list method to implement caching with respect to filters and pagination.
        """
        query_params = request.query_params
        doctor_name = query_params.get('doctor_name')
        date = query_params.get('date')
        is_completed = query_params.get('is_completed')

        # Generate cache key based on filter parameters and pagination
        pagination_key = f"limit={query_params.get('limit', 10)}&offset={query_params.get('offset', 0)}"
        cache_key = f"appointments:{pagination_key}"

        if doctor_name or date or is_completed:
            return super().list(request, *args, **kwargs)
        
        # Check if the result is already cached
        cached_response = cache.get(cache_key)
        if cached_response:
            return Response(cached_response)

        # Get the result from DB if not cached
        response = super().list(request, *args, **kwargs)

        cache.set(cache_key, response.data, timeout=300)  # Cache for 5 minutes

        return response



class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete an appointment.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsAppointmentOwnerOrSuperuser]
    lookup_field = 'id'
    queryset = Appointment.objects.all()

    def delete(self, request, *args, **kwargs):
        """
        Override delete method to clear the cache after deleting an appointment.
        """
        response = super().delete(request, *args, **kwargs)
        cache.delete_pattern('appointments:*')
        return response


class AppointmentReportView(generics.ListAPIView):
    """
    View to generate a report of appointments.
    """
    permission_classes=[IsAdminUser]
    serializer_class = AppointmentReportSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class=AppointmentReportFilter

    def get_queryset(self):
        """
        Return the queryset of appointments grouped by date.
        """
        return Appointment.objects.select_related('doctor', 'patient').values('scheduled_at__date').annotate(count=Count('id'))

class AppointmentCreateView(generics.CreateAPIView):
    """
    View to create appointments.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [IsAdminUser]