from django.db import models

from django.core.exceptions import ValidationError
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


class Services(models.Model):
    """
    This class represents a service offered by a medical service system.

    Attributes:
    title: The title or name of the service.
    description: A detailed description of the service.
    price: The cost of the service.
    image: An image representing the service.
    title = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    price = models.PositiveIntegerField(verbose_name='стоимость')
    image = models.ImageField(upload_to='image/', verbose_name='иконка', **NULLABLE)
    """

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'услуга'
        verbose_name_plural = 'услуги'


class Appointment(models.Model):
    """
    This class represents an appointment record in a medical service system.

    Attributes:
    user: The patient who made the appointment.
    services: The diagnostic service for which the appointment is made.
    doctor: The doctor assigned to the appointment.
    date: The date and time of the appointment.
    result: The results of the diagnostic examination.

    Methods:
    clean_fields: Validates that the appointment date is not in the past.
    """

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='записи', verbose_name='пациент',
                             **NULLABLE)
    services = models.ForeignKey('Services', on_delete=models.CASCADE, related_name='записи',
                                 verbose_name='диагностика', **NULLABLE)
    doctor = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='user', verbose_name='врач')
    date = models.DateTimeField(verbose_name='дата и время приема')
    result = models.TextField(verbose_name='результаты обследования', **NULLABLE)

    def __str__(self):
        return f'{self.user}: {self.date} {self.services}, {self.doctor}'

    class Meta:
        verbose_name = 'запись на диагностику'
        verbose_name_plural = 'записи на диагностику'

    def clean_fields(self, exclude=None):

        super().clean_fields(exclude=exclude)

        now = timezone.now()
        if self.date < now:
            raise ValidationError('Не допускается создавать записи в прошедшем времени')
