from django.views.generic import DetailView, ListView

from main.models import Item
from fb_rank.utils import get_top, get_greater


class ItemDetailView(DetailView):
    model = Item


class TopItemListView(ListView):
    model = Item
    template_name = 'main/top_item_list.html'

    def get_queryset(self):
        qs = super(TopItemListView, self).get_queryset()
        return get_top(qs, limit=5)


class TrendingItemListView(ListView):
    model = Item
    template_name = 'main/trending_item_list.html'

    def get_queryset(self):
        qs = super(TrendingItemListView, self).get_queryset()
        return get_greater(qs, 50)
