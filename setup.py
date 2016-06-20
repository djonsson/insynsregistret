#! ../env/bin/python

import os
import sys
import insynsregistret

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

README = open('README.rst').read()
LICENSE = open("LICENSE").read()

setup(
    name='insynsregistret',
    version=insynsregistret.__version__,
    description='A client for the Swedish insynsregistret',
    long_description=(README),
    license=LICENSE,
    author='Daniel Jonsson',
    author_email='wd.jonsson@gmail.com',
    url='https://github.com/djonsson/insynsregistret',
    install_requires=[''],
    packages=['insynsregistret'],
    include_package_data=True,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ),
    keywords='insynsregustret, insider trading, finansinspektionen, omx',
    tests_require=['nose'],
    test_suite='tests',
)