from users.views import UsersListView
from .views import *
from django.urls import path
from med.apps import MedConfig

app_name = MedConfig.name





urlpatterns = [
    path('', ServicesListView.as_view(), name='index'),
    path("services/<int:pk>/", ServicesDetailView.as_view(), name="speciality_detail"),
    path('about/', UsersListView.as_view(), name='about'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    
    path('making_an_appointment/', ServicesMakingListView.as_view(), name='making_an_appointment'),
    path('appointments_create/<int:pk>/', AppointmentCreateView.as_view(), name='appointments_create'),
    path('appointments_my/', AppointmentUserListView.as_view(), name='appointments_my'),
    path('appointments_archive/', AppointmentArchiveListView.as_view(), name='appointments_archive'),
    path('appointments_cancel/<int:pk>/', AppointmentCancelView.as_view(), name='appointments_cancel'),

    ]