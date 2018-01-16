from django.contrib.auth.models import User
from django.db import models


__all__ = ['Coach', 'Game', 'Link', 'Player', 'Post', 'SeniorSpotlight',
           'Settings', 'Sponsor']


class Coach(models.Model):
    class Meta:
        verbose_name_plural = 'coaches'

    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    title = models.CharField(max_length=64)
    bio = models.TextField(blank=True)
    email_address = models.EmailField(blank=True)
    photo = models.ImageField(blank=True)
    ordering = models.IntegerField()

    def __str__(self):
        return '{0} {1} ({2})'.format(self.first_name, self.last_name,
                                      self.title)


class Game(models.Model):
    class squads:
        FRESHMAN = 1
        JV = 2
        VARSITY = 3
        FRESHMAN_RED = 4

    SQUAD_CHOICES = (
        (squads.FRESHMAN_RED, 'Freshman Red'),
        (squads.FRESHMAN, 'Freshman'),
        (squads.JV, 'JV'),
        (squads.VARSITY, 'Varsity'),
    )

    squad = models.IntegerField(choices=SQUAD_CHOICES)
    scrimmage = models.BooleanField()
    date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    opponent = models.CharField(max_length=64)
    location_name = models.CharField(max_length=64, blank=True)
    location_map_url = models.URLField(blank=True)
    whs_score = models.IntegerField(null=True, blank=True)
    opponent_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{0}: {1}'.format(
            self.get_squad_display(),
            self.opponent
        )


class Link(models.Model):
    title = models.CharField(max_length=128)
    url = models.URLField()

    def __str__(self):
        return self.title


class Player(models.Model):
    class classes:
        FRESHMAN = 1
        SOPHOMORE = 2
        JUNIOR = 3
        SENIOR = 4

    class squads:
        FRESHMAN = 1
        JV = 2
        VARSITY = 3
        FRESHMAN_RED = 4

    class positions:
        FORWARD = 1
        MIDFIELDER = 2
        DEFENDER = 3
        GOALKEEPER = 4

    CLASS_CHOICES = (
        (classes.FRESHMAN, 'Freshman'),
        (classes.SOPHOMORE, 'Sophomore'),
        (classes.JUNIOR, 'Junior'),
        (classes.SENIOR, 'Senior'),
    )

    SQUAD_CHOICES = (
        (squads.FRESHMAN_RED, 'Freshman Red'),
        (squads.FRESHMAN, 'Freshman'),
        (squads.JV, 'JV'),
        (squads.VARSITY, 'Varsity'),
    )

    POSITION_CHOICES = (
        (positions.FORWARD, 'Forward'),
        (positions.MIDFIELDER, 'Midfielder'),
        (positions.DEFENDER, 'Defender'),
        (positions.GOALKEEPER, 'Goalkeeper'),
    )

    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    number = models.CharField(max_length=3)
    klass = models.IntegerField(choices=CLASS_CHOICES, verbose_name='Class')
    squad = models.IntegerField(choices=SQUAD_CHOICES)
    position = models.IntegerField(choices=POSITION_CHOICES)
    photo = models.ImageField(blank=True)

    def __str__(self):
        return '{0} {1} (#{2})'.format(self.first_name, self.last_name,
                                       self.number)


class Post(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Posted')
    author = models.ForeignKey(User)
    image = models.ImageField(blank=True)
    title = models.CharField(max_length=128)
    body = models.TextField()

    def __str__(self):
        return self.title


class SeniorSpotlight(models.Model):
    player = models.ForeignKey(Player, limit_choices_to={
        'klass': Player.classes.SENIOR
    })
    photo = models.ImageField()
    bio = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{0} {1}'.format(self.player.first_name, self.player.last_name)

    def save(self, *args, **kwargs):
        if self.active:
            qs = SeniorSpotlight.objects.filter(active=True)

            if self.pk:
                qs = qs.exclude(pk=self.pk)

            qs.update(active=False)

        super().save(*args, **kwargs)


class Settings(models.Model):
    imgur_client_id = models.CharField(max_length=255, blank=True)
    imgur_client_secret = models.CharField(max_length=255, blank=True)
    imgur_access_token = models.CharField(max_length=255, blank=True)
    imgur_refresh_token = models.CharField(max_length=255, blank=True)
    imgur_token_type = models.CharField(max_length=255, blank=True)


class Sponsor(models.Model):
    class levels:
        IRON = 1
        BRONZE = 2
        SILVER = 3
        GOLD = 4
        PLATINUM = 5

    LEVEL_CHOICES = (
        (levels.IRON, 'Iron'),
        (levels.BRONZE, 'Bronze'),
        (levels.SILVER, 'Silver'),
        (levels.GOLD, 'Gold'),
        (levels.PLATINUM, 'Platinum'),
    )

    name = models.CharField(max_length=128)
    level = models.IntegerField(choices=LEVEL_CHOICES)

    def __str__(self):
        return self.name
