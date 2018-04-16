"""common test stuff"""
import os
import platform
import warnings

import pymongo

import prosper.common.prosper_config as p_config

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.join(
    os.path.dirname(HERE), 'prosper', 'test_utils'
)

TEST_CONFIG = p_config.ProsperConfig(os.path.join(HERE, 'test.cfg'))
ROOT_CONFIG = p_config.ProsperConfig(os.path.join(ROOT, 'app.cfg'))

def get_database_name(base_name='mongo_test'):
    """creates a database name combining name/py-version

    Args:
        base_name (str): name of db to connect to

    Returns:
        str: name + pymajor.pyminor + if(dev)

    """
    db_str = '{base_name}_{pymajor}-{pyminor}'.format(
        base_name=base_name,
        pymajor=platform.python_version_tuple()[0],
        pyminor=platform.python_version_tuple()[1],
    )
    if '+' in platform.python_version():
        db_str = db_str + '-dev'

    return db_str

DATABASE_NAME = get_database_name()

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
        print('DROPPING: {}.{}'.format(database_name, table))
        conn[database_name][table].remove()

    conn.close()
