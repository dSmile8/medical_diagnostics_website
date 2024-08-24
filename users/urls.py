from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, ProfileView, reset_password, DoctorCreateView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', UserCreateView.as_view(), name='create'),
    path('email-confirm/<str:token>/', email_verification, name='email_confirm'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path("reset_password/", reset_password, name="reset_password"),
    path("create_doctor/", DoctorCreateView.as_view(), name="create_doctor"),

]