"""plugins for prosper projects/tests"""

import pytest

import prosper.common.prosper_config as p_config

def pytest_addoption(parser):
    """configure pytest cli args and ini args"""
    group = parser.getgroup('prosper')
    group.addoption(
        '--secret-cfg',
        action='store',
        dest='secret_filepath',
        default='',
        help='path to secret config template values',
    )

    parser.addini('config_path', 'Path to default app.cfg file')

@pytest.fixture
def secret_cfg(request):
    """yield a config with secrets applied

    Returns:
        prosper.config.ProsperConfig: configuration object with secrets applied

    """
    return p_config.render_secrets(
        request.config.getini('config_path'),
        request.config.option.secret_filepath,
    )

@pytest.fixture
def config(request):
    """yield a raw config.  No secrets

    Returns
        prosper.config.ProsperConfig: configuration object without secrets

    """
    return p_config.ProsperConfig(
        request.config.getini('config_path'),
    )
