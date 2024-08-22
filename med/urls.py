from .views import *
from django.urls import path
from med.apps import MedConfig

app_name = MedConfig.name

urlpatterns = [
    path('', ServicesListView.as_view(), name='index'),
    path("services/<int:pk>/", ServicesDetailView.as_view(), name="speciality_detail"),
    path('about/', DoctorsListView.as_view(), name='about'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),

    ]