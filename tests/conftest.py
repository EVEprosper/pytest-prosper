"""conftest: pytest configuration"""
import helpers

helpers.clear_mongo_test_db()

pytest_plugins = ['pytester']
