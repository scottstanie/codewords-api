# Serializers define how the API is presented.
# This file is imported into rest_api/viewsets.py

from rest_framework import serializers
from allauth.socialaccount.models import SocialToken

from api.models import User, Game, WordSet, Word, Card, Guess, Clue
from rest_framework.authtoken.models import Token
# Import special API serializer mixins from api/mixins.py
from api.mixins import DynamicFieldsMixin


# Recursive Serializer, use for recursive models.
class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

# Serializers define the API representation.


class UserSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    date_joined = serializers.CharField(read_only=True)
    last_login = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'custom_data',
            'date_joined',
            'last_login'
        )


class TokenSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Token
        fields = ('key', 'user_id')


# Used only if Allauth is installed.
# Uncomment below to use in place of TokenSerializer:

class SocialTokenSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField('dynamic_user_id')
    key = serializers.SerializerMethodField('dynamic_key')

    def dynamic_user_id(self, token):
        user = self.context['request'].user
        if user is not None and not user.is_anonymous():
            return user.id

    def dynamic_key(self, token):
        return token.token

    class Meta:
        model = SocialToken
        fields = ('key', 'user_id')


class GameSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = (
            'id', 'url', 'unique_id', 'red_giver', 'red_guesser',
            'blue_giver', 'blue_guesser', 'current_turn', 'current_guess_number',
            'red_remaining', 'blue_remaining', 'started_date', 'active',
            'winning_team', 'word_set'
        )


class WordSetSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'url', 'description')
        model = WordSet


class WordSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ('id', 'text', 'word_set', 'url')


class CardSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    word = WordSerializer()

    class Meta:
        model = Card
        fields = ('id', 'url', 'word', 'chosen', 'color', 'game')


class GuessSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Guess
        fields = ('id', 'url', 'user', 'guesser_team', 'game', 'card')


class ClueSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Clue
        fields = ('id', 'url', 'word', 'number', 'giver', 'game')
