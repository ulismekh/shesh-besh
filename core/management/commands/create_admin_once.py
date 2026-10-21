
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create a one-time admin account using environment variables"

    def handle(self, *args, **options):
        username = os.environ.get("ADMIN_USERNAME")
        password = os.environ.get("ADMIN_PASSWORD")

        if not username or not password:
            raise CommandError(
                "Set ADMIN_USERNAME and ADMIN_PASSWORD environment variables."
            )

        User = get_user_model()

        if User.objects.filter(username=username).exists():
            raise CommandError(
                "This username already exists. No changes were made."
            )

        User.objects.create_superuser(
            username=username,
            email="",
            password=password,
        )

        self.stdout.write(
            self.style.SUCCESS(f"Superuser '{username}' created successfully.")
        )
