from django import forms
from django.conf import settings
from django.core.mail import send_mail


class StileFormMixin:
    """
    A mixin class for Django forms that adds a common style to all form fields.

    Attributes:
    -----------
    fields : dict
        A dictionary containing the form fields.

    Methods:
    --------
    __init__(self, *args, **kwargs)
        Initializes the form with the provided arguments and applies a common style to all form fields.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


def send_new_password(email, new_password):
    """
    Sends a new password to the specified email address.

    Parameters:
    -----------
    email : str
        The email address to which the new password will be sent.
    new_password : str
        The new password to be sent to the email address.

    Returns:
    --------
    None
        This function does not return any value. It sends an email with the new password.
    """
    send_mail(
        subject='Пароль изменен',
        message=f'Новый пароль {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
