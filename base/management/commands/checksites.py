from django.core.management.base import BaseCommand, CommandError

from base.sites import SITES
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    help = '''
        Grabs all sites from /base/sites.py and makes sure they are
        created in the database if they do not exist.
    '''

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("CREATING SITES from /base/sites.py..."))

        for site in SITES.keys():
            try:
                checked_site = Site.objects.get(id=SITES[site]['SITE_ID'])
                if checked_site.name != SITES[site]['SITE_NAME'] or checked_site.domain != SITES[site]['SITE_DOMAIN']:
                    checked_site.name = SITES[site]['SITE_NAME']
                    checked_site.domain = SITES[site]['SITE_DOMAIN']
                    checked_site.save()
                    self.stdout.write('MODIFIED: %s site name and domain with current values.' % (SITES[site]['SITE_DOMAIN']))
                else:
                    self.stdout.write('SITE ALREADY EXISTS: %s site name and domain unchanged.' % (checked_site.domain))
            except ObjectDoesNotExist:
                checked_site = Site(
                    id = SITES[site]['SITE_ID'],
                    name = SITES[site]['SITE_NAME'],
                    domain = SITES[site]['SITE_DOMAIN']
                )
                checked_site.save()
                self.stdout.write('CREATED: %s site.' % (SITES[site]['SITE_DOMAIN']))

        self.stdout.write(self.style.SUCCESS('...DONE.\n'))
