from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from pathlib import Path

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        db = Path(settings.DATABASES["default"]["NAME"])

        self.stdout.write(f"Database: {db}")
        self.stdout.write(f"Exists: {db.exists()}")
        self.stdout.write(f"Users: {User.objects.count()}")
        self.stdout.write(
            f"Superusers: {list(User.objects.filter(is_superuser=True).values_list('username', flat=True))}"
        )