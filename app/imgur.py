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
        url = cls.url(settings)
        headers = cls.headers(settings)
        response = requests.get(url, headers=headers)
        return response.json()

    @classmethod
    def url(cls, settings):
        path = cls.COLLECTION_PATH

        if ':account_username/' in path:
            account_username = '{0}/'.format(settings.imgur_account_username)
            path.replace(':account_username/', account_username)

        return cls.BASE_URL + path


class Album(ImgurModel):
    COLLECTION_PATH = 'account/:account_username/albums/'
    ITEM_PATH = 'album/:'
