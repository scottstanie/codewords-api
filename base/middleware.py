from django.contrib.sites.models import Site
from django.conf import settings
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie

# Functtion that sets a session key if user has no existing session

def set_session(request):
    if hasattr(request, 'session') and not request.session.session_key:
        request.session.save()
        request.session.modified = True

# Gets root site domain and returns it

def set_root_domain(domain):
    domain_array = domain.split('.')
    if len(domain_array) > 2:
        domain_array.pop(0)
        root_domain = '.' + '.'.join(domain_array)
    else:
        root_domain = ''.join(domain_array)
    return root_domain

# Underscores spaces

def set_underscore(input_string):
    new_string = input_string.replace(" ", "_").lower()
    return new_string

# Grabs the request and applies the site ID to the appropriate site.

class WolfhoundSiteMiddleware(object):
    def process_request(self, request):
        host = request.get_host()

        if 'site_override' in request.GET.keys() and settings.DEBUG == True:
            host = request.GET['site_override']

        try:
            root_domain = set_root_domain(host)
            current_site = Site.objects.get(domain__icontains=root_domain)
            settings.SESSION_COOKIE_DOMAIN=set_root_domain(current_site.domain)
            settings.CSRF_COOKIE_DOMAIN=set_root_domain(current_site.domain)
        except Site.DoesNotExist:
            current_site = Site.objects.get(id=settings.SITE_ID)

        settings.SESSION_COOKIE_NAME=set_root_domain(set_underscore(current_site.name) + '_sessionid')
        settings.CSRF_COOKIE_NAME=set_root_domain(set_underscore(current_site.name) + '_csrftoken')

        request.current_site = current_site
        settings.SITE_ID = current_site.id
        settings.SELECTED_SITE = current_site.name

# Ensures sessions and tokens are applied each request

class WolfhoundSetSessionMiddleware(object):
    def process_response(self, request, response):
        set_session(request)
        get_token(request)
        return response
