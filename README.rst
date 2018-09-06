|Show Logo|

Pytest-Prosper
==============

|Build Status| |Coverage Status| |PyPI Badge| |Docs| |Gitter|

Helper libraries for test coverage and general maintenance of services.  Making test coverage easier across Prosper projects!

Quickstart
----------

.. code-block:: python

    setup(
        ...
        tests_require=[
            'pytest-prosper',
        ]
    )

Pytest-Prosper is suggested as a ``tests_require`` install.  Though there are some general use utilities, this library is not meant for production use.

Features
--------

`schema_utils`_
~~~~~~~~~~~~~~~

NoSQL is a powerful tool for web scraping, but can be difficult to keep traditional DBA tools running on.  Get alerted when major updates to data feeds occur without having to hand-craft JSONschemas for every source.

PyTest Fixtures
~~~~~~~~~~~~~~~

- ``--secret-cfg``: supports passing a secret template to a config file.  Supports `prosper.common.prosper_cli`_ secret management

- ``secret_cfg``: passes a config object with secrets filled out

- ``config``: passes a config object (no secrets)

- ``config_file``: a ``pytest.ini`` option to source the correct configuration file


.. |Show Logo| image:: http://dl.eveprosper.com/podcast/logo-colour-17_sm2.png
    :target: http://eveprosper.com
.. |Build Status| image:: https://travis-ci.org/EVEprosper/pytest-prosper.svg?branch=master
    :target: https://travis-ci.org/EVEprosper/pytest-prosper
.. |Coverage Status| image:: https://coveralls.io/repos/github/EVEprosper/pytest-prosper/badge.svg?branch=master
    :target: https://coveralls.io/github/EVEprosper/pytest-prosper?branch=master
.. |PyPI Badge| image:: https://badge.fury.io/py/pytest-prosper.svg
    :target: https://badge.fury.io/py/pytest-prosper
.. |Docs| image:: https://readthedocs.org/projects/pytest-prosper/badge/?version=latest
    :target: http://pytest-prosper.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. |Gitter| image:: https://badges.gitter.im/Join%20Chat.svg
    :alt: Join the chat at https://gitter.im/EVEProsper/Lobby
    :target: https://gitter.im/EVEProsper/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
.. _schema_utils: http://pytest-prosper.readthedocs.io/en/latest/schema_utils.html
.. _prosper.common.prosper_cli: https://prospercommon.readthedocs.io/en/latest/prosper_cli.html
