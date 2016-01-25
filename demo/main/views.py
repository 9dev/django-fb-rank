from django.views.generic import DetailView

from main.models import Item


class ItemDetailView(DetailView):
    model = Item
