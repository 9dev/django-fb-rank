from django.core.cache import caches

from ._base import BaseTestCase
from fb_rank.utils import update_rank

from main.models import Item


CACHE = caches['default']


class TestRankingUpdate(BaseTestCase):

    def test_can_update_items_ranking_if_cache_does_not_exist(self):
        # Harriet makes sure that cache is empty.
        CACHE.clear()
        likes = CACHE.get_many(['rank_Item_1', 'rank_Item_2'])
        self.assertEqual(likes, {})

        # She triggers ranking update for all the items.
        qs = Item.objects.all()
        update_rank(qs)

        # She now sees new items in cache along with their rankings.
        likes = CACHE.get_many(['rank_Item_1', 'rank_Item_2'])
        self.assertNotEqual(likes, {})
