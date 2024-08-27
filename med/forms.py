from .models import *
from django import forms


class AppointmentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['doctor'].queryset = kwargs['initial']['doctor']

    class Meta:
        model = Appointment
        fields = ('doctor', 'date',)
