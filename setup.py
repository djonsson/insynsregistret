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

setup(
    name='insynsregistret',
    version=insynsregistret.__version__,
    description='A client for the Swedish insynsregistret',
    long_description=(README),
    license='BSD',
    author='Daniel Jonsson',
    author_email='wd.jonsson@gmail.com',
    url='https://github.com/djonsson/insynsregistret',
    install_requires=[''],
    packages=['insynsregistret'],
    include_package_data=True,
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Topic :: Office/Business :: Financial',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ),
    keywords='insynsregistret, insider trading, finansinspektionen, omx',
    tests_require=['nose'],
    test_suite='tests',
)
