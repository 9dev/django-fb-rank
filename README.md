# django-fb-rank

Django app that creates a ranking of objects in your model, based on a number of Facebook shares.

## Installation

- Add `fb_rank` folder to Python path.
- Add `"fb_rank"` to your `INSTALLED_APPS`.
- Update your settings:
    - `CACHES`: You cannot use `LocMemCache` (no cross-process caching is possible with this backend). Optionally you can specify which cache you want to use by adding `FB_RANK_CACHE_NAME` to your settings.
    
            FB_RANK_CACHE_NAME = 'mycache'

    - `FULL_URL_PREFIX`: Default protocol and your domain (without leading slash).
    
            FULL_URL_PREFIX = 'http://www.example.com'
    
    - `FB_ACCESS_TOKEN`: Your Facebook access token (you need Facebook app first).

## Usage

You want to create Facebook shares ranking for one of your models. Obviously, every object need to have its own url, so remember to define `get_absolute_url()` method in your model class.

### Ranking update

In order to create or update ranking of a set of objects you could do the following:

    from fb_rank.utils import update_rank

    qs = MyModel.objects.all()
    update_rank(qs)

Make sure to update this ranking often (you can set up a cron job to do that).

As an example, demo project comes with a custom development command for this purpose:

    $ . ~/.virtualenvs/fb_rank/bin/activate
    $ python demo/manage.py update_rank

### Top objects

To get the most shared objects within a QuerySet:

    from fb_rank.utils import get_top
    
    qs = MyModel.objects.all()
    top_objects = get_top(qs)
    
Optionally you can specify a limit and an offset:

    top_objects = get_top(qs, limit=10, offset=30)

### Objects above some threshold

Sometimes you may only need objects that were shared more than X times. You can grab them using `get_greater()` function.

    from fb_rank.utils import get_greater
    
    qs = MyModel.objects.all()
    popular_objects = get_greater(qs, threshold=100)
    
Again, you can also specify a limit and an offset if you wish.

### Rank of a single object

To get a total number of shares for only one object:

    from fb_rank.utils import get_rank
    
    obj = MyModel()
    rank = get_rank(obj)

Alternatively you can use a templatetag in your templates:

    {% load fb_rank %}
    
    <h1>Total shares: {% get_rank my_object %}</h1>

## Demo

`django-fb-rank` provides a simple demo with example usage. To install it from the console, execute `fab install` command. To run it, type ``fab runserver``.

Of course, to do that you need to have `fabric` installed on your computer.

## Tests

Tests assume that Selenium's ChromeDriver can be found at:
> /usr/bin/chromedriver

It also needs correct permissions. Make sure to run:

    $ sudo chmod a+x /usr/bin/chromedriver

To run all the tests simply type:

    $ fab install
    $ fab testall

## Notes

This package was tested with Python 3.4 and Django 1.8.

## License

MIT
