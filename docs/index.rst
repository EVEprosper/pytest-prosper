.. ProsperTestUtils documentation master file, created by
   sphinx-quickstart on Sat Mar 31 13:38:57 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==============
Pytest-Prosper
==============

|Build Status| |Coverage Status| |PyPI Badge| |Docs|

Helper libraries for test coverage and general maintenance of services.  Making test coverage easier across Prosper projects!

Quickstart
==========

.. code-block:: python

    setup(
        ...
        tests_require=[
            'pytest-prosper',
        ]
    )

Pytest-Prosper is suggested as a ``tests_require`` install.  Though there are some general use utilities, this library is not meant for production use.

Index
=====

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started.rst
   schema_utils.rst

API Reference
=============

.. toctree::
    :maxdepth: 2
 
    source/test_utils.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |Build Status| image:: https://travis-ci.org/EVEprosper/ProsperTestUtils.svg?branch=master
   :target: https://travis-ci.org/EVEprosper/ProsperTestUtils
.. |Coverage Status| image:: https://coveralls.io/repos/github/EVEprosper/ProsperTestUtils/badge.svg?branch=master
   :target: https://coveralls.io/github/EVEprosper/ProsperTestUtils?branch=master
.. |PyPI Badge| image:: https://badge.fury.io/py/ProsperTestUtils.svg
   :target: https://badge.fury.io/py/ProsperTestUtils
.. |Docs| image:: https://readthedocs.org/projects/prospertestutils/badge/?version=latest
