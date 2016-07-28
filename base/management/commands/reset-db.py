from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = '''
        Deletes any local database files, resetting the database,
        then reruns setup.
    '''

    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.WARNING('Do you want to reset the local database (Y/n)?'), ending=' ')
            response_localdb = raw_input().lower()
            if response_localdb == 'n':
                self.stdout.write(self.style.WARNING('...SKIPPED.\n'))
            else:
                os.system("rm *_dev_database.db")
                self.stdout.write(self.style.SUCCESS('...Local DB cleared.\n'))
                call_command('setup')
        except KeyboardInterrupt:
            self.stderr.write('\n\nOperation cancelled.')
