from django.forms import SelectDateWidget, DateTimeInput

from .models import *
from django import forms


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('doctor', 'date',)





