from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, forms, BooleanField
from django import forms
from users.models import User


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class UserCreateForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class ProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
