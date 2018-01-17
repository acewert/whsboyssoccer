import requests
from datetime import datetime, timezone

from .models import Settings


__all__ = ['Album', 'Image']


""" TODO:
- is there some good way to combine ImgurManyToManyField with ImgurManager?
    - so, for instance, album.images can be both
"""


class ImgurQuery:
    BASE_URL = 'https://api.imgur.com/3/'
    _settings = None

    @classmethod
    def settings(cls):
        if cls._settings is None:
            cls._settings = Settings.objects.first()
        return cls._settings

    @classmethod
    def headers(cls):
        settings = cls.settings()
        authorization = 'Bearer {0}'.format(settings.imgur_access_token)

        return {
            'Authorization': authorization,
        }

    def __init__(self, path):
        self.path = path

    def execute(self):
        url = self.BASE_URL + self.path
        headers = self.headers()
        response = requests.get(url, headers=headers)
        return response.json()


class ImgurFieldError(Exception):
    pass


class ImgurField:
    def __init__(self, primary_key=False):
        # TODO: check that only one field per model has primary_key=True
        self.primary_key = primary_key


class ImgurBooleanField(ImgurField):
    def parse(self, value):
        # TODO: check it if's a boolean
        return value


class ImgurDateTimeField(ImgurField):
    def parse(self, value):
        return datetime.fromtimestamp(value, timezone.utc)


class ImgurIntegerField(ImgurField):
    def parse(self, value):
        # TODO: check if it's an integer
        return value


class ImgurStringField(ImgurField):
    def parse(self, value):
        # TODO: check if it's a string
        return value


class ImgurForeignKey(ImgurField):
    def __init__(self, model, **kwargs):
        super().__init__(**kwargs)
        self.model = model

    def parse(self, value):
        # TODO: check if value is of type self.model.pk
        return self.model(pk=value)


class ImgurQueryset:
    def __init__(self, model, path):
        self.model = model
        self.query = ImgurQuery(path)
        self._select_related = []
        self._results = None

    def __iter__(self):
        if self._results is None:
            self._execute()
        yield from self._results

    def _clone(self):
        qs = ImgurQueryset(self.model, self.query.path)
        qs._select_related = list(self._select_related)
        return qs

    def _execute(self):
        data = self.query.execute()['data']
        self._results = [self.model._from_raw_values(d) for d in data]

        for related_field_name in self._select_related:
            try:
                field = getattr(self.model, related_field_name)

                if not isinstance(field, ImgurForeignKey):
                    # TODO: exception message
                    raise ImgurFieldError
            except AttributeError:
                # TODO: exception message
                raise ImgurFieldError

            for obj in self._results:
                related_obj = getattr(obj, related_field_name)
                related_obj.refresh()

    def select_related(self, *related):
        qs = self._clone()
        qs._select_related.extend(related)
        return qs


class ImgurManager:
    def __init__(self, model, path):
        self.model = model
        self.path = path

    def all(self):
        return ImgurQueryset(self.model, self.path)

    def get(self, pk):
        obj = self.model(pk=pk)
        obj.refresh()
        return obj

    def select_related(self, *related):
        qs = ImgurQueryset(self.model, self.path).select_related(*related)
        return qs


class ImgurModel:
    @classmethod
    def _from_raw_values(cls, values):
        obj = cls()
        obj._populate_from_raw_values(values)
        return obj

    @classmethod
    def _get_pk_field_name(cls):
        for field_name, field in cls._get_fields():
            if field.primary_key:
                return field_name

    @classmethod
    # TODO: move to _meta.get_fields()
    def _get_fields(cls):
        for member_name in dir(cls):
            member = getattr(cls, member_name)
            if isinstance(member, ImgurField):
                yield member_name, member

    def __init__(self, **data):
        if 'pk' in data:
            self.pk = data['pk']
            del data['pk']

        self.__dict__.update(data)

    def get_path(self):
        return self.PATH.format(pk=self.pk)

    def get_pk(self):
        return getattr(self, self._get_pk_field_name())

    def set_pk(self, value):
        setattr(self, self._get_pk_field_name(), value)

    pk = property(get_pk, set_pk)

    def _populate_from_raw_values(self, raw_values):
        for field_name, field in self._get_fields():
            if field_name in raw_values:
                value = field.parse(raw_values[field_name])
                setattr(self, field_name, value)
            else:
                setattr(self, field_name, None)

    def refresh(self):
        path = self.get_path()
        query = ImgurQuery(path)
        response = query.execute()

        if response['status'] == 404:
            raise self.DoesNotExist

        self._populate_from_raw_values(response['data'])


"""
class Account(ImgurModel):
    username = ImgurStringField(primary_key=True)

    PATH = 'account/{pk}/'

    @property
    def albums(self):
        path = 'account/{0}/albums/'.format(self.pk)
        return ImgurManager(Album, path)
"""


class Image(ImgurModel):
    id = ImgurStringField(primary_key=True)
    animated = ImgurBooleanField()
    datetime = ImgurDateTimeField()
    description = ImgurStringField()
    height = ImgurIntegerField()
    link = ImgurStringField()
    title = ImgurStringField()
    width = ImgurIntegerField()

    PATH = 'image/{pk}/'

    def _thumbnail(self, suffix):
        link = self.link
        index = link.rfind('.')
        return link[:index] + suffix + link[index:]

    @property
    def big_square(self):
        return self._thumbnail('b')

    class DoesNotExist(Exception):
        pass

Image.objects = ImgurManager(Image, 'account/me/images/')


class Album(ImgurModel):
    id = ImgurStringField(primary_key=True)
    cover = ImgurForeignKey(Image)
    description = ImgurStringField()
    title = ImgurStringField()

    PATH = 'album/{pk}/'

    """ TODO: nope, this doesn't work, album.images needs to be a manager
    def __init__(self, images=None, **data):
        super().__init__(**data)

        images_path = 'album/{pk}/images/'.format(pk=self.pk)
        self.images = ImgurQueryset(Image, images_path)

        if images is not None:
            # TODO: make sure images is list<Image>
            self.images._results = images
    """

    @property
    def images(self):
        path = 'album/{pk}/images/'.format(pk=self.pk)
        return ImgurManager(Image, path)

    class DoesNotExist(Exception):
        pass

Album.objects = ImgurManager(Album, 'account/me/albums/')
