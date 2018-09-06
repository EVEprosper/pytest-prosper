Pytest Fixtures
===============

Half of the power of PyTest is its `Fixtures`_.  ``pytest-prosper`` comes with some baked-in features that every Prosper project should find useful.

Secret Management
-----------------

Secret management is challenging, but `prosper.common.prosper_cli`_ has a built in ``--secret-cfg`` and these fixtures mimic that api.

.. code-block:: cfg

    pytest.ini
    [pytest]
    config_path = path/to/app.cfg

.. code-block:: bash

    python setup.py test --secret-cfg=secrets.ini

.. code-block:: python

    import pytest

    def test_something_secret(secret_cfg):
        handle = login(
            username=secret_cfg.get_option('credentials', 'username'),
            password=secret_cfg.get_option('credentials', 'password'),
        )

Though the ``app.cfg`` should be in the repository, ``secrets.ini`` should not be.  By providing a ``secrets.ini`` file at test time, secrets can remain unpaired and safe.


.. _Fixtures: https://docs.pytest.org/en/latest/fixture.html
.. _prosper.common.prosper_cli: https://prospercommon.readthedocs.io/en/latest/prosper_cli.html