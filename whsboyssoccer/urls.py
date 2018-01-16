from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from app import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^coaches/$', views.coaches, name='coaches'),
    url(r'^history/$', views.history, name='history'),
    url(r'^oauth/$', views.oauth, name='oauth'),
    url(r'^photos/$', views.photos, name='photos'),
    url(r'^posts/$', views.posts, name='posts'),
    url(r'^roster/$', views.roster, name='roster'),
    url(r'^schedule/$', views.schedule, name='schedule'),
    url(r'^sponsor/$', views.sponsor, name='sponsor'),
    url(r'^$', views.home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
