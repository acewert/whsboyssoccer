from django.db import models


__all__ = ['Player']


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
