from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

class Command(BaseCommand):
    help = '''
        Runs Werkzeug, similar to the runserver_plus command.
    '''

    def handle(self, *args, **options):
        call_command('runserver_plus')
