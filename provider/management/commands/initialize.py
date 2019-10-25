from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Create Initial User and Data'

    def handle(self, *args, **kwargs):
            try:
                admin = User.objects.create_superuser('admin', 'admin@admin.cc', 'admin')
                admin.save()
                self.stdout.write('Successfully created superuser.')
            except IntegrityError:
                self.stdout.write('Superuser exists already.')
