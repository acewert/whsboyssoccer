from django import forms
from django.contrib import admin

from ckeditor.widgets import CKEditorWidget

from .models import *


def full_name(person):
    return '{0} {1}'.format(person.first_name, person.last_name)
full_name.short_description = 'Name'


class CoachAdmin(admin.ModelAdmin):
    list_display = (full_name, 'title', 'ordering')


class GameAdmin(admin.ModelAdmin):
    list_display = ('opponent', 'squad', 'date', 'time', 'location_name')


class PlayerAdmin(admin.ModelAdmin):
    list_display = (full_name, 'number', 'klass', 'squad', 'position')


class SeniorSpotlightAdminForm(forms.ModelForm):
    bio = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = SeniorSpotlight
        fields = '__all__'


class SeniorSpotlightAdmin(admin.ModelAdmin):
    form = SeniorSpotlightAdminForm


admin.site.register(Coach, CoachAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(SeniorSpotlight, SeniorSpotlightAdmin)