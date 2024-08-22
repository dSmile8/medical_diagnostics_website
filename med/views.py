from django.shortcuts import render
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
