from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

from checksocial import verify_socialaccount

class Command(BaseCommand):
    help = '''
        Runs setup, installs all python assets, migrates the database,
        sets up any sites in /base/sites.py, and allows you to create a
        Superuser.
    '''

    def add_arguments(self, parser):
        parser.add_argument(
            '--skipassets',
            action='store_true',
            dest='skipassets',
            help='Skips asset install.'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('WOLFHOUND-SERVER SETUP'))
        self.stdout.write(self.style.SUCCESS('======================\n'))

        try:
            if not options['skipassets']:
                call_command('assets')
            call_command('mm')
            call_command('checksites')

            if verify_socialaccount() is True:
                call_command('checksocial')

            self.stdout.write(self.style.WARNING('Create a SUPERUSER account (Y/n)?'), ending=' ')
            response_superuser = raw_input().lower()
            if response_superuser == 'n':
                self.stdout.write(self.style.WARNING('...SKIPPED.'))
            else:
                call_command('createsuperuser')
                self.stdout.write(self.style.WARNING('Make sure to change your superuser username and password in production.'))

            self.stdout.write(self.style.SUCCESS('\nWolfhound-Server SETUP complete!'))
            self.stdout.write(self.style.SUCCESS('To run the server, type: ./manage.py run OR ./manage.py api\n'))
        except KeyboardInterrupt:
            self.stderr.write('\n\nOperation cancelled.')
