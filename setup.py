import os
from setuptools import setup


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-fb-rank',
    version='0.1',
    packages=['fb_rank'],
    include_package_data=True,
    license='MIT License',
    description='Django app that creates a ranking of objects in your model, based on a number of Facebook shares.',
    long_description=README,
    url='https://github.com/9dev/django-fb-rank',
    author='9dev',
    author_email='9devmail@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'django >= 1.8',
        'requests',
    ],
)
