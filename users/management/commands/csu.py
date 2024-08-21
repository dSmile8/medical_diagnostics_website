from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@bk.com',
            first_name='Admin_first_name',
            last_name='Admin_last_name',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )

        user.set_password('123')
        user.save()
