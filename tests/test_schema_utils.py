"""validate prosper.test_utils.schema_utils"""
import os
import platform

import pytest
import helpers

import prosper.test_utils.schema_utils as schema_utils
def test_00_forcefail():
    print(platform.node())
    print(platform.system())
    print(platform.python_version())
    print(helpers.DATABASE_NAME)
    assert False

class TestMongoContextManager:
    """validate expected behavior for MongoContextManager"""
    demo_data = [
        {'butts': True, 'many': 10},
        {'butts': False, 'many': 100},
    ]
    def test_mongo_context_testmode(self, tmpdir):
        """test with _testmode enabled"""
        mongo_context = schema_utils.MongoContextManager(
            helpers.TEST_CONFIG,
            helpers.DATABASE_NAME,
        )
        mongo_context._testmode = True
        mongo_context._testmode_filepath = tmpdir
        with mongo_context as _:
            _['test_collection'].insert(self.demo_data)

        with mongo_context as _:
            data = _['test_collection'].find_one({'butts': True})

        assert data['many'] == 10

    def test_mongo_context_prodmode(self):
        """test against real mongo"""
        if not helpers.can_connect_to_mongo(helpers.TEST_CONFIG):
            pytest.xfail('no mongo credentials')

        mongo_context = schema_utils.MongoContextManager(
            helpers.TEST_CONFIG,
            helpers.DATABASE_NAME,
        )

        with mongo_context as _:
            _['test_collection'].insert(self.demo_data)

        with mongo_context as _:
            data = _['test_collection'].find_one({'butts': True})

        assert data['many'] == 10
