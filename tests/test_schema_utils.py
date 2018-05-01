"""validate prosper.test_utils.schema_utils"""
import datetime
import json
import jsonschema
import pathlib

import pytest
import helpers

import prosper.test_utils.schema_utils as schema_utils
import prosper.test_utils.exceptions as exceptions


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

class TestFetchLatestSchema:
    """validate expected behavior for fetch_latest_schema()"""
    fake_schema_table = [
        {'schema_group':'test', 'schema_name':'fake.schema', 'version':'1.0.0',
         'schema':{'result':'NOPE'}},
        {'schema_group':'test', 'schema_name':'fake.schema', 'version':'1.1.0',
         'schema':{'result':'NOPE'}},
        {'schema_group':'test', 'schema_name':'fake.schema', 'version':'1.1.1',
         'schema':{'result':'YUP'}},
        {'schema_group':'not_test', 'schema_name':'fake.schema', 'version':'1.1.2',
         'schema':{'result':'NOPE'}},
    ]
    def test_fetch_latest_version(self, mongo_fixture):
        """try to find latest schema"""
        collection_name = 'fake_schema_table'

        with mongo_fixture as t_mongo:
            t_mongo[collection_name].insert(self.fake_schema_table)

        with mongo_fixture as t_mongo:
            latest_schema = schema_utils.fetch_latest_schema(
                'fake.schema',
                'test',
                t_mongo[collection_name]
            )

        assert latest_schema['schema'] == {'result': 'YUP'}
        assert latest_schema['version'] == '1.1.1'

    def test_fetch_latest_version_empty(self, mongo_fixture):
        """make sure function returns expected for no content"""
        collection_name = 'blank_schema_table'

        with pytest.warns(exceptions.FirstRunWarning):
            with mongo_fixture as t_mongo:
                latest_schema = schema_utils.fetch_latest_schema(
                    'fake.schema',
                    'test',
                    t_mongo[collection_name]
                )

        assert latest_schema['schema'] == {}
        assert latest_schema['version'] == '1.0.0'

class TestCompareSchemas:
    """validate expected behavior for compare_schemas()"""
    base_schema = helpers.load_schema_from_file('base_schema.json')
    minor_change = helpers.load_schema_from_file('minor_schema_change.json')
    major_removed_value = helpers.load_schema_from_file('major_items_removed.json')
    major_values_changed = helpers.load_schema_from_file('major_values_changed.json')
    unhandled_diff = set(helpers.load_schema_from_file('unhandled_diff.json'))

    def test_compare_schemas_happypath(self):
        """make sure equivalence works as expected"""
        status = schema_utils.compare_schemas(
            self.base_schema,
            self.base_schema
        )

        assert status == schema_utils.Update.no_update

    def test_compare_schemas_minor(self):
        """make sure minor updates are tagged as such"""
        status = schema_utils.compare_schemas(
            self.base_schema,
            self.minor_change
        )

        assert status == schema_utils.Update.minor

    def test_compare_schemas_major(self):
        """make sure major updates are tagged as such"""
        status = schema_utils.compare_schemas(
            self.base_schema,
            self.major_removed_value
        )

        assert status == schema_utils.Update.major

        status = schema_utils.compare_schemas(
            self.base_schema,
            self.major_values_changed
        )

        assert status == schema_utils.Update.major

    def test_compare_schemas_empty(self):
        """make sure empty case signals first-run"""
        status = schema_utils.compare_schemas(
            {},
            self.base_schema,
        )

        assert status == schema_utils.Update.first_run

    def test_compare_schemas_error(self):
        """make sure raises for really screwed up case"""
        pytest.xfail('compare_schemas raise case not working yet')
        with pytest.raises(exceptions.UnhandledDiff):
            status = schema_utils.compare_schemas(
                self.base_schema,
                self.unhandled_diff
            )

class TestBuildMetadata:
    """validate expected behavior for build_metadata()"""
    fake_metadata = {
        'schema_group': 'fake_group',
        'schema_name': 'fake_name',
        'update': datetime.datetime.utcnow().isoformat(),
        'version': '1.2.1',
        'schema': {'type': 'DONTCARE'},
    }
    dummy_schema = {'fake': 'DONTCARE'}

    def test_build_schema_no_update(self):
        """assert behavior for no_update"""
        metadata = schema_utils.build_metadata(
            self.dummy_schema,
            self.fake_metadata,
            schema_utils.Update.no_update,
        )
        assert metadata == self.fake_metadata

    def test_build_schema_first_run(self):
        """assert behavior for first_run"""
        metadata = schema_utils.build_metadata(
            self.dummy_schema,
            self.fake_metadata,
            schema_utils.Update.first_run,
        )

        assert metadata['schema'] == self.dummy_schema
        assert metadata['update'] != self.fake_metadata['update']
        assert metadata['version'] == self.fake_metadata['version']

    def test_build_schema_minor(self):
        """assert behavior for minor update"""
        metadata = schema_utils.build_metadata(
            self.dummy_schema,
            self.fake_metadata,
            schema_utils.Update.minor,
        )

        assert metadata['schema'] == self.dummy_schema
        assert metadata['update'] != self.fake_metadata['update']
        assert metadata['version'] == '1.2.2'

    def test_build_schema_major(self):
        """assert behavior for major update"""
        metadata = schema_utils.build_metadata(
            self.dummy_schema,
            self.fake_metadata,
            schema_utils.Update.major,
        )

        assert metadata['schema'] == self.dummy_schema
        assert metadata['update'] != self.fake_metadata['update']
        assert metadata['version'] == '1.3.0'

    def test_build_schema_badschema(self):
        """assert behavior for bad schema"""
        dummy_meta = {
            'schema': '',
            'version': '1.0.0',
            'update': datetime.datetime.utcnow().isoformat(),
        }

        with pytest.raises(jsonschema.exceptions.ValidationError):
            metadata = schema_utils.build_metadata(
                self.dummy_schema,
                dummy_meta,
                schema_utils.Update.first_run
            )

class TestDumpMajorUpdate:
    """validate expected behavior for dump_major_update()"""

    dummy_metadata1 = {'butts': 'yes'}
    dummy_metadata2 = {'butts': 'no'}
    def test_dump_major_udpate_empty(self, tmpdir):
        """validate system doesn't raise for empty data"""
        filename = pathlib.Path(tmpdir) / 'empty.json'
        schema_utils.dump_major_update(
            self.dummy_metadata1,
            filename,
        )

        with open(str(filename), 'r') as tmp_fh:
            saved_data = json.load(tmp_fh)

        assert saved_data[0] == self.dummy_metadata1


    def test_dump_major_update_exists(self, tmpdir):
        """validate system appends new metadata to report"""
        filename = pathlib.Path(tmpdir) / 'exists.json'
        with open(str(filename), 'w') as tmp_fh:
            json.dump([self.dummy_metadata1], tmp_fh)

        schema_utils.dump_major_update(
            self.dummy_metadata2,
            filename,
        )

        with open(str(filename), 'r') as tmp_fh:
            saved_data = json.load(tmp_fh)

        assert saved_data[1] == self.dummy_metadata2
