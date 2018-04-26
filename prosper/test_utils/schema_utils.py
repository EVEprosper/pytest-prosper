"""schema testers"""
import json
import logging
import pathlib

import genson
import pymongo
import semantic_version

from . import _version
ROOT_SCHEMA = pathlib.Path(__file__).parent / 'root_schema.schema'

class MongoContextManager:
    """context manager for mongo connections

    Notes:
        connection_str requires {username}, {password} format strings

    Args:
        config (:obj:`prosper.common.prosper_config.ProsperConfig`): configparser-like object
        database (str): which database to connect to
        log_key (str): name of logger to attach to

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
        schema_name (str): name of schema to track
        schema_group (str): group name for schema lookup
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

    return max(
        schema_list, key=lambda x: semantic_version.Version(x['version'])
    )['schema']
