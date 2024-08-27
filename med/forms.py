
from django import forms

from med.models import Appointment


class AppointmentForm(forms.ModelForm):
    """
       Form for managing appointments.

       This form is used to create and update appointment records in the database.
       It inherits from Django's ModelForm and is specifically designed for the Appointment model.
    """

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['doctor'].queryset = kwargs['initial']['doctor']

    class Meta:
        model = Appointment
        fields = ('doctor', 'date',)
