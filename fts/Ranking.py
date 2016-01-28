from django.core.cache import caches

from ._base import BaseTestCase
from fb_rank.utils import update_rank

from main.models import Item


CACHE = caches['default']


class TestRankingUpdate(BaseTestCase):

    def tearDown(self):
        CACHE.clear()
        super(TestRankingUpdate, self).tearDown()

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

    def test_can_update_items_ranking_if_cache_exists(self):
        # Harriet makes sure that cache is not empty.
        key = 'rank_Item_example'
        CACHE.clear()
        CACHE.set(key, 0)

        # She triggers ranking update by hand.
        qs = Item.objects.filter(slug='example')
        update_rank(qs)

        # She now sees updated item rank in cache.
        likes = CACHE.get(key)
        self.assertNotEqual(likes, 0)


class TestItemsRanking(BaseTestCase):

    def setUp(self):
        qs = Item.objects.all()
        update_rank(qs)
        super(TestItemsRanking, self).setUp()

    def tearDown(self):
        CACHE.clear()
        super(TestItemsRanking, self).tearDown()

    def test_can_see_top_items_in_correct_order(self):
        # Florence hits a page with a list of top items.
        self.get(name='top_item_list')

        # She sees the items ordered from the most popular to the least popular.
        expected_output = '\n'.join([
            '/',
            '/example',
            '/admin',
            '/notexistingurl',
        ])
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn(expected_output, body_text)

    def test_can_see_only_items_above_some_threshold_on_trending_page(self):
        # Florence hits the trending page.
        self.get(name='trending_item_list')

        # She sees items with a rank above the threshold.
        body_text = self.browser.find_element_by_tag_name('body').text
        expected_output = '\n'.join(['/', '/example'])
        self.assertIn(expected_output, body_text)

        # She doesn't see items with a rank below the threshold.
        unexpected_output = '\n'.join(['/admin', '/notexistingurl'])
        self.assertNotIn(unexpected_output, body_text)

    def test_can_see_rank_of_a_single_item(self):
        # Florence hits a detail page for an item.
        self.get(name='item_detail', kwargs={'slug': 'example'})

        # She sees its rank.
        rank = self.browser.find_element_by_id('id_rank').text
        self.assertTrue(0 < int(rank) < 100)
