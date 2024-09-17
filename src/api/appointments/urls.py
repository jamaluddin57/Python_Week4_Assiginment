from django.urls import path
from .views import AppointmentListView, AppointmentDetailView, AppointmentReportView, AppointmentCreateView
urlpatterns = [
    # List appointments
    path('list/', AppointmentListView.as_view(), name='appointment-list'),

    # Retrieve details of an appointment by id
    path('<int:id>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    # Generate a report of appointments
    path('report/', AppointmentReportView.as_view(), name='appointment-report'),

    path('create/', AppointmentCreateView.as_view(), name='appointment-create'),
]
