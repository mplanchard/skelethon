# -*- coding=utf-8 -*-
"""Common utilities for command-line tools."""

import errno
from functools import partial, wraps
from os import path
from subprocess import Popen
from sys import exit

import click


err_red = partial(click.secho, fg='red', err=True)
err_yellow = partial(click.secho, fg='yellow', err=True)
out_green = partial(click.secho, fg='green')
out_red = partial(click.secho, fg='red')
out_yellow = partial(click.secho, fg='yellow')


TAG_MAP = {
    'dev': '.dev',
    'alpha': 'a',
    'beta': 'b',
    'rc': 'rc',
    'final': '',
    'post': '.post'
}

TAG_VER_PATH = path.abspath(
    path.join(
        path.realpath(path.dirname(__file__)),
        '../.version.json'
    )
)


def run(cmd, **kwargs):
    """Run the specified command interactively with Popen.

    :param Iterable cmd: the command to run
    :param kwargs: keyword arguments to pass to ``Popen``
    """
    proc = Popen(cmd, **kwargs)
    try:
        proc.communicate()
    except KeyboardInterrupt:
        err_red('Aborted!')
        exit(errno.EINTR)


def release_options(func):
    """Decorate a function with click release options."""
    @click.option(
        '--alpha', 'release', flag_value='alpha', help='alpha pre-release'
    )
    @click.option(
        '--beta', 'release', flag_value='beta', help='beta pre-release'
    )
    @click.option(
        '--rc', 'release', flag_value='rc',
        help='release candidate pre-release'
    )
    @click.option(
        '--dev', 'release', flag_value='dev', default=True,
        help='development release (default)'
    )
    @click.option(
        '--post', 'release', flag_value='post', help='post release'
    )
    @click.option(
        '--final', 'release', flag_value='final', help='final release'
    )
    @wraps(func)
    def wrapped(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapped
