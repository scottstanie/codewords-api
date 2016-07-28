from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

from base.sites import SITES
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings

def verify_socialaccount():
    if 'allauth.socialaccount' in settings.INSTALLED_APPS:
        return True
    else:
        return False

def verify_fb():
    if 'allauth.socialaccount.providers.facebook' in settings.INSTALLED_APPS:
        return True
    else:
        return False

def verify_google():
    if 'allauth.socialaccount.providers.google' in settings.INSTALLED_APPS:
        return True
    else:
        return False

class Command(BaseCommand):
    help = '''
        Generates social applications, for use with django-allauth.
    '''

    def handle(self, *args, **options):
        if verify_socialaccount() is True:
            call_command('checkfb')
            call_command('checkgoogle')
        else:
            self.stdout.write(self.style.WARNING('Allauth SocialApp not installed. Please check /base/settings.py'))
