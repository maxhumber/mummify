#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='mummify',
    version='0.0.3',
    description='Automatic ML Logging',
    long_description=readme(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Version Control',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    url='https://github.com/maxhumber/mummify',
    author='Max Humber',
    author_email='max.humber@gmail.com',
    license='MIT',
    packages=['mummify'],
    install_requires=[
        'markdown',
        'pandas',
        'fire'
    ],
    entry_points = {
        'console_scripts': ['mummify=mummify.cli:cli']
    },
    include_package_data=True,
    zip_safe=False
)
