"""who tests the tester's tests?"""
import pytest
import _pytest.outcomes

import prosper.common.test_helpers as p_helpers
import prosper.common.exceptions as exceptions

def test_assert_docker_regular():
    """make sure p_helpers.assert_docker() raises expected error"""
    p_helpers.DOCKER_OK = False
    with pytest.raises(exceptions.DockerNotFound):
        p_helpers.assert_docker()

def test_assert_docker_xfail():
    """make sure p_helpers.assert_docker() raises xfail in mode"""
    p_helpers.DOCKER_OK = False
    with pytest.raises(_pytest.outcomes.XFailed):
        p_helpers.assert_docker(xfail=True)
