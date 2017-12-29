from django.shortcuts import render

from .models import *


__all__ = [
    'home', 'roster', 'schedule', 'coaches', 'history', 'photos', 'sponsor',
]


def home(request):
    posts = Post.objects.order_by('-timestamp')[:5]
    raw_sponsors = Sponsor.objects.order_by('name')

    sponsors = {
        'iron': [],
        'bronze': [],
        'silver': [],
        'gold': [],
        'platinum': [],
    }

    for sponsor in raw_sponsors:
        sponsors[sponsor.get_level_display().lower()].append(sponsor)

    context = {
        'posts': posts,
        'sponsors': sponsors,
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