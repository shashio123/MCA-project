from django.core.management.base import BaseCommand, CommandError
from customers.helper import calculate_defaulters_and_creditlimit

class Command(BaseCommand):
    help = 'Calculate credit score'

    def handle(self, *args, **options):
        calculate_defaulters_and_creditlimit()
        print("calculating customers cs......")



