from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import forms, BooleanField

from users.models import User


class StyleFormMixin:
    """
    A mixin class to style form fields with Bootstrap classes.

    This mixin class can be used in Django forms to apply Bootstrap classes to form fields.
    It iterates over the form fields and applies the appropriate Bootstrap class based on the field type.

    Attributes:
        None

    Methods:
        __init__(self, *args, **kwargs):
            Initializes the mixin class and applies Bootstrap classes to form fields.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class UserCreateForm(StyleFormMixin, UserCreationForm):
    """
        A Django form for creating a new user.

        This form inherits from StyleFormMixin and UserCreationForm. It is used to collect and validate
        user information during the user registration process.
    """

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')


class ProfileForm(StyleFormMixin, UserChangeForm):
    """
        A Django form for updating user profile information.

        This form inherits from StyleFormMixin and UserChangeForm. It is used to collect and validate
        user information during the user profile update process.
    """

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
