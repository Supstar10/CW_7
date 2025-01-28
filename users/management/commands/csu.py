from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            username='daniil',
            email='admin@admin.com',
            password='admin',
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        user.set_password('admin')
        user.save()
