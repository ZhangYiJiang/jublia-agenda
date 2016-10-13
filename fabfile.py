from fabric.api import *
from contextlib import contextmanager as _contextmanager

env.hosts = ['52.220.148.170', ]
env.user = 'yijiang'
env.directory = '$HOME/jublia-agenda'
env.activate = 'source $HOME/jublia-agenda/venv/bin/activate'


@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield


def deploy():
    backend()
    frontend()


def frontend():
    with cd(env.directory):
        run('git pull')
        # Build frontend
        with cd('frontend'):
            run('npm i --progress false')
            run('npm run build')
            run('rm -rf serve/')
            run('cp -r dist/ serve')


def backend():
    with virtualenv():
        run('git pull')
        # Build backend
        run('pip install -q -r requirements.txt')
        run('./manage.py migrate --noinput')
        run('./manage.py collectstatic --noinput')


def createsuperuser():
    with virtualenv():
        run('./manage.py createsuperuser')
