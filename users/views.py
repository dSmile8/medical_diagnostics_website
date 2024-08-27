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
    """
        A view for updating user profile.

        Attributes:
        model: The model to be updated, in this case, User.
        form_class: The form class for updating the user profile, ProfileForm.
        success_url: The URL to redirect to after successful profile update.
        template_name: The template to render for the profile view.

        Methods:
        test_func: Checks if the current user is the same as the profile being viewed or if the user is a superuser.
        get_object: Returns the user object for the profile being viewed.
        """

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
    """
    Verifies the user's email by activating their account.

    Parameters:
    request (HttpRequest): The request object containing the user's token.
    token (str): The unique token sent to the user's email for verification.

    Returns:
    HttpResponseRedirect: Redirects the user to the login page upon successful email verification.
    """
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class ProfileView(UserPassesTestMixin, UpdateView):
    """
    A view for updating user profile.

    Attributes:
    model: The model to be updated, in this case, User.
    form_class: The form class for updating the user profile, ProfileForm.
    success_url: The URL to redirect to after successful profile update.
    template_name: The template to render for the profile view.

    Methods:
    test_func: Checks if the current user is the same as the profile being viewed or if the user is a superuser.
    get_object: Returns the user object for the profile being viewed.
    """

    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile')
    template_name = 'users/profile.html'

    def test_func(self):
        if self.request.user == self.get_object() or self.request.user.is_superuser:
            return True

    def get_object(self, queryset=None):
        return self.request.user


def reset_password(request):
    """
    Handles the password reset functionality for users.

    Parameters:
    request (HttpRequest): The request object containing the user's email.

    Returns:
    HttpResponse: Renders the reset password template with a success message if the email is found and a new password is sent.
                  Otherwise, renders the reset password template without any message.
    """

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
    """
    A view for creating a new doctor user.

    Attributes:
    model: The model to be created, in this case, User.
    form_class: The form class for creating a new doctor user, UserCreateForm.
    success_url: The URL to redirect to after successful doctor user creation.

    Methods:
    form_valid: Sets the 'is_doctor' and 'is_staff' attributes of the new user to True before saving.
    test_func: Checks if the current user is a superuser.
    """

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
    """
    A view for deleting a user profile.

    Attributes:
    model: The model to be updated, in this case, User.
    form_class: The form class for updating the user profile, ProfileForm.
    success_url: The URL to redirect to after successful profile deletion.
    template_name: The template to render for the profile view.

    Methods:
    test_func: Checks if the current user is the same as the profile being viewed or if the user is a superuser.
    """

    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile')
    template_name = 'users/profile.html'

    def test_func(self):
        if self.request.user == self.get_object() or self.request.user.is_superuser:
            return True


class UsersListView(ListView):
    """
    A view for displaying a list of doctor users.

    Attributes:
    model: The model to be displayed, in this case, User.
    template_name: The template to render for the list view.

    Methods:
    get_queryset: Returns a queryset of doctor users.
    """

    model = User
    template_name = 'med/about.html'

    def get_queryset(self):
        return User.objects.filter(is_doctor=True)
