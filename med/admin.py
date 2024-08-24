from django.contrib import admin

from med.models import Services, Doctor, Appointment


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('title', 'price',)
    list_filter = ('price', 'doctor',)
    search_fields = ('title', 'price', 'doctor',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)
    list_filter = ('last_name', 'services',)
    search_fields = ('last_name', 'services',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'doctor', 'services', 'result')
    list_filter = ('user', 'doctor', 'services', 'result')
    search_fields = ('user', 'doctor', 'services', 'result')
