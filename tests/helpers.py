"""common test stuff"""
import os
import warnings

import pymongo

import prosper.common.prosper_config as p_config

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.join(
    os.path.dirname(HERE), 'prosper', 'test_utils'
)

TEST_CONFIG = p_config.ProsperConfig(os.path.join(HERE, 'test.cfg'))
ROOT_CONFIG = p_config.ProsperConfig(os.path.join(ROOT, 'app.cfg'))

DATABASE_NAME = 'mongo_test'

def can_connect_to_mongo(config):
    """returns true/false whether mongo is available

    Args:
        config (:obj:`prosper_config.ProsperConfig`): configparser with `MONGO` keys

    Returns:
        bool: can connect to mongo

    """
    if not any([
            config.get_option('MONGO', 'username'),
            config.get_option('MONGO', 'password'),
            config.get_option('MONGO', 'connection_string'),
    ]):
        return False

    # TODO: connect to prod mongo with keys, raise if keys are bad
    return True

def clear_mongo_test_db(
        database_name=DATABASE_NAME,
        config=TEST_CONFIG,
):
    """clear out test/dummy data

    WARNING: DELETES TABLES!!!

    Args:
        database_name (str): name of database to clear out
        config (:obj:`prosper_config.ProsperConfig`): configpaser with `MONGO` keys

    """
    if not can_connect_to_mongo(config):
        return

    conn = pymongo.MongoClient(
        config.get_option('MONGO', 'connection_string').format(
            username=config.get_option('MONGO', 'username'),
            password=config.get_option('MONGO', 'password'),
        )
    )
    tables = conn[database_name].collection_names()
    print(tables)
    for table in tables:
        conn[database_name][table].remove()

    conn.close()
