#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='mummify',
    version='0.3.3',
    description='Git + Logging for ML',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
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
    entry_points = {
        'console_scripts': ['mummify=mummify.cli:cli']
    },
    zip_safe=False,
    python_requires='>=3.6',
    setup_requires=['setuptools>=38.6.0']
)
