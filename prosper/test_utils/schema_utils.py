"""schema testers"""
import json
import logging
import pathlib


import genson
import pymongo
import semantic_version


ROOT_SCHEMA = pathlib.Path(__file__).parent / 'root_schema.schema'

class MongoContextManager:
    """context manager for mongo connections

    Notes:
        connection_str requires {username}, {password} format strings

    Args:
        username (str): MongoDB Username
        password (str): MongoDB Password
        connection_str (str): connection string to platform

    """
    logger = logging.getLogger('PROSPER__test_helper')
    def __init__(self, username, password, connection_str):
        self.username = username
        self.password = password
        self.connection_str = connection_str
        self._testmode = False
        self._testmode_filepath = pathlib.Path(__file__).parent / 'testdb.json'

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
            self.connection_str.format(
                username=self.username,
                password=self.password,
            )
        )

    def __enter__(self):
        """with MongoContextManager() entrypoint"""
        self.connection = self.__get_connector()
        return self.connection

    def __exit__(self, *exc):
        """with MongoContextManager() exitpoint"""
        self.connection_str.close()
