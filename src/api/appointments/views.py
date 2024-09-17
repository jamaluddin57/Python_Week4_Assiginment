from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import Appointment
from .serializer import AppointmentSerializer, AppointmentReportSerializer
from django.db.models import Q, Count
from .permissions import IsAppointmentOwnerOrSuperuser
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .filters import AppointmentReportFilter, AppointmentFilter

class AppointmentListView(generics.ListAPIView):
    """
    View to list and create appointments.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class=AppointmentFilter
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


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete an appointment.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsAppointmentOwnerOrSuperuser]
    lookup_field = 'id'
    queryset = Appointment.objects.all()


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