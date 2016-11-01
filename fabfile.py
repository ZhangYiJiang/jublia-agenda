from contextlib import contextmanager as _contextmanager

from fabric.api import *
from fabric.decorators import runs_once

env.hosts = ['52.220.148.170', ]
env.user = 'yijiang'
env.directory = '$HOME/jublia-agenda'
env.activate = 'source $HOME/jublia-agenda/venv/bin/activate'


@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield


@runs_once
def update():
    run('git pull')


def deploy():
    backend()
    frontend()


def frontend():
    with cd(env.directory):
        update()
        # Build frontend
        with cd('frontend'):
            run('npm i --progress false')
            run('npm run build')
            run('rm -rf serve/')
            run('cp -r dist/ serve')


def backend():
    with virtualenv():
        update()
        # Build backend
        run('pip install -q -r requirements.txt')
        run('./manage.py migrate --noinput')
        run('./manage.py collectstatic --noinput')
        # Test
        run('./manage.py test backend.tests')


def createsuperuser():
    with virtualenv():
        run('./manage.py createsuperuser')


def seed(arguments=''):
    with virtualenv():
        run('./manage.py seed ' + arguments)
