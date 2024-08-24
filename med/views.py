from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, TemplateView

from med.models import Services, Doctor


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
    model = Doctor
    template_name = 'med/about.html'

    # def get_context(self):
    #     context_data = get_category_cache()
    #     return context_data

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class ServicesDetailView(DetailView):
    """"Детальная информация об услуге"""
    model = Services

    def get(self, request, pk):
        services = Services.objects.get(id=pk)
        doctor = Doctor.objects.filter(services=services)
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
