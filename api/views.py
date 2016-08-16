from django.shortcuts import render
from django.http import HttpResponse

from django.conf import settings

from rest_framework.response import Response
from rest_framework.permissions import AllowAny  # , IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


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
