from django.conf.urls import url
from django.views.decorators.cache import cache_page

from main import views


CACHE_TIME = 60


urlpatterns = [
    url(
        r'^top$',
        cache_page(CACHE_TIME)(views.TopItemListView.as_view()),
        name='top_item_list'
    ),
    url(
        r'^trending$',
        cache_page(CACHE_TIME)(views.TrendingItemListView.as_view()),
        name='trending_item_list'
    ),
    url(
        r'^(?P<slug>.*)',
        cache_page(CACHE_TIME)(views.ItemDetailView.as_view()),
        name='item_detail'
    ),
]
