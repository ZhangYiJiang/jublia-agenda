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
    with virtualenv():
        # Build backend
        run('git pull')
        run('pip install -q -r requirements.txt')
        run('./manage.py migrate --noinput')
        run('./manage.py collectstatic --noinput')

        # Build frontend
        with cd('frontend'):
            run('npm i --progress false')
            run('npm run build')
            run('rm -rf serve/')
            run('cp -r dist/ serve')


def createsuperuser():
    with virtualenv():
        run('./manage.py createsuperuser')
