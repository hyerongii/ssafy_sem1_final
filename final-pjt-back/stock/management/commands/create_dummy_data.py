# your_app/management/commands/create_dummy_data.py
from django.core.management.base import BaseCommand
from stock.utils import create_dummy_data, create_user_interests

class Command(BaseCommand):
    help = 'Creates dummy users and profiles for testing'

    def handle(self, *args, **kwargs):
        create_dummy_data()
        create_user_interests()
        self.stdout.write(self.style.SUCCESS('Successfully created dummy data'))