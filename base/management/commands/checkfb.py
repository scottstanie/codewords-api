from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

from base.sites import SITES
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist

from checksocial import verify_socialaccount, verify_fb

class Command(BaseCommand):
    help = '''
        Generates Facebook social applications, for use with django-allauth.
    '''

    def handle(self, *args, **options):
        if verify_socialaccount() is True and verify_fb() is True:
            from allauth.socialaccount.models import SocialApp

            self.stdout.write(self.style.SUCCESS(
                'GENERATING FACEBOOK APPS from server/base/sites.py...'
            ))

            for site in SITES.keys():
                if 'FACEBOOK_KEY' and 'FACEBOOK_SECRET' in SITES[site].keys():
                    if SITES[site]['FACEBOOK_KEY'] != '' and SITES[site]['FACEBOOK_KEY'] != '':
                        try:
                            social_app = SocialApp.objects.get(
                                name = SITES[site]['SITE_NAME'],
                                provider = 'facebook'
                            )
                            if social_app.client_id != SITES[site]['FACEBOOK_KEY'] or social_app.secret != SITES[site]['FACEBOOK_SECRET']:
                                social_app.client_id = SITES[site]['FACEBOOK_KEY']
                                social_app.secret = SITES[site]['FACEBOOK_SECRET']
                                social_app.save()
                                self.stdout.write(self.style.SUCCESS('UPDATED: %s social app key and secret with current values.' % (social_app.name)))
                            else:
                                self.stdout.write(self.style.WARNING('SOCIAL APP ALREADY EXISTS: %s social app key and secret unchanged.' % (social_app.name)))
                        except ObjectDoesNotExist:
                            picked_site = Site.objects.get(name=SITES[site]['SITE_NAME'])
                            social_app = SocialApp(
                                provider = 'facebook',
                                name = SITES[site]['SITE_NAME'],
                                client_id = SITES[site]['FACEBOOK_KEY'],
                                secret = SITES[site]['FACEBOOK_SECRET']
                            )
                            social_app.save()
                            social_app.sites = [picked_site]
                            social_app.save()
                            self.stdout.write(self.style.SUCCESS('LINKED FACEBOOK APP: %s' % (SITES[site]['SITE_NAME'])))
            self.stdout.write(self.style.SUCCESS('...DONE'))

        else:
            self.stdout.write(self.style.WARNING(
                'Facebook provider not in INSTALLED_APPS. Please check /base/settings.py'
            ))
