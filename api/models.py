from __future__ import unicode_literals
import hashlib
import time
from django.contrib.auth.models import User
from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser


COLOR_CHOICES = (('red', 'red'), ('blue', 'blue'), ('grey', 'grey'), ('black', 'black'))
TEAM_CHOICES = (('red', 'red'), ('blue', 'blue'))
TURN_STATES = (
    ('blue_give', 'Blue Team to give clue'), ('blue_guess', 'Blue Team to guess'),
    ('red_give', 'Red Team to give clue'), ('red_guess', 'Red Team to guess')
)


# Creates an API auth token for every new user.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class User(AbstractUser):
    custom_data = models.TextField(null=True, blank=True)


def _create_hash():
    """This function generate 10 character long hash"""
    hash = None
    while not hash:
        hash = hashlib.sha1()
        hash.update(str(time.time()))
        uid = hash.hexdigest()[:10]
        if Game.objects.filter(unique_id=uid).exists():
            hash = None
            continue
    return uid


class WordSet(models.Model):
    '''A set of words grouped together'''
    name = models.CharField(max_length=200, default='alternate')
    url = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Word(models.Model):
    '''A word can be reused across games'''
    text = models.CharField(max_length=200)
    word_set = models.ForeignKey(WordSet, default=1)
    url = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return self.text


class Game(models.Model):
    url = models.URLField(null=True, blank=True)
    unique_id = models.CharField(max_length=10, default=_create_hash, unique=True)
    red_giver = models.ForeignKey(User, related_name='red_giver', default=1)
    red_guesser = models.ForeignKey(User, related_name='red_guesser', default=1)
    blue_giver = models.ForeignKey(User, related_name='blue_giver', default=1)
    blue_guesser = models.ForeignKey(User, related_name='blue_guesser', default=1)
    current_turn = models.CharField(max_length=16, choices=TURN_STATES, default='red_give')
    current_guess_number = models.IntegerField(default=0)
    red_remaining = models.IntegerField(default=9)
    blue_remaining = models.IntegerField(default=9)
    started_date = models.DateTimeField('date started', auto_now_add=True)
    active = models.BooleanField(default=True)
    winning_team = models.CharField(max_length=5, choices=TEAM_CHOICES, null=True)
    word_set = models.ForeignKey(WordSet, default=1)

    def blue_team(self):
        return [self.blue_giver, self.blue_guesser]

    def red_team(self):
        return [self.red_giver, self.red_guesser]

    def all_players(self):
        return self.red_team() + self.blue_team()

    def current_player(self):
        '''Maps current_turn option to a User'''
        player_map = {
            'blue_give': self.blue_giver,
            'blue_guess': self.blue_guesser,
            'red_give': self.red_giver,
            'red_guess': self.red_guesser
        }
        return player_map[self.current_turn]

    def is_giver(self, user):
        return user == self.blue_giver or user == self.red_giver

    def print_with_score(self):
        return "Game %s: %s red remaining, %s blue remaining" % \
                (self.unique_id, self.red_remaining, self.blue_remaining)

    def __unicode__(self):
        return self.unique_id


class Card(models.Model):
    '''A Card is specific to one game'''
    url = models.URLField(null=True, blank=True)
    word = models.ForeignKey(Word)
    chosen = models.BooleanField(default=False)
    color = models.CharField(
        max_length=5,
        choices=COLOR_CHOICES,
        default='grey'
    )
    game = models.ForeignKey(Game, default=7)

    def __unicode__(self):
        return '%s: %s' % (str(self.word), self.color)


class Guess(models.Model):
    url = models.URLField(null=True, blank=True)
    user = models.ForeignKey(User)
    guesser_team = models.CharField(max_length=5, choices=TEAM_CHOICES, default='red')
    game = models.ForeignKey(Game, default=7)
    card = models.OneToOneField(Card, null=True)

    def is_wrong(self):
        return self.card.color != self.guesser_team

    def __unicode__(self):
        if self.card is None:
            string = "Pass by %s on %s" % (self.user, self.guesser_team)
        else:
            string = '"%s" guessed by %s on %s' % (self.card, self.user, self.guesser_team)
        return string


class Clue(models.Model):
    url = models.URLField(null=True, blank=True)
    word = models.CharField(max_length=96)
    number = models.IntegerField(default=1)
    giver = models.ForeignKey(User, default=1)
    game = models.ForeignKey(Game, default=7)

    def __unicode__(self):
        return '%s - %s' % (self.word, self.number)
