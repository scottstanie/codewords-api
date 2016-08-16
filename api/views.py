from itertools import cycle

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from django.conf import settings

from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from models import Game, User, Word, Card, Guess, Clue, TURN_STATES


# Index View
def index(request):
    response = render(request, 'api/index.html')
    return response


class IsCurrentGuesser(permissions.BasePermission):
    '''Checks whether a user is the current guesser of a game'''
    def has_object_permission(self, request, view, obj):
        is_current_player = obj.current_player().id == request.user.id
        is_a_guesser = (obj.red_guesser.id == request.user.id) or \
                       (obj.blue_guesser.id == request.user.id)
        return is_current_player and is_a_guesser


class IsCurrentGiver(permissions.BasePermission):
    '''Checks whether a user is the current clue giver'''
    def has_object_permission(self, request, view, obj):
        is_current_player = obj.current_player().id == request.user.id
        is_a_giver = (obj.red_giver.id == request.user.id) or \
                     (obj.blue_giver.id == request.user.id)
        return is_current_player and is_a_giver


@api_view(['Post'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsCurrentGuesser])
def guess(request):

    word_id = request.POST['wordId']
    unique_id = request.POST['game_id']
    player = request.POST['player']
    clue_number = int(request.POST['clueNumber'])

    game = get_object_or_404(Game, unique_id=unique_id)
    user = get_object_or_404(User, username=player)
    check_double_post(game, user)

    if word_id:
        word = get_object_or_404(Word, id=word_id.replace('word', ''))
        card = get_object_or_404(Card, word=word, game=game)
        card.chosen = True
        card.save()
    else:
        # User passed
        card = None

    team_color = request.POST['teamColor'].split('_')[0]
    guess = Guess(user=user, guesser_team=team_color, game=game, card=card)
    guess.save()
    if not word_id:
        # User passed
        game.current_turn = find_next_turn(game)
        game.current_guess_number = 0
        game.save()
        return Response({"message": "OK"})
    else:
        game.current_guess_number += 1

    if card.color == 'black':
        # Assassinated!
        game.active = False
        team_choices = {'red', 'blue'}
        other_team = (team_choices - set(team_color)).pop()
        game.winning_team = other_team
    elif (clue_number > 0 and game.current_guess_number >= clue_number + 1) \
            or guess.is_wrong():
        # Note: this greater than also works for '0' unlimited clues
        game.current_turn = find_next_turn(game)
        game.current_guess_number = 0

    decrement_card_counter(game, card.color)
    check_game_over(game)

    game.save()
    return Response({"message": "OK"})


def check_double_post(game, user):
    return user.username != game.current_player().username


@api_view(['Post'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsCurrentGiver])
def give(request):
    text = request.POST['text']
    unique_id = request.POST['game_id']
    player = request.POST['player']

    game = get_object_or_404(Game, unique_id=unique_id)
    user = get_object_or_404(User, username=player)
    if check_double_post(game, user):
        # Player has already given clue, probably a double post
        return Response({'message': 'double post'}, status=status.HTTP_409_CONFLICT)

    count = request.POST['count']
    clue = Clue(word=text, number=count, giver=user, game=game)
    clue.save()
    game.current_turn = find_next_turn(game)
    game.save()
    return Response({'message': 'ok'})


def find_next_turn(game):
    turn_cycle = cycle(t[0] for t in TURN_STATES)
    t = turn_cycle.next()
    while t != game.current_turn:
        t = turn_cycle.next()
    return turn_cycle.next()


def decrement_card_counter(game, card_color):
    if card_color == 'red':
        game.red_remaining -= 1
    elif card_color == 'blue':
        game.blue_remaining -= 1


def check_game_over(game):
    if game.red_remaining == 0:
        game.winning_team = 'red'
        game.active = False
    elif game.blue_remaining == 0:
        game.winning_team = 'blue'
        game.active = False


# Ping Test view
def ping(request):
    return HttpResponse("OK")


# Custom API views
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def check_site(request):
    return Response({
        'site': settings.SITE_ID,
        'name': settings.SELECTED_SITE,
        'session_cookie_domain': settings.SESSION_COOKIE_DOMAIN,
        'csrf_cookie_domain': settings.CSRF_COOKIE_DOMAIN
    })
