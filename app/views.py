import random

from django.core.paginator import Paginator
from django.shortcuts import render

from .models import *


__all__ = [
    'home', 'roster', 'schedule', 'coaches', 'history', 'photos', 'posts',
    'sponsor',
]


def random_splash():
    SPLASH_IMAGES = [
        ('0109', 'left 50% top 75%'),
        ('9001', 'left 40% top 20%'),
        ('9018', 'left 50% top 10%'),
        ('9041', 'left 50% top 25%'),
        ('9044', 'left 50% top 50%'),
        ('9071', 'left 50% top 5%'),
        ('9072', 'left 50% top 10%'),
        ('9103', 'left 30% top 50%'),
        ('9124', 'left 75% top'),
        ('9180', 'left 40% top 20%'),
        ('9196', 'left 50% top 30%'),
        ('9269', 'left 40% top 85%'),
        ('9346', 'left 50% top 25%'),
    ]

    img, pos = random.choice(SPLASH_IMAGES)

    return {
        'splash': 'images/splash/IMG_' + str(img) + '.JPG',
        'splash_position': pos,
    }


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

    context.update(random_splash())

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

    context.update(random_splash())

    return render(request, 'roster.html', context)


def schedule(request):
    games = Game.objects.order_by('date')

    context = {'games': games}
    context.update(random_splash())

    return render(request, 'schedule.html', context)


def coaches(request):
    coaches = Coach.objects.order_by('ordering')

    context = {'coaches': coaches}
    context.update(random_splash())

    return render(request, 'coaches.html', context)


def history(request):
    context = random_splash()

    return render(request, 'history.html', context)


def photos(request):
    context = random_splash()

    return render(request, 'photos.html', context)


def posts(request):
    all_posts = Post.objects.order_by('-timestamp')
    paginator = Paginator(all_posts, 10)

    page = request.GET.get('page')

    try:
        page = int(page)
    except (TypeError, ValueError):
        page = 1

    if page < 1 or (page > paginator.num_pages and page != 1):
        page = paginator.num_pages

    posts = paginator.page(page)

    context = {'posts': posts}
    context.update(random_splash())

    return render(request, 'posts.html', context)


def sponsor(request):
    context = random_splash()

    return render(request, 'sponsor.html', context)
