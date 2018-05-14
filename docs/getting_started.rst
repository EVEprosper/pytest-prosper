===============
Getting Started
===============

ProsperTestUtils is a simple Python library compatable with >=3.5.  

This collection is designed to help:

- Test case development
- Production environment helpers

Most application should use this library as a ``tests_require`` rather than directly ``pip install prospertestutils``

.. code-block:: python

    # setup.py
    setup(
        ...
        tests_require=[
            'pytest',
            'prospertestutils',
            ...
        ],
    )

Plugin Development
------------------

Functionality is separated by family.  Utilities should be built with an easy-to-use API and split into easy-to-test units.  

Testing
-------

.. code-block:: bash

    python setup.py test

Testing powered by `PyTest`_

Documentation
-------------

.. code-block:: bash

    pip install .[dev]
    sphinx-apidoc -f -o docs/source prosper/test_utils
    sphinx-build -b html docs/ webpage/
