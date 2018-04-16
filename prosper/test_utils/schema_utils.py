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
            log_key=_version.__library_name__,
    ):
        self.username = config.get_option('MONGO', 'username')
        self.password = config.get_option('MONGO', 'password')
        self.database = config.get_option('MONGO', 'database')
        self.connection_string = config.get_option('MONGO', 'connection_string')
        self._testmode = False
        self._testmode_filepath = pathlib.Path(__file__).parent
        self.logger = logging.getLogger(log_key)
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
        config,
        collection_name='schemas',
):
    """find latest schema in database

    Args:
        schema_name (str): name of schema to track
        schema_group (str): group name for schema lookup
        config (:obj:`prosper_config.ProsperConfig`): config object with MONGO creds
        collection_name (str): table name with schemas

    Returns:
        dict: jsonschema object with latest version

    """
    pass
