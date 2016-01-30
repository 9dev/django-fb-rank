from unittest.mock import call, MagicMock, patch

from django.test import TestCase

from .utils import get_greater, get_rank, get_top, update_rank


class QuerySetMock(object):

    def __init__(self, objects):
        self.model = MagicMock(__name__='MyModelMock')
        self.objects = objects

    def __iter__(self):
        return iter(self.objects)

    def __getitem__(self, x):
        return self.objects.__getitem__(x)

    def count(self):
        return len(self.objects)


class MyModelMock(object):

    def __init__(self, pk):
        self.pk = pk

    def get_absolute_url(self):
        return '/{}'.format(self.pk)


class UtilsTestCase(TestCase):

    @patch('fb_rank.utils.CACHE.get')
    def test_can_get_rank_for_a_single_object(self, mock_cache_get):
        obj = MyModelMock(1)

        rank = get_rank(obj)

        mock_cache_get.assert_called_once_with('rank_MyModelMock_1', 0)
        self.assertEqual(rank, mock_cache_get.return_value)

    @patch('fb_rank.utils.CACHE.get')
    def test_can_get_top_objects_with_no_arguments(self, mock_cache_get):
        n = 5
        objects = [MyModelMock(i) for i in range(n)]
        mock_cache_get.side_effect = list(range(n))
        qs = QuerySetMock(objects)

        calls = []
        for i in range(n):
            calls.append(call('rank_MyModelMock_{}'.format(i), 0))

        result = get_top(qs)

        mock_cache_get.assert_has_calls(calls)
        self.assertEqual(result, list(reversed(objects)))

    @patch('fb_rank.utils.CACHE.get')
    def test_can_get_top_objects_with_limit_and_offset(self, mock_cache_get):
        n = 20
        objects = [MyModelMock(i) for i in range(n)]
        mock_cache_get.side_effect = list(range(n))
        qs = QuerySetMock(objects)

        calls = []
        for i in range(n):
            calls.append(call('rank_MyModelMock_{}'.format(i), 0))

        result = get_top(qs, limit=5, offset=5)

        mock_cache_get.assert_has_calls(calls)
        self.assertEqual(result, list(reversed(objects))[5:10])

    @patch('fb_rank.utils.CACHE.get')
    def test_cannot_get_top_objects_for_empty_queryset(self, mock_cache_get):
        objects = []
        qs = QuerySetMock(objects)

        result = get_top(qs)

        mock_cache_get.assert_not_called()
        self.assertEqual(result, [])

    @patch('fb_rank.utils.CACHE.get')
    def test_can_get_objects_above_threshold_with_no_arguments(self, mock_cache_get):
        n = 5
        objects = [MyModelMock(i) for i in range(n)]
        mock_cache_get.side_effect = [x*10 for x in range(n)]
        qs = QuerySetMock(objects)

        calls = []
        for i in range(n):
            calls.append(call('rank_MyModelMock_{}'.format(i), 0))

        result = get_greater(qs, 20)

        mock_cache_get.assert_has_calls(calls)
        self.assertEqual(result, list(reversed(objects[3:])))

    @patch('fb_rank.utils.CACHE.get')
    def test_can_get_objects_above_threshold_with_limit_and_offset(self, mock_cache_get):
        n = 20
        objects = [MyModelMock(i) for i in range(n)]
        mock_cache_get.side_effect = [x*10 for x in range(n)]
        qs = QuerySetMock(objects)

        calls = []
        for i in range(n):
            calls.append(call('rank_MyModelMock_{}'.format(i), 0))

        result = get_greater(qs, 20, limit=10, offset=5)

        mock_cache_get.assert_has_calls(calls)
        self.assertEqual(result, list(reversed(objects))[5:15])
        self.assertNotIn(objects[:3], result)

    @patch('fb_rank.utils.CACHE.get')
    def test_cannot_get_objects_above_threshold_for_empty_queryset(self, mock_cache_get):
        objects = []
        qs = QuerySetMock(objects)

        result = get_greater(qs, 5)

        mock_cache_get.assert_not_called()
        self.assertEqual(result, [])

    @patch('django.conf.settings.FB_ACCESS_TOKEN', 'abc')
    @patch('django.conf.settings.FULL_URL_PREFIX', 'xyz')
    @patch('requests.get')
    @patch('fb_rank.utils.CACHE.set')
    def test_ranking_updates_for_queryset_with_few_objects(self, mock_cache_set, mock_requests_get):
        n = 20
        objects = [MyModelMock(i) for i in range(n)]
        qs = QuerySetMock(objects)

        calls, data = [], {}
        for i in range(n):
            calls.append(call('rank_MyModelMock_{}'.format(i), i*10))
            url = '{}/{}'.format('xyz', i)
            data[url] = {'share': {'share_count': i*10}}

        response = MagicMock()
        response.json = MagicMock(return_value=data)
        mock_requests_get.side_effect = [response]

        update_rank(qs)

        mock_requests_get.assert_called_once()
        mock_cache_set.assert_has_calls(calls, any_order=True)

    @patch('django.conf.settings.FB_ACCESS_TOKEN', 'abc')
    @patch('django.conf.settings.FULL_URL_PREFIX', 'xyz')
    @patch('requests.get')
    @patch('fb_rank.utils.CACHE.set')
    def test_ranking_updates_for_queryset_with_lots_of_objects(self, mock_cache_set, mock_requests_get):
        n = 115
        objects = [MyModelMock(i) for i in range(n)]
        qs = QuerySetMock(objects)
        calls = []
        data = [{}, {}, {}]

        for i in range(n):
            calls.append(call('rank_MyModelMock_{}'.format(i), i+7))
            idx = i // 50
            url = '{}/{}'.format('xyz', i)
            data[idx][url] = {'share': {'share_count': i+7}}

        responses = [MagicMock(), MagicMock(), MagicMock()]
        responses[0].json = MagicMock(return_value=data[0])
        responses[1].json = MagicMock(return_value=data[1])
        responses[2].json = MagicMock(return_value=data[2])
        mock_requests_get.side_effect = responses

        update_rank(qs)

        mock_cache_set.assert_has_calls(calls, any_order=True)
        self.assertEqual(mock_requests_get.call_count, 3)

    @patch('django.conf.settings.FB_ACCESS_TOKEN', 'abc')
    @patch('django.conf.settings.FULL_URL_PREFIX', 'xyz')
    @patch('requests.get')
    @patch('fb_rank.utils.CACHE.set')
    def test_ranking_does_not_update_for_empty_queryset(self, mock_cache_set, mock_requests_get):
        objects = []
        qs = QuerySetMock(objects)

        update_rank(qs)

        mock_cache_set.assert_not_called()
        mock_requests_get.assert_not_called()
