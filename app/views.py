from django.shortcuts import render

from .models import *


__all__ = [
    'home', 'roster', 'schedule', 'coaches', 'history', 'photos', 'sponsor',
]


def home(request):
    try:
        senior_spotlight = SeniorSpotlight.objects.get(active=True)
    except SeniorSpotlight.DoesNotExist:
        senior_spotlight = None

    posts = Post.objects.order_by('-timestamp')[:5]

    context = {
        'posts': posts,
        'senior_spotlight': senior_spotlight
    }

    return render(request, 'home.html', context)


def roster(request):
    freshman_red = Player.objects.filter(squad=Player.squads.FRESHMAN_RED)
    freshman = Player.objects.filter(squad=Player.squads.FRESHMAN)
    jv = Player.objects.filter(squad=Player.squads.JV)
    varsity = Player.objects.filter(squad=Player.squads.VARSITY)

    context = {
        'freshman_red': freshman_red,
        'freshman': freshman,
        'jv': jv,
        'varsity': varsity,
    }

    return render(request, 'roster.html', context)


def schedule(request):
    games = Game.objects.order_by('date')

    context = {'games': games}

    return render(request, 'schedule.html', context)


def coaches(request):
    coaches = Coach.objects.order_by('ordering')

    context = {'coaches': coaches}

    return render(request, 'coaches.html', context)


def history(request):
    return render(request, 'history.html')


def photos(request):
    return render(request, 'photos.html')


def sponsor(request):
    return render(request, 'sponsor.html')