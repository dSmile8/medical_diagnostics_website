from datetime import datetime

from django.http import HttpRequest
from django.shortcuts import HttpResponseRedirect, get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView

from med.forms import AppointmentForm
from med.models import Services, Appointment
from users.models import User


class ServicesListView(ListView):
    """"Показ списка всех услуг"""

    model = Services
    template_name = 'med/index.html'

    # def get_context(self):
    # context_data = get_category_cache()
    # return context_data

    def get_queryset(self):
        queryset = super().get_queryset().order_by('title')
        return queryset

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name} / {phone} / {message}')
        data = f'Name: {name}. Phone: {phone}. Message: {message}\n'
        with open('user_data.txt', 'a', encoding='UTF-8') as f:
            f.write(data)
        return HttpResponseRedirect(reverse('med:index'))


class DoctorsListView(ListView):
    """Показ списка врачей"""
    model = User
    template_name = 'med/about.html'

    # def get_context(self):
    #     context_data = get_category_cache()
    #     return context_data

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class ServicesDetailView(DetailView):
    """"Детальная информация об услуге"""

    success_url = reverse_lazy('med:appointments_my')

    def get(self, request, pk):
        services = Services.objects.get(id=pk)
        doctor = User.objects.filter(is_doctor=True)
        context = {
            'services': services,
            'doctor': doctor,
            'title': services.title,
            'description': services.description
        }
        return render(request, 'med/services.html', context)


class ContactsTemplateView(TemplateView):
    template_name = 'med/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name} / {phone} / {message}')
        data = f'Name: {name}. Phone: {phone}. Message: {message}\n'
        with open('user_data.txt', 'a', encoding='UTF-8') as f:
            f.write(data)
        return HttpResponseRedirect(reverse('med:contacts'))


class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    success_url = reverse_lazy('med:appointments_my')

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        # self.service = Services.objects.get(pk=self.kwargs['pk'])
        # self.doctor = User.objects.filter(is_doctor=True)
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self, **kwargs):
        service = Services.objects.get(pk=self.kwargs['pk'])
        doctor = User.objects.filter(services=service.pk)
        return {
            'doctor': doctor,
            'date': datetime.now().strftime('%Y-%m-%d'),
        }

    def form_valid(self, form, **kwargs):
        form.instance.user = self.request.user
        form.instance.service = self.service
        # servise = Services.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


class AppointmentUserListView(ListView):
    """"Показ списка забронированных пользователем записей на диагностику"""
    model = Appointment
    template_name = 'med/user_appointments.html'

    # def get_context(self):
    #     context_data = get_category_cache()
    #     return context_data

    def get_queryset(self):
        user = self.request.user
        current_datetime = datetime.now()

        if user.is_authenticated:  # для зарегистрированных пользователей
            queryset = super().get_queryset().filter(user=user, date__gte=current_datetime).order_by('date')
        else:  # для незарегистрированных пользователей
            queryset = None
        return queryset


class AppointmentArchiveListView(ListView):
    """"Показ списка прошедших записей на диагностику"""
    model = Appointment
    template_name = 'med/appointments_archive.html'

    # def get_context(self):
    #     context_data = get_category_cache()
    #     return context_data

    def get_queryset(self):
        user = self.request.user
        current_datetime = datetime.now()

        if user.is_authenticated:  # для зарегистрированных пользователей
            if user.is_staff or user.is_superuser:  # для работников и суперпользователя
                queryset = super().get_queryset().filter(date__lt=current_datetime).order_by('-date', 'services')
            else:  # для остальных пользователей
                queryset = super().get_queryset().filter(user=user, date__lt=current_datetime).order_by('-date',
                                                                                                        'services')
        else:  # для незарегистрированных пользователей
            queryset = None
        return queryset


class AppointmentCancelView(View):
    """"Отмена записи на прием"""
    success_url = reverse_lazy('med:appointments_my')

    def post(self, request, pk, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.user = None
        appointment.save()
        return redirect(self.success_url)


class ServicesMakingListView(ListView):
    """"Показ списка всех услуг для записи на прием"""

    model = Services
    template_name = 'med/making_an_appointment.html'

    # def get_context(self):
    # context_data = get_category_cache()
    # return context_data

    def get_queryset(self):
        queryset = super().get_queryset().order_by('title')
        return queryset
