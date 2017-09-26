from django.shortcuts import render

from .models import *


def home(request):
    return render(request, 'home.html')


def roster(request):
    freshman = Player.objects.filter(squad=Player.squads.FRESHMAN)
    jv = Player.objects.filter(squad=Player.squads.JV)
    varsity = Player.objects.filter(squad=Player.squads.VARSITY)

    context = {
        'freshman': freshman,
        'jv': jv,
        'varsity': varsity,
    }

    return render(request, 'roster.html', context)


def schedule(request):
    return render(request, 'schedule.html')


def coaches(request):
    return render(request, 'coaches.html')


def history(request):
    return render(request, 'history.html')


def photos(request):
    return render(request, 'photos.html')


def sponsor(request):
    return render(request, 'sponsor.html')