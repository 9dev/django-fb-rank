from django.core.urlresolvers import reverse
from django.db import models


class Item(models.Model):
    slug = models.CharField(max_length=100, primary_key=True, blank=True)
    name = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('item_detail', kwargs={'slug': self.slug})
