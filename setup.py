#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='mummify',
    version='0.3.0',
    description='Git + Logging for ML',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
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
    entry_points = {
        'console_scripts': ['mummify=mummify.cli:cli']
    },
    zip_safe=False,
    python_requires='>=3.6'
)
