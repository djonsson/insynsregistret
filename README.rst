===============
Insynsregistret
===============

.. image:: https://api.travis-ci.org/djonsson/insynsregistret.svg?branch=master
    :target: https://travis-ci.org/djonsson/insynsregistret

.. image:: https://codecov.io/gh/djonsson/insynsregistret/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/djonsson/insynsregistret

Introduction
------------
`Insynsregistret <http://insynsok.fi.se>`_  is a Swedish financial registry maintained by the `Swedish Finansinspektionen <http://www.fi.se>`_ (FI). It contains
information regarding insider trading on the Stockholm Stock Exchange (OMX) which is the largest financial market in Sweden.

All insider trading is reported to FI, which publishes the data to this public database. This python library makes it easier to automate data extraction from Insynsregistret.

Please note that this library currently is under development. See the tests for usage instructions.

Usage
-----
::

    #Sets up environment and installs dependencies
    $ make env

    #Activate the environment
    $ . env/bin/activate

    #Shows the list of commands available
    $ make help

      env         create a development environment using virtualenv
      deps        install dependencies
      clean       remove unwanted stuff
      lint        check style with flake8
      test        run all your tests using nose
      production  run test suite and do a release
      release     package and upload a release
      sdist       package


License
-------
Insynsregistret is BSD licensed, so feel free to use it as you like.