from django.conf.urls import url, include
from rest_framework import routers, views, reverse, response
from rest_framework.authtoken import views as authtoken_views
from api import views as api_views
from api.viewsets import *

# Routers provide an easy way for automatically determining the URL config
router = routers.DefaultRouter()

# Function used to simplify registering endpoints
def register(route, viewset, *args, **kwargs):
    router.register(route, viewset, *args, **kwargs)

# Register your API endpoints here, example:
# register(r'name_of_endpoint_link', YourViewSet)

register(r'users', UserViewSet)
register(r'token', TokenViewSet)
register(r'showdown', ShowdownViewSet)
register(r'question', QuestionViewSet)
register(r'candidate', CandidateViewSet)
register(r'friend', FriendViewSet)

# URL routes to be fed into /base/urls.py
# All custom views in /api/views.py are defined under api_views

urlpatterns = [
    url(r'^ping/$', api_views.ping, name='ping'),
    url(r'^site/', api_views.check_site),
    url(r'^api/', include(router.urls)),
    url(r'^api/auth/', include('rest_auth.urls')),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', authtoken_views.obtain_auth_token),
    url(r'^$', api_views.index, name='index'),
]
