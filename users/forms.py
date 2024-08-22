from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class RegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',  'email', 'phone', 'password1', 'password2')


class UserForm(StyleFormMixin, UserChangeForm):
    pass

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()
