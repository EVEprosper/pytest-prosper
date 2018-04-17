"""validate prosper.test_utils.schema_utils"""
import os

import pytest
import helpers

import prosper.test_utils.schema_utils as schema_utils

@pytest.fixture
def mongo_fixture(tmpdir):
    """helper for making testmode mongo context managers

    Args:
        tmpdir: PyTest magic

    Returns:
        schema_utils.MongoContextManager: in tinydb mode

    """
    mongo_context = schema_utils.MongoContextManager(
        helpers.TEST_CONFIG,
        _testmode_filepath=tmpdir,
        _testmode=True,
    )
    return mongo_context


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
            _testmode=True,
            _testmode_filepath=tmpdir,
        )

        with mongo_context as t_mongo:
            t_mongo['test_collection'].insert(self.demo_data)

        with mongo_context as t_mongo:
            data = t_mongo['test_collection'].find_one({'butts': True})

        assert data['many'] == 10

    def test_mongo_context_prodmode(self):
        """test against real mongo"""
        if not helpers.can_connect_to_mongo(helpers.TEST_CONFIG):
            pytest.xfail('no mongo credentials')

        mongo_context = schema_utils.MongoContextManager(
            helpers.TEST_CONFIG,
        )

        with mongo_context as mongo:
            mongo['test_collection'].insert(self.demo_data)

        with mongo_context as _:
            data = mongo['test_collection'].find_one({'butts': True})

        assert data['many'] == 10

FAKE_SCHEMA_TABLE = [
    {'schema_group':'test', 'schema_name':'fake.schema', 'version':'1.0.0',
     'schema':{'result':'NOPE'}},
    {'schema_group':'test', 'schema_name':'fake.schema', 'version':'1.1.0',
     'schema':{'result':'NOPE'}},
    {'schema_group':'test', 'schema_name':'fake.schema', 'version':'1.1.1',
     'schema':{'result':'YUP'}},
    {'schema_group':'not_test', 'schema_name':'fake.schema', 'version':'1.1.2',
     'schema':{'result':'NOPE'}},
]
def test_fetch_latest_version(mongo_fixture):
    """try to find latest schema"""
    collection_name = 'fake_schema_table'

    with mongo_fixture as t_mongo:
        t_mongo[collection_name].insert(FAKE_SCHEMA_TABLE)

    latest_schema = schema_utils.fetch_latest_schema(
        'fake.schema',
        'test',
        helpers.TEST_CONFIG,
        collection_name=collection_name,
        _testmode=True,
        _testmode_filepath=mongo_fixture._testmode_filepath,
    )

    assert latest_schema == {'result': 'YUP'}
