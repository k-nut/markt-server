import os

from fabric.api import local
from fabric.api import env
from fabric.api import warn_only
from fabric.api import cd
from fabric.operations import run, sudo

def pull_latest_version():
    with cd('/home/knut/markt-server'):
        run('git pull git@github.com:k-nut/markt-server.git')
    sudo('service markt-server restart')


def deploy():
    pull_latest_version()
