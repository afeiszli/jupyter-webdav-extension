#!/usr/bin/env python

import re
import os

from setuptools import setup, find_packages


def _get_requirements(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path) as f:
            packages = f.read().splitlines()
    except (IOError, OSError) as ex:
        raise RuntimeError("Can't open file with requirements: %s", repr(ex))
    packages = (p.strip() for p in packages if not re.match("^\s*#", p))
    packages = list(filter(None, packages))
    return packages


def _install_requirements():
    requirements = _get_requirements('requirements.txt')
    return requirements

setup(
    name='webdav_service',
    version='0.0.1',
    description='JupyterHub service to add a public route for webdav within a notebook server',
    author='Alex Feiszli',
    author_email='alex.feiszli@gmail.com',
    url='https://github.com/afeiszli/jupyter-webdav-extension',
    license="GPL3",
    entry_points={
        'console_scripts': ['jupyter_webdav_service=webdav_service.webdav_service:run'],
    },
    packages=find_packages(),
    install_requires=_install_requirements()
)
