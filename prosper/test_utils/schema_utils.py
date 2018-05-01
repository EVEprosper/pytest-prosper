"""schema testers"""
import copy
import datetime
import enum
import json
import logging
import pathlib
import warnings

import deepdiff
import genson
import jsonschema
import pymongo
import semantic_version

from . import _version
from . import exceptions

with open(str(pathlib.Path(__file__).parent / 'root_schema.schema'), 'r') as schema_fh:
    ROOT_SCHEMA = json.load(schema_fh)


class Update(enum.Enum):
    """enum for classifying what kind of update is required"""
    first_run = 'first_run'
    major = 'major'
    minor = 'minor'
    no_update = 'no_update'


class MongoContextManager:
    """context manager for mongo connections

    Notes:
        connection_str requires {username}, {password} format strings

    Args:
        config (:obj:`prosper.common.prosper_config.ProsperConfig`): configparser-like object
        _testmode (bool): use a localdb rather than a prod one
        _testmode_filepath (str): path to localdb

    """

    def __init__(
            self,
            config,
            _testmode=False,
            _testmode_filepath=pathlib.Path(__file__).parent,
    ):
        self.username = config.get_option('MONGO', 'username')
        self.password = config.get_option('MONGO', 'password')
        self.database = config.get_option('MONGO', 'database')
        self.connection_string = config.get_option('MONGO', 'connection_string')
        self._testmode = _testmode
        self._testmode_filepath = _testmode_filepath
        # TODO: validate {} in connection_str

    def __get_connector(self):
        """switches between testmode/prod connectors

        Returns:
            pymongo.MongoCollection: connection to mongodb

        """
        if self._testmode:
            import tinymongo
            return tinymongo.TinyMongoClient(foldername=str(self._testmode_filepath))

        return pymongo.MongoClient(
            self.connection_string.format(
                username=self.username,
                password=self.password,
            )
        )

    def __enter__(self):
        """with MongoContextManager() entrypoint"""
        self.connection = self.__get_connector()
        return self.connection[self.database]

    def __exit__(self, *exc):
        """with MongoContextManager() exitpoint"""
        self.connection.close()


def fetch_latest_schema(
        schema_name,
        schema_group,
        mongo_collection,
):
    """find latest schema in database

    Args:
        schema_name (str): data source name
        schema_group (str): datas source group
        mongo_collection (:obj:`pymongo.collection`): db connection handle

    Returns:
        dict: jsonschema object with latest version

    """
    schema_list = list(mongo_collection.find({
        '$and':[
            {'schema_name': schema_name},
            {'schema_group': schema_group},
        ],
    }))
    if not schema_list:
        warnings.warn(
            '{}.{} schema not in database -- creating fresh entry'.format(
                schema_group, schema_name),
            exceptions.FirstRunWarning
        )
        return dict(
            schema_group=schema_group,
            schema_name=schema_name,
            update='',
            version='1.0.0',
            schema={},
        )
    return max(
        schema_list, key=lambda x: semantic_version.Version(x['version'])
    )

def compare_schemas(
        sample_schema,
        current_schema,
):
    """compare 2 jsonschemas and look for changes.  Checks required[] keys

    Notes:
        Update.minor: added required keys, but did not remove anything
        Update.major: removed required keys or otherwise changed structure
        Update.no_update: schemas are identical

    Args:
        sample_schema (dict): incomming schema to validate
        current_schema (dict): current schema from database

    Returns:
        Update: update status of comparison

    """
    if not sample_schema:
        return Update.first_run

    diff = deepdiff.DeepDiff(sample_schema, current_schema)

    is_minor = any([
        'dictionary_item_added' in diff,
    ])
    is_major = any([
        'dictionary_item_removed' in diff,
        'values_changed' in diff,
        'type_changes' in diff,  # is minor?
        'iterable_item_removed' in diff
    ])

    if is_major:
        return Update.major
    if is_minor:
        return Update.minor
    if diff:
        raise exceptions.UnhandledDiff(diff)

    return Update.no_update

def build_schema(
        schema,
        current_metadata,
        update_type,
):
    """build updated schema

    Args:
        schema (dict): jsonschema for data source
        current_metadata (dict): current table entry frame
        update_type (enum): what kind of update to perform

    Returns:
        dict: updated current_metadata

    """
    updated_metadata = copy.deepcopy(current_metadata)
    if any([
            update_type == Update.first_run,
            update_type == Update.minor,
            update_type == Update.major,
    ]):
        updated_metadata['schema'] = schema
        updated_metadata['update'] = datetime.datetime.utcnow().isoformat()

    current_version = semantic_version.Version(current_metadata['version'])
    if update_type == Update.minor:
        updated_metadata['version'] = str(current_version.next_patch())
    elif update_type == Update.major:
        updated_metadata['version'] = str(current_version.next_minor())

    jsonschema.validate(updated_metadata, ROOT_SCHEMA)

    return updated_metadata

