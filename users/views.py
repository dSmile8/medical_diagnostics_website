from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy

from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView as BaseLoginView
from config import settings
from med.services import StileFormMixin
from users.forms import RegisterForm, UserForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'


"""    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.is_active = True
        new_user.set_password(form.cleaned_data['password1'])
        new_user.save()
        send_mail(
            subject='Поздравляем с регистрацией',
            message='Вы зарегистрировались на нашей платформе!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email,],
            fail_silently=False,
        )
        return super().form_valid(form)"""


class UserUpdateView(LoginRequiredMixin, UpdateView, StileFormMixin):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('med:index')

    def get_object(self, queryset=None):
        return self.request.user

