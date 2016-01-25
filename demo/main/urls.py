from django.conf.urls import url

from main import views


urlpatterns = [
    url(r'^(?P<slug>.*)', views.ItemDetailView.as_view(), name='item_detail'),
]
