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

.. |Build Status| image:: https://travis-ci.org/EVEprosper/pytest-prosper.svg?branch=master
    :target: https://travis-ci.org/EVEprosper/pytest-prosper
.. |Coverage Status| image:: https://coveralls.io/repos/github/EVEprosper/pytest-prosper/badge.svg?branch=master
    :target: https://coveralls.io/github/EVEprosper/pytest-prosper?branch=master
.. |PyPI Badge| image:: https://badge.fury.io/py/pytest-prosper.svg
    :target: https://badge.fury.io/py/pytest-prosper
.. |Docs| image:: https://readthedocs.org/projects/pytest-prosper/badge/?version=latest
    :target: http://pytest-prosper.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status