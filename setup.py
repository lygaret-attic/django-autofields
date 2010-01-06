#!/usr/bin/env python

from distutils.core import setup

setup(
        name='django-autofields',
        version='0.1',
        description='Django auto-populating fields',
        author='Jon Raphaelson',
        author_email='jonraphaelson@gmail.com',
        url='http://www.github.com/lygaret/django-autofields',
        packages=['autofields', 'autofields.fields']
)
