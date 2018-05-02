"""common test stuff"""
import datetime
import json
import os
import platform
import warnings

import pymongo
import genson

import prosper.common.prosper_config as p_config
from prosper.test_utils.schema_utils import generate_first_run_metadata, generate_schema_from_data

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.join(os.path.dirname(HERE), 'prosper', 'test_utils')

TEST_CONFIG = p_config.ProsperConfig(os.path.join(HERE, 'test.cfg'))
ROOT_CONFIG = p_config.ProsperConfig(os.path.join(ROOT, 'app.cfg'))

def init_schema_database(
        context,
        group_tag,
        name_tag,
        data,
        version,
):
    """generates simple database for test process

    Args:
        context (:obj:`pymongo.collection`): mongo handle for writing to
        group_tag (str): group name of entry
        name_tag (str): name of entry
        data (dict): raw data to genson
        version (str): version to tag

    """
    metadata = generate_first_run_metadata(name_tag, group_tag, version)
    metadata['schema'] = generate_schema_from_data(data, 'DONTCARE')
    metadata['update'] = datetime.datetime.utcnow().isoformat()

    context.insert_one(metadata)

    return metadata

def update_database_name(config, base_name='mongo_test'):
    """creates a database name combining name/py-version

    Makes thread-safe names for test databases

    Args:
        config (:obj:`prosper_config.ProsperConfig`): config object to update
        base_name (str): name of db to connect to

    Returns:
        ProsperConfig: name + pymajor.pyminor + if(dev)

    """
    db_str = '{base_name}_{pymajor}-{pyminor}'.format(
        base_name=base_name,
        pymajor=platform.python_version_tuple()[0],
        pyminor=platform.python_version_tuple()[1],
    )
    if '+' in platform.python_version():
        db_str = db_str + '-dev'


    try:
        config.local_config['MONGO']['database'] = db_str
    except Exception:
        pass
    config.global_config['MONGO']['database'] = db_str

    os.environ['PROSPER_MONGO__database'] = db_str

    return config

TEST_CONFIG = update_database_name(TEST_CONFIG)
ROOT_CONFIG = update_database_name(ROOT_CONFIG)

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
        config=TEST_CONFIG,
):
    """clear out test/dummy data

    WARNING: DELETES TABLES!!!

    Args:
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
    database_name = config.get_option('MONGO', 'database')
    tables = conn[database_name].collection_names()
    print(tables)
    for table in tables:
        print('DROPPING: {}.{}'.format(database_name, table))
        conn[database_name][table].remove()

    conn.close()

def load_schema_from_file(
        filepath,
        root_folder=os.path.join(HERE, 'sample_schemas')
):
    """read json/schema from file and load into program

    Args:
        filepath (str): path to schema file
        root_folder (str): folder path

    Returns:
        dict: JSON parsed schema file

    """
    with open(os.path.join(root_folder, filepath), 'r') as j_fh:
        return json.load(j_fh)
