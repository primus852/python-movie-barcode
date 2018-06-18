# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pmb',
    version='0.1.0',
    description='Create a Movie Barcode of any given videofile',
    long_description=readme,
    author='Torsten Wolzer',
    author_email='findnibbler@gmail.com',
    url='https://github.com/primus852/python-movie-barcode',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

