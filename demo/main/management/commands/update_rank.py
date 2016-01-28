from django.core.management.base import BaseCommand

from fb_rank.utils import update_rank

from main.models import Item


class Command(BaseCommand):
    help = 'Updates Facebook ranking of all Items'

    def handle(self, *args, **options):
        qs = Item.objects.all()
        update_rank(qs)
        self.stdout.write('Successfully updated ranking for model Item')
