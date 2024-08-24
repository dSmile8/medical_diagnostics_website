from .models import *
from django import forms


class AppointmentForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.get('user')
    #     super().__init__(*args, **kwargs)
    #
    # def save(self):
    #     self.instance.user = self.user
    #     return super().save()

    class Meta:
        model = Appointment
        fields = ('services', 'doctor', 'date',)
        # exclude = ('user' ,)
