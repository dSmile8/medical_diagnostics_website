from .views import *
from django.urls import path
from med.apps import MedConfig

app_name = MedConfig.name

urlpatterns = [
    path('', ServicesListView.as_view(), name='index'),
    path("services/<int:pk>/", ServicesDetailView.as_view(), name="speciality_detail"),
    path('about/', DoctorsListView.as_view(), name='about'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),

    path('appointments_create/', AppointmentCreateView.as_view(), name='appointments_create'),
    path('appointments_my/', AppointmentUserListView.as_view(), name='appointments_my'),
    path('appointments_archive/', AppointmentArchiveListView.as_view(), name='appointments_archive'),
    path('appointments_cancel/<int:pk>/', AppointmentCancelView.as_view(), name='appointments_cancel'),

    ]