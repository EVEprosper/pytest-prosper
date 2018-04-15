"""who tests the tester's tests?"""
import pytest
import _pytest.outcomes

import prosper.test_utils.docker_utils as docker_utils
import prosper.test_utils.exceptions as exceptions

def test_assert_docker_regular():
    """make sure p_helpers.assert_docker() raises expected error"""
    docker_utils.DOCKER_OK = False
    with pytest.raises(exceptions.DockerNotFound):
        docker_utils.assert_docker()

def test_assert_docker_xfail():
    """make sure p_helpers.assert_docker() raises xfail in mode"""
    docker_utils.DOCKER_OK = False
    with pytest.raises(_pytest.outcomes.XFailed):
        docker_utils.assert_docker(xfail=True)
