from datetime import datetime

from django.shortcuts import HttpResponseRedirect, get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView

from med.forms import AppointmentForm
from med.models import Services, Appointment
from users.models import User


class ServicesListView(ListView):
    """
    Display a list of all services.

    Attributes:
    model : Services
        The model class to query for the list of services.
    template_name : str
        The name of the template to render for this view.

    Methods:
    get_queryset()
        Override the default queryset to order services by title.
    post(request, *args, **kwargs)
        Handle POST requests to process form data.
        Save user's contact information and redirect to the same page.
    """

    model = Services
    template_name = 'med/index.html'

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
    """
       Retrieve and return all doctors.

       Parameters:
       None

       Returns:
       queryset : QuerySet
           A QuerySet containing all doctors.
   """

    model = User
    template_name = 'med/about.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class ServicesDetailView(DetailView):
    """
    Display detailed information about a service.

    Attributes:
    success_url : str
        The URL to redirect to after successful processing.

    Methods:
    get(request, pk)
        Retrieve and display detailed information about a service.

    Parameters:
    request : HttpRequest
        The request object.
    pk : int
        The primary key of the service to retrieve.

    Returns:
    HttpResponse
        The rendered HTML response with detailed information about the service.
    """

    success_url = reverse_lazy('med:appointments_my')

    def get(self, request, pk):
        services = Services.objects.get(id=pk)
        self.service = Services.objects.get(pk=self.kwargs['pk'])
        self.doctor = self.service.services.filter(services=self.service.pk)
        context = {
            'services': services,
            'doctor': self.doctor,
            'title': services.title,
            'description': services.description
        }
        return render(request, 'med/services.html', context)


class ContactsTemplateView(TemplateView):
    """
    A view for displaying the contacts page.

    Attributes:
    template_name : str
        The name of the template to render for this view.

    Methods:
    get_context_data(self, **kwargs)
        Override the default get_context_data method to add a title to the context.
    post(self, request, *args, **kwargs)
        Handle POST requests to process form data.
        Save user's contact information and redirect to the same page.
    """
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
    """
    A view for creating a new appointment.

    Attributes:
    model : Appointment
        The model class to create a new appointment.
    form_class : AppointmentForm
        The form class to use for creating a new appointment.
    success_url : str
        The URL to redirect to after successfully creating an appointment.

    Methods:
    get_initial(self, **kwargs)
        Override the default get_initial method to set initial values for the form.
    form_valid(self, form, **kwargs)
        Override the default form_valid method to set the user and service for the appointment.
    """
    model = Appointment
    form_class = AppointmentForm
    success_url = reverse_lazy('med:appointments_my')

    def get_initial(self, **kwargs):
        self.service = Services.objects.get(pk=self.kwargs['pk'])
        print(self.service)
        self.doctor = self.service.services.filter(services=self.service.pk)
        return {
            'doctor': self.doctor,
            'date': datetime.now().strftime('%Y-%m-%d'),
        }

    def form_valid(self, form, **kwargs):
        form.instance.user = self.request.user
        form.instance.services = self.service
        return super().form_valid(form)


class AppointmentUserListView(ListView):
    """
    Display a list of appointments made by the current user.

    Attributes:
    model : Appointment
        The model class to query for the list of appointments.
    template_name : str
        The name of the template to render for this view.

    Methods:
    get_queryset()
        Override the default queryset to filter and order appointments.

    Parameters:
    None

    Returns:
    queryset : QuerySet
        A QuerySet containing all appointments made by the current user,
        ordered by date in ascending order. If the user is not authenticated,
        the queryset will be None.
    """

    model = Appointment
    template_name = 'med/appointments_my.html'

    def get_queryset(self):
        user = self.request.user
        current_datetime = datetime.now()

        if user.is_authenticated:  # для зарегистрированных пользователей
            queryset = super().get_queryset().filter(user=user, date__gte=current_datetime).order_by('date')
        else:  # для незарегистрированных пользователей
            queryset = None
        return queryset


class AppointmentArchiveListView(ListView):
    """
    Display a list of past appointments for diagnosis.

    Attributes:
    model : Appointment
        The model class to query for the list of appointments.
    template_name : str
        The name of the template to render for this view.

    Methods:
    get_queryset()
        Override the default queryset to filter and order past appointments.

    Parameters:
    None

    Returns:
    queryset : QuerySet
        A QuerySet containing all past appointments, ordered by date in descending order and then by service.
        If the user is not authenticated, the queryset will be None.
    """

    model = Appointment
    template_name = 'med/appointments_archive.html'

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
    """
    A view for canceling an appointment.

    Attributes:
    success_url : str
        The URL to redirect to after successfully canceling an appointment.

    Methods:
    post(self, request, pk, *args, **kwargs)
        Handle POST requests to cancel an appointment.

    Parameters:
    request : HttpRequest
        The request object.
    pk : int
        The primary key of the appointment to cancel.
    args : tuple
        Additional positional arguments.
    kwargs : dict
        Additional keyword arguments.

    Returns:
    HttpResponseRedirect
        A redirect response to the success URL.
    """

    success_url = reverse_lazy('med:appointments_my')

    def post(self, request, pk, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.user = None
        appointment.save()
        return redirect(self.success_url)


class ServicesMakingListView(ListView):
    """
    Display a list of all services for making an appointment.

    Attributes:
    model : Services
        The model class to query for the list of services.
    template_name : str
        The name of the template to render for this view.

    Methods:
    get_queryset()
        Override the default queryset to order services by title.

    Parameters:
    None

    Returns:
    queryset : QuerySet
        A QuerySet containing all services ordered by title.
    """

    model = Services
    template_name = 'med/making_an_appointment.html'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('title')
        return queryset
