from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, render_to_response, redirect

from django.conf import settings

from rest_framework.response import Response
from rest_framework.permissions import AllowAny  # , IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_auth.registration.views import SocialLoginView

from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.helpers import complete_social_login

from django.utils.translation import ugettext_lazy as _


from rest_framework import serializers


from requests.exceptions import HTTPError


### SOCIAL LOGIN ADAPTER ###

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed
        (and before the pre_social_login signal is emitted).
        We're trying to solve different use cases:
        - social account already exists, just go on
        - social account has no email or email is unknown, just go on
        - social account's email exists, link social account to existing user
        """

        # Ignore existing social accounts, just do this stuff for new ones
        if sociallogin.is_existing:
            return

        # some social logins don't have an email address, e.g. facebook accounts
        # with mobile numbers only, but allauth takes care of this case so just
        # ignore it
        if 'email' not in sociallogin.account.extra_data:
            return

        # check if given email address already exists.
        # Note: __iexact is used to ignore cases
        try:
            email = sociallogin.account.extra_data['email'].lower()
            email_address = EmailAddress.objects.get(email__iexact=email)

        # if it does not, let allauth take care of this new social account
        except EmailAddress.DoesNotExist:
            return

        # if it does, connect this new social login to the existing user
        user = email_address.user
        sociallogin.connect(request, user)


class CustomSocialLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=False, allow_blank=True)
    code = serializers.CharField(required=False, allow_blank=True)

    def _get_request(self):
        request = self.context.get('request')
        if not isinstance(request, HttpRequest):
            request = request._request
        return request

    def get_social_login(self, adapter, app, token, response):
        """
        :adapter: allauth.socialaccount Adapter subclass. Usually OAuthAdapter or Auth2Adapter
        :param app: `allauth.socialaccount.SocialApp` instance
        :param token: `allauth.socialaccount.SocialToken` instance
        :param response: Provider's response for OAuth1. Not used in the
        :return: :return: A populated instance of the `allauth.socialaccount.SocialLoginView` instance
        """
        request = self._get_request()

        if 'site' in request.GET.keys():
            self.app = SocialApp.objects.get(id=request.GET['site'])
        else:
            app = app

        social_login = adapter.complete_login(request, app, token, response=response)
        social_login.token = token

        return social_login

    def validate(self, attrs):
        view = self.context.get('view')
        request = self._get_request()

        if not view:
            raise serializers.ValidationError(
                _('View is not defined, pass it as a context variable')
            )

        adapter_class = getattr(view, 'adapter_class', None)
        if not adapter_class:
            raise serializers.ValidationError(_('Define adapter_class in view'))

        adapter = adapter_class(request)

        if 'site' in request.GET.keys():
            app = SocialApp.objects.get(id=request.GET['site'])
        else:
            app = adapter.get_provider().get_app(request)

        # More info on code vs access_token
        # http://stackoverflow.com/questions/8666316/facebook-oauth-2-0-code-and-token

        # Case 1: We received the access_token
        if('access_token' in attrs):
            access_token = attrs.get('access_token')

        # Case 2: We received the authorization code
        elif('code' in attrs):
            self.callback_url = getattr(view, 'callback_url', None)
            self.client_class = getattr(view, 'client_class', None)

            if not self.callback_url:
                raise serializers.ValidationError(
                    _('Define callback_url in view')
                )
            if not self.client_class:
                raise serializers.ValidationError(
                    _('Define client_class in view')
                )

            code = attrs.get('code')

            provider = adapter.get_provider()
            scope = provider.get_scope(request)
            client = self.client_class(
                request,
                app.client_id,
                app.secret,
                adapter.access_token_method,
                adapter.access_token_url,
                self.callback_url,
                scope
            )
            token = client.get_access_token(code)
            access_token = token['access_token']

        else:
            raise serializers.ValidationError(_('Incorrect input. access_token or code is required.'))

        token = adapter.parse_token({'access_token': access_token})
        token.app = app

        try:
            login = self.get_social_login(adapter, app, token, access_token)
            complete_social_login(request, login)
        except HTTPError:
            raise serializers.ValidationError(_('Incorrect value'))

        if not login.is_existing:
            login.lookup()
            login.save(request, connect=True)
        attrs['user'] = login.account.user

        return attrs


# Allows Facebook logins through the API.
class CustomFacebookAdapter(FacebookOAuth2Adapter):
    def get_login_redirect_url(self, request):
        return request.GET['next']


class FacebookLogin(SocialLoginView):
    adapter_class = CustomFacebookAdapter
    serializer_class = CustomSocialLoginSerializer


# Index View
def index(request):
    response = render(request, 'api/index.html')
    return response


# Ping Test view
def ping(request):
    return HttpResponse("OK")


# Custom API views
@api_view(['GET'])
@permission_classes([AllowAny])
def check_site(request):
    return Response({
        'site': settings.SITE_ID,
        'name': settings.SELECTED_SITE,
        'session_cookie_domain': settings.SESSION_COOKIE_DOMAIN,
        'csrf_cookie_domain': settings.CSRF_COOKIE_DOMAIN
    })
