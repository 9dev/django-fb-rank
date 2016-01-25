from django.conf.urls import url, include

from main import urls as main_urls


urlpatterns = [
    url(r'', include(main_urls)),
]
