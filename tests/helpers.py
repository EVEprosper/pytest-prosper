"""common test stuff"""

import os

import prosper.common.prosper_config as p_config

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.join(
    os.path.dirname(HERE), 'prosper', 'test_utils'
)

TEST_CONFIG = p_config.ProsperConfig(os.path.join(HERE, 'test.cfg'))
ROOT_CONFIG = p_config.ProsperConfig(os.path.join(ROOT, 'app.cfg'))
