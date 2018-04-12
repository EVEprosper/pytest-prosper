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
        config_key (str): section name for ConfigParser
        log_key (str): name of logger to attach to

    """

    def __init__(
            self,
            config,
            database,
            config_key='MONGODB',
            log_key='PROSPER__' + _version.__library_name__
    ):
        self.username = config.get_option(config_key, 'username')
        self.password = config.get_option(config_key, 'password')
        self.database = database
        self.connection_string = config.get_option(config_key, 'connection_string')
        self._testmode = False
        self._testmode_filepath = pathlib.Path(__file__).parent / 'testdb.json'
        self.logger = logging.getLogger(log_key)
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
