from django.db import models


__all__ = ['Coach', 'Game', 'Player', 'SeniorSpotlight']


class Coach(models.Model):
    class Meta:
        verbose_name_plural = 'coaches'

    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    title = models.CharField(max_length=64)
    bio = models.TextField(blank=True)
    email_address = models.EmailField(blank=True)
    ordering = models.IntegerField()

    def __str__(self):
        return '{0} {1} ({2})'.format(self.first_name, self.last_name,
                                      self.title)


class Game(models.Model):
    class squads:
        FRESHMAN = 1
        JV = 2
        VARSITY = 3

    SQUAD_CHOICES = (
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
    klass = models.IntegerField(choices=CLASS_CHOICES)
    squad = models.IntegerField(choices=SQUAD_CHOICES)
    position = models.IntegerField(choices=POSITION_CHOICES)

    def __str__(self):
        return '{0} {1} (#{2})'.format(self.first_name, self.last_name,
                                       self.number)


class SeniorSpotlight(models.Model):
    player = models.ForeignKey(Player)
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
