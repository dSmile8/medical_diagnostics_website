from .views import *
from django.urls import path
from med.apps import MedConfig

app_name = MedConfig.name

urlpatterns = [
    path('', ServicesListView.as_view(), name='index1'),
    path("services/<int:pk>/", ServicesDetailView.as_view(), name="speciality_detail")
    ]