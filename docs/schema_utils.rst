============
schema_utils
============

Many Prosper projects rely on NoSQL sources and backends.  In an effort to signal humans only when there are breaking changes, ProsperTestUtils implements an auto-jsonschema system for tracking data sources and their changes over time.

``prosper.test_utils.schema_helper()`` understands how to manage minor updates (keys added), and will raise exceptions if bigger changes occur.

schema_helper
-------------

.. code-block:: python

    schema_helper(
        data,
        data_source,
        schema_name,
        schema_group,
        config,
    )

Powered by `genson`_, raw JSON data goes in, and a `JSONschema`_ is tested against a MongoDB.  Minor updates and new sources will be handled automatically, but larger changes will raise exceptions.  Also major changes will dump to an update file.

update-prosper-schemas
----------------------

.. code-block:: bash

    git clone git@github.com:EVEprosper/ProsperTestUtils.git
    cd ProsperTestUtils
    pip install -e .
    python setup.py test
    update-prosper-schemas --dump-config > my_config.cfg
    update-prosper-schemas prosper-schema-update_2018-05-14T01/44/17.440168.json --verbose --config=my_config.cfg

When major updates are required, a human needs to push updates to the database.  Just run the test suite and then run ``update-prosper-schemas`` on the dumped .json file.

.. _genson: https://pypi.org/project/genson/