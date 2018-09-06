"""validates pytest plugins work as expected"""

import os

CONFIG_FILE = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'dummy_cfg.cfg'
)
SECRET_FILE = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'dummy_secrets.cfg'
)

def test_secret_config(testdir):
    """validate secret_config fixture"""
    testdir.makeini(f"""
        [pytest]
        config_path = {CONFIG_FILE}
    """)

    testdir.makepyfile(f"""

        import pytest
        def test_secret_cfg(secret_cfg):
            assert secret_cfg.get_option('section', 'secret') == 'princess'

    """)

    result = testdir.runpytest(f'--secret-cfg={SECRET_FILE}')
    assert result.ret == 0

