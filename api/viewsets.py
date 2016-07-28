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


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_queryset(self):
        unique_id = self.request.query_params.get('unique_id', None)

        if unique_id is not None:
            return self.queryset.filter(title__icontains=unique_id)
        else:
            return self.queryset


class WordSetViewSet(viewsets.ModelViewSet):
    queryset = WordSet.objects.all()
    serializer_class = WordSetSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name', None)

        if name is not None:
            return self.queryset.filter(title__icontains=name)
        else:
            return self.queryset


class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer

    def get_queryset(self):
        text = self.request.query_params.get('text', None)

        if text is not None:
            return self.queryset.filter(name__icontains=text)
        else:
            return self.queryset


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class GuessViewSet(viewsets.ModelViewSet):
    queryset = Guess.objects.all()
    serializer_class = GuessSerializer


class ClueViewSet(viewsets.ModelViewSet):
    queryset = Clue.objects.all()
    serializer_class = ClueSerializer
