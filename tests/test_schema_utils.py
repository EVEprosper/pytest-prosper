"""validate prosper.test_utils.schema_utils"""
import os

import pytest
import helpers

import prosper.test_utils.schema_utils as schema_utils

class TestMongoContextManager:
    """validate expected behavior for MongoContextManager"""
    database_name = 'mongo_test'
    demo_data = [
        {'butts': True, 'many': 10},
        {'butts': False, 'many': 100},
    ]
    def test_mongo_context_testmode(self, tmpdir):
        """test with _testmode enabled"""
        mongo_context = schema_utils.MongoContextManager(
            helpers.TEST_CONFIG,
            self.database_name,
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
        if not any([
                helpers.TEST_CONFIG.get_option('MONGO', 'username'),
                helpers.TEST_CONFIG.get_option('MONGO', 'password'),
                helpers.TEST_CONFIG.get_option('MONGO', 'connection_string'),
        ]):
            pytest.xfail('no mongo credentials')

        mongo_context = schema_utils.MongoContextManager(
            helpers.TEST_CONFIG,
            self.database_name,
        )

        with mongo_context as _:
            _['test_collection'].insert(self.demo_data)

        with mongo_context as _:
            data = _['test_collection'].find_one({'butts': True})

        assert data['many'] == 10
