from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = '''
        Asks to update setuptools and pip, then installs and updates
        assets from requirements.txt.
    '''

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Update SETUPTOOLS (Y/n)?'), ending=' ')
        response_setuptools = raw_input().lower()
        if response_setuptools == 'n':
            self.stdout.write(self.style.WARNING('...SKIPPED.\n'))
        else:
            os.system("$VIRTUAL_ENV/bin/pip install --upgrade setuptools")
            self.stdout.write(self.style.SUCCESS('...UPDATED.\n'))

        self.stdout.write(self.style.WARNING('Update PIP (Y/n)?'), ending=' ')
        response_pip = raw_input().lower()
        if response_pip == 'n':
            self.stdout.write(self.style.WARNING('...SKIPPED.\n'))
        else:
            os.system("$VIRTUAL_ENV/bin/pip install --upgrade pip")
            self.stdout.write(self.style.SUCCESS('...UPDATED.\n'))

        self.stdout.write(self.style.WARNING('Install ASSETS (Y/n)?'), ending=' ')
        response_assets = raw_input().lower()
        if response_assets == 'n':
            self.stdout.write(self.style.WARNING('...SKIPPED.\n'))
        else:
            self.stdout.write(self.style.SUCCESS('\nINSTALLING assets...'))
            os.system("$VIRTUAL_ENV/bin/pip install \
                -r requirements.txt")
            self.stdout.write(self.style.SUCCESS('...DONE.\n'))
