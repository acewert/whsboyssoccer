import requests

from .models import Settings


__all__ = ['Album']


class ImgurModel:
    BASE_URL = 'https://api.imgur.com/3/'
    
    @classmethod
    def headers(cls, settings):
        authorization = 'Bearer {0}'.format(settings.imgur_access_token)

        return {
            'Authorization': authorization,
        }

    @classmethod
    def query(cls):
        settings = Settings.objects.first()
        url = cls.collection_url(settings)
        headers = cls.headers(settings)
        response = requests.get(url, headers=headers)
        return [cls(**d) for d in response['data']]

    @classmethod
    def collection_url(cls, settings):
        path = cls.COLLECTION_PATH

        if ':account_username/' in path:
            account_username = '{0}/'.format(settings.imgur_account_username)
            path = path.replace(':account_username/', account_username)

        return cls.BASE_URL + path

    def __init__(**data):
        self.__dict__.update(data)

    def item_url(self, settings):
        path = self.ITEM_PATH

        if ':id/' in path:
            idno = '{0}/'.format(self.id)
            path = path.replace(':id/', idno)

        return cls.BASE_URL + path


class Album(ImgurModel):
    COLLECTION_PATH = 'account/:account_username/albums/'
    ITEM_PATH = 'album/:id/'
