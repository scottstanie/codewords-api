# Serializers define how the API is presented.
# This file is imported into rest_api/viewsets.py

from rest_framework import serializers
from allauth.socialaccount.models import SocialToken
# Import your models to use with the API here:
from api.models import User, Candidate, Question, Showdown, Friend
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


class CandidateSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ('id', 'name', 'url', 'description')


class QuestionSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'title', 'url', 'description')


class ShowdownSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Showdown
        fields = ('id', 'url', 'winner', 'loser', 'rater', 'created_at')


class FriendSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ('id', 'url', 'first_name', 'last_name', 'facebook_id', 'image_url')
