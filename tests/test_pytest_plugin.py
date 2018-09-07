"""validates pytest plugins work as expected"""

import os

CONFIG_FILE = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'dummy_cfg.cfg'
)
SECRET_FILE = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'dummy_secrets.cfg'
)

class TestSecretConfig:
    """test --secret-cfg behavior"""
    def test_secret_config_happypath(self, testdir):
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

    def test_secret_config_strict(self, testdir):
        """validate --secret-strict behavior"""
        testdir.makeini(f"""
            [pytest]
            config_path = {CONFIG_FILE}
        """)

        testdir.makepyfile(f"""

            import pytest
            def test_secret_cfg(secret_cfg):
                assert secret_cfg.get_option('section', 'secret') == 'princess'

        """)

        result = testdir.runpytest(f'--secret-strict')
        assert result.parseoutcomes()['xfailed'] == 1

    def test_secret_config_empty(self, testdir):
        """validate fall-through case for blank --secret-cfg"""
        testdir.makeini(f"""
            [pytest]
            config_path = {CONFIG_FILE}
        """)

        testdir.makepyfile(f"""

            import pytest
            def test_secret_cfg(secret_cfg):
                assert secret_cfg.get_option('section', 'value') == 'butts'
                assert secret_cfg.get_option('section', 'secret') == None

        """)

        result = testdir.runpytest()
        print(result.parseoutcomes())
        assert result.ret == 0

def test_regular_config(testdir):
    """validate config fixture"""
    testdir.makeini(f"""
        [pytest]
        config_path = {CONFIG_FILE}
    """)

    testdir.makepyfile(f"""

        import pytest
        def test_config(config):
            assert config.get_option('section', 'value') == 'butts'

    """)

    result = testdir.runpytest()
    assert result.ret == 0
