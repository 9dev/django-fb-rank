from math import ceil
import requests

from django.core.cache import caches
from django.conf import settings


BATCH_SIZE = 50
API_URL = 'https://graph.facebook.com'
CACHE = caches['default']


def update_rank(qs):
    obj_count = qs.count()
    batch_count = ceil(obj_count / BATCH_SIZE)
    model_name = qs.model.__name__

    for i in range(batch_count):
        items = {}
        for obj in qs[i*BATCH_SIZE:i*BATCH_SIZE+BATCH_SIZE-1]:
            full_url = settings.FULL_URL_PREFIX + obj.get_absolute_url()
            items[full_url] = obj

        params = {
            'ids': ','.join(items.keys()),
            'access_token': settings.FB_ACCESS_TOKEN,
        }

        response = requests.get(API_URL, params=params)
        data = response.json()

        if 'error' in data:
            raise Exception(data)

        for k, v in data.items():
            obj = items[k]
            rank = v['share']['share_count']
            CACHE.set('rank_{}_{}'.format(model_name, obj.pk), rank)


def get_top(qs, limit=10, offset=0):
    model_name = qs.model.__name__

    for obj in qs:
        obj.rank = CACHE.get('rank_{}_{}'.format(model_name, obj.pk), 0)

    qs = sorted(qs, key=lambda o: o.rank, reverse=True)
    return qs[offset:offset+limit]


def get_greater(qs, threshold, limit=10, offset=0):
    model_name = qs.model.__name__

    for obj in qs:
        obj.rank = CACHE.get('rank_{}_{}'.format(model_name, obj.pk), 0)

    qs = filter(lambda o: o.rank > threshold, qs)
    qs = sorted(qs, key=lambda o: o.rank, reverse=True)
    return qs[offset:offset+limit]
