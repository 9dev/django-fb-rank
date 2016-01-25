from django.core.cache import caches

from ._base import BaseTestCase
from fb_rank.utils import update_rank

from main.models import Item


CACHE = caches['default']


class TestRankingUpdate(BaseTestCase):
    fixtures = ['base.json']

    def test_can_update_items_ranking_if_cache_does_not_exist(self):
        # Harriet makes sure that cache is empty.
        CACHE.clear()
        qs = Item.objects.all()
        keys = ['rank_Item_'+x for x in qs.values_list('slug', flat=True)]
        likes = CACHE.get_many(keys)
        self.assertEqual(likes, {})

        # She triggers ranking update for all the items.
        update_rank(qs)

        # She now sees new items in cache along with their rankings.
        likes = CACHE.get_many(keys)
        self.assertNotEqual(likes, {})
