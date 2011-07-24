# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

from setuptools import setup, find_packages
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
HISTORY = open(os.path.join(here, 'HISTORY.txt')).read()
version = open(os.path.join(here, 'version.txt')).read().strip()


setup(
    name='nagiosplugin',
    version=open('version.txt').read().strip(),
    description='Class library for writing Nagios (Icinga) plugins',
    long_description=README + '\n\n' + HISTORY,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Zope Public License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Monitoring',
    ],
    keywords='Nagios Icinga plugin check monitoring',
    author='Christian Kauhaus',
    author_email='kc@gocept.com',
    url='http://projects.gocept.com/projects/projects/nagiosplugin/wiki',
    download_url='http://pypi.python.org/pypi/nagiosplugin',
    license='ZPL',
    install_requires=[
        'mock',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={'': ['*.txt', '*.rst']},
    include_package_data=True,
    zip_safe=False,
    test_suite='nagiosplugin.tests',
    entry_points={
        'console_scripts': [
            'check_http = nagiosplugin.examples.check_http:main',
        ],
    },
)
