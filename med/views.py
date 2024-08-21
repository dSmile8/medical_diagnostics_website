from django.views.generic import ListView

from med.models import Services


class ServicesListView(ListView):
    """"Показ списка всех услуг"""

    model = Services
    template_name = 'med/index1.html'

    # def get_context(self):
        # context_data = get_category_cache()
        # return context_data

    def get_queryset(self):
        queryset = super().get_queryset().order_by('title')
        return queryset
