import random
import secrets
import string

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse

from django.views.generic import CreateView, UpdateView, ListView

from config.settings import EMAIL_HOST_USER
from users.forms import UserCreateForm, ProfileForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Для подтверждения регистрации на сайте {host} перейдите по следующей ссылке:'
                    f'{url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email])
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class ProfileView(UserPassesTestMixin, UpdateView):
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile')
    template_name = 'users/profile.html'

    def test_func(self):
        # if self.get_object().is_doctor and self.request.user.is_superuser:
        #     return True
        # if not self.get_object().is_doctor and self.request.user == self.get_object():
        #     return True
        # return self.request.user.is_superuser

        if self.request.user == self.get_object() or self.request.user.is_superuser:
            return True

    def get_object(self, queryset=None):
        return self.request.user


def reset_password(request):
    context = {
        "success_message": "Пароль успешно сброшен. Новый пароль был отправлен на ваш адрес электронной почты.",
    }
    if request.method == "POST":
        email = request.POST.get("email")
        user = get_object_or_404(User, email=email)
        characters = string.ascii_letters + string.digits
        characters_list = list(characters)
        random.shuffle(characters_list)
        password = "".join(characters_list[:10])
        user.set_password(password)
        user.save()
        send_mail(
            subject="Восстановление пароля",
            message=f"Здравствуйте, вы запрашивали обновление пароля. Ваш новый пароль: {password}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return render(request, "users/reset_password.html", context)
    else:
        return render(request, "users/reset_password.html")


class DoctorCreateView(UserPassesTestMixin, CreateView):
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.instance.is_doctor = True
        form.instance.is_staff = True
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser


class ProfileDeleteView(UserPassesTestMixin, UpdateView):
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile')
    template_name = 'users/profile.html'

    def test_func(self):
        # if self.get_object().is_doctor or self.request.user.is_superuser:
        #     return True
        # if not self.get_object().is_doctor and self.request.user == self.get_object():
        #     return True
        # return self.request.user.is_superuser

        if self.request.user == self.get_object() or self.request.user.is_superuser:
            return True


class UsersListView(ListView):
    model = User
    template_name = 'med/about.html'

    def get_queryset(self):
        return User.objects.filter(is_doctor=True)
