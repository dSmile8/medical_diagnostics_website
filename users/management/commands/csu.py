from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    This command is used to create initial users for the application.
    It creates four users: an admin, two patients, and two doctors.
    Each user is created with default values and passwords set to '123'.
    """

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@bk.com',
            first_name='Admin_first_name',
            last_name='Admin_last_name',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
        user1 = User.objects.create(
            email='user1@bk.com',
            first_name='Пациент 1',
            last_name='Пациентов 1',
            is_active=True
        )
        user2 = User.objects.create(
            email='user2@bk.com',
            first_name='Пациент 2',
            last_name='Пациентов 2',
            is_active=True
        )
        user3 = User.objects.create(
            email='doc1@bk.com',
            first_name='Доктор',
            last_name='Ай!Болит',
            is_active=True,
            is_staff=True,
            is_doctor=True,
        )
        user4 = User.objects.create(
            email='doc2@bk.com',
            first_name='Елена',
            last_name='Малышева',
            is_active=True,
            is_staff=True,
            is_doctor=True,
        )

        user.set_password('123')
        user1.set_password('123')
        user2.set_password('123')
        user3.set_password('123')
        user4.set_password('123')
        user.save()
        user1.save()
        user2.save()
        user3.save()
        user4.save()
