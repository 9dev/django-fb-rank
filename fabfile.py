from contextlib import contextmanager
from fabric.api import cd, env, local, prefix, shell_env


VENV_PATH = 'venv'
PYTHON_PATH = '/usr/bin/python3.4'

SETTINGS_MODULE = 'demo.settings'
DEMO_PATH = 'demo'


def install():
    # create virtualenv
    local('rm -rf {}'.format(VENV_PATH))
    local('virtualenv -p {} {}'.format(PYTHON_PATH, VENV_PATH))

    with _venv_local():
        # install requirements
        with cd(DEMO_PATH):
            local('pip install -r {}/requirements.txt'.format(DEMO_PATH))

		# migrate db
        _django_local('makemigrations')
        _django_local('migrate')


def runserver():
    with _venv_local():
        _django_local('runserver')


def updatedb():
    with _venv_local():
        _django_local('makemigrations')
        _django_local('migrate')


def _django_local(command):
    return local(
        'python {}/manage.py {}'.format(DEMO_PATH, command)
    )


@contextmanager
def _venv_local():
    with shell_env(DJANGO_SETTINGS_MODULE=SETTINGS_MODULE):
        with prefix('. %s/bin/activate' % VENV_PATH):
            yield

