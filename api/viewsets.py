# ViewSets define the view behavior for the API.
# This file is imported into rest_api/urls.py

from rest_framework import viewsets
from allauth.socialaccount.models import SocialAccount, SocialToken
from api.serializers import *


# ViewSets define the view behavior for the API.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        all = self.request.query_params.get('all', None)

        if all is not None and user.is_superuser:
            return self.queryset
        else:
            return self.queryset.filter(username=user.username)

# class TokenViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Token.objects.all()
#     serializer_class = TokenSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         if not user.is_anonymous():
#             return self.queryset.filter(user=user)
#         else:
#             return []
# Replace TokenViewSet with the following if Allauth is installed as well
# as the SocialTokenSerializer in /server/api/serializers.py:


class TokenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_anonymous():
            if len(self.queryset.filter(user=user)) != 0:
                return self.queryset.filter(user=user)
            else:
                self.serializer_class = SocialTokenSerializer
                try:
                    new_queryset = SocialToken.objects.all()
                    return new_queryset.filter(account__user=user)
                except ObjectDoesNotExist:
                    return []
        else:
            return []


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        title = self.request.query_params.get('title', None)

        if title is not None:
            return self.queryset.filter(title__icontains=title)
        else:
            return self.queryset


class ShowdownViewSet(viewsets.ModelViewSet):
    queryset = Showdown.objects.all()
    serializer_class = ShowdownSerializer


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name', None)

        if name is not None:
            return self.queryset.filter(name__icontains=name)
        else:
            return self.queryset


class FriendViewSet(viewsets.ModelViewSet):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer

    def get_queryset(self):
        first_name = self.request.query_params.get('first_name', None)

        if first_name is not None:
            return self.queryset.filter(first_name__icontains=first_name)
        else:
            return self.queryset
