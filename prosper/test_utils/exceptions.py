"""exceptions for test_utils cases"""
class TestUtilsException(Exception):
    """general exception for prosper.test_utils modules"""
    pass

class DockerUtilsException(TestUtilsException):
    """general exception for docker_utils libraries"""
    pass

class DockerNotFound(DockerUtilsException):
    """cannot find/connect to Docker in environment"""
    pass

class SchemaUtilsException(TestUtilsException):
    """general exception for schema_utils libraries"""
    pass

class UnhandledDiff(SchemaUtilsException):
    """DeepDiff had output, but not handled as change"""
    pass
