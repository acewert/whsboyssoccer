from django import forms
from django.contrib import admin

from ckeditor.widgets import CKEditorWidget

from .models import *


class SeniorSpotlightAdminForm(forms.ModelForm):
    bio = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = SeniorSpotlight
        fields = '__all__'


class SeniorSpotlightAdmin(admin.ModelAdmin):
    form = SeniorSpotlightAdminForm


admin.site.register(Coach)
admin.site.register(Game)
admin.site.register(Player)
admin.site.register(SeniorSpotlight, SeniorSpotlightAdmin)