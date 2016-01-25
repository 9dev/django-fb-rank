from django.conf.urls import url

from main import views


urlpatterns = [
    url(r'^top$', views.TopItemListView.as_view(), name='top_item_list'),
    url(r'^trending$', views.TrendingItemListView.as_view(), name='trending_item_list'),
    url(r'^(?P<slug>.*)', views.ItemDetailView.as_view(), name='item_detail'),
]
