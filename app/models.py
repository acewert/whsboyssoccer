from django.contrib.auth.models import User
from django.db import models


__all__ = ['Coach', 'Game', 'Link', 'Player', 'Post', 'SchoolRecord',
           'SeniorSpotlight', 'Settings', 'Sponsor']


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


class SchoolRecord(models.Model):
    class categories:
        GAME_ASSISTS = 1
        GAME_GOALS = 2
        GAME_SAVES = 3
        SEASON_ASSISTS = 4
        SEASON_GOALS = 5
        SEASON_SAVES = 6
        CAREER_ASSISTS = 7
        CAREER_GOALS = 8
        CAREER_SAVES = 9
        WINNING_STREAK = 10
        SEASON_WINS = 11
        SHUTOUTS = 12
        PLAYOFF_APPEARANCE = 13

    CATEGORY_CHOICES = (
        (categories.GAME_ASSISTS, 'Most Individual Assists in a Game'),
        (categories.GAME_GOALS, 'Most Individual Goals in a Game'),
        (categories.GAME_SAVES, 'Most Saves in a Game'),
        (categories.SEASON_ASSISTS, 'Most Individual Assists in a Season'),
        (categories.SEASON_GOALS, 'Most Individual Goals in a Season'),
        (categories.SEASON_SAVES, 'Most Saves in a Season'),
        (categories.CAREER_ASSISTS, 'Most Individual Career Assists'),
        (categories.CAREER_GOALS, 'Most Individual Career Goals'),
        (categories.CAREER_SAVES, 'Most Career Saves'),
        (categories.WINNING_STREAK, 'Longest Winning Streak'),
        (categories.SEASON_WINS, 'Most Wins in a Season'),
        (categories.SHUTOUTS, 'Most Shutouts'),
        (categories.PLAYOFF_APPEARANCE, 'Best Playoff Appearance'),
    )

    INDIVIDUAL_CATEGORIES = [
        categories.GAME_ASSISTS, categories.GAME_GOALS, categories.GAME_SAVES,
        categories.SEASON_ASSISTS, categories.SEASON_GOALS,
        categories.SEASON_SAVES, categories.CAREER_ASSISTS,
        categories.CAREER_GOALS, categories.CAREER_SAVES,
    ]

    TEAM_CATEGORIES = [
        categories.WINNING_STREAK, categories.SEASON_WINS, categories.SHUTOUTS,
        categories.PLAYOFF_APPEARANCE,
    ]

    category = models.IntegerField(choices=CATEGORY_CHOICES)
    record = models.CharField(max_length=32)
    season = models.CharField(max_length=9)
    player = models.CharField(max_length=65, blank=True)

    def __str__(self):
        if self.category in self.INDIVIDUAL_CATEGORIES:
            return '{0}: {1} - {2} ({3})'.format(
                self.get_category_display(),
                self.player,
                self.record,
                self.season,
            )
        else:
            return '{0}: {1} ({2})'.format(
                self.get_category_display(),
                self.record,
                self.season,
            )


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
    imgur_token_expires = models.DateTimeField(null=True)
    imgur_account_id = models.CharField(max_length=255, blank=True)
    imgur_account_username = models.CharField(max_length=255, blank=True)


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
