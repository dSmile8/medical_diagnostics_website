from django import forms
from django.conf import settings
from django.core.mail import send_mail


class StileFormMixin:
    """Формы"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


def send_new_password(email, new_password):
    send_mail(
        subject='Пароль изменен',
        message=f'Новый пароль {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
