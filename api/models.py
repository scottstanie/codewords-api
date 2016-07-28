from __future__ import unicode_literals
from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser


# Creates an API auth token for every new user.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class User(AbstractUser):
    custom_data = models.TextField(null=True, blank=True)


class Candidate(models.Model):
    '''A user who is one of the two people getting rated'''
    name = models.CharField(max_length=255)
    url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.title


class Question(models.Model):
    '''The question posed for the user to answer

    The answer will be one of two Candidates shown to them'''
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return self.title


class Showdown(models.Model):
    url = models.URLField(null=True, blank=True)
    winner = models.ForeignKey(Candidate, related_name='wins')
    loser = models.ForeignKey(Candidate, related_name='loses')
    rater = models.ForeignKey(User)  # related_name = showdown_set
    question = models.ForeignKey(Question)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, null=True)

    def __unicode__(self):
        return "%s: winner: %s, loser: %s" % (self.question, self.winner, self.lost)


class Friend(models.Model):
    """
    A facebook friend of a signed up user (or through some other method of connection)
    """
    url = models.URLField(null=True, blank=True)
    source_user = models.ForeignKey(User)  # related_name = showdown_set
    first_name = models.TextField(null=True, blank=True)
    last_name = models.TextField(null=True, blank=True)
    facebook_id = models.IntegerField()
    image_url = models.URLField(null=True, blank=True)
