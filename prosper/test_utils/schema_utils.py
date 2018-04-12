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
        # username (str): MongoDB Username
        # password (str): MongoDB Password
        database (str): which database to connect to
        # connection_str (str): connection string to platform

    """

    def __init__(self, config, database, config_key='MONGODB', log_key=_version.__library_name__):
        self.username = config.get_option(config_key, 'username')
        self.password = config.get_option(config_key, 'password')
        self.database = database
        self.connection_string = config.get_option(config_key, 'connection_string')
        self._testmode = False
        self._testmode_filepath = pathlib.Path(__file__).parent / 'testdb.json'
        self.logger = logging.getLogger('PROSPER__test_helper')
        # TODO: validate {} in connection_str

    def __get_connector(self):
        """switches between testmode/prod connectors

        Returns:
            pymongo.MongoCollection: connection to mongodb

        """
        if self._testmode:
            import tinymongo
            return tinymongo.TinyMongoClient(self._testmode_filepath)

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
