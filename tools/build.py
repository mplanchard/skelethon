#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build a package distribution, with easy pre/post versioning."""

from __future__ import absolute_import

import json
from os import path

import click

from _common import TAG_MAP, TAG_VER_PATH, release_options, run


def tag_version(release):
    """Get the tag version for the specified release.

    :param str release: the release (e.g. dev)
    """
    if release == 'final':
        return ''

    with open(TAG_VER_PATH) as tagfile:
        vers = json.load(tagfile)
    return vers[release]


@click.command(context_settings={'ignore_unknown_options': True})
@click.argument('setup_args', nargs=-1, type=click.UNPROCESSED)
@release_options
def cli(release, setup_args):
    """Build a Python package, applying release modifiers as desired.

    The release modifier chosen from the options below will determine
    the build tag in accordance with PEP 440. Any additional arguments
    will be passed directly to setup.py.

    Note that only **one** release modifier at a time may be specified.
    If multiple modifiers are provided, the last one will be used.

    Examples:

    To build a wheel with the "rc" version tag:

    \b
        tools/build.py --rc bdist_wheel

    To build a source dist as well:

    \b
        tools/build.py --rc bdist_wheel sdist

    To build a post-release (with the "post" version tag):

    \b
        tools/build.py --post bdist_wheel

    """
    setup = path.abspath(
        path.join(
            path.realpath(path.dirname(__file__)),
            '../setup.py'
        )
    )
    cmd = (
        'python',
        setup,
        'egg_info',
        '--tag-build',
        '{}{}'.format(TAG_MAP[release], tag_version(release)),
        *setup_args,
    )
    run(cmd)


if __name__ == '__main__':
    cli()  # pylint: disable=E1120
