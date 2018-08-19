import configparser
import os

import pytest


@pytest.fixture
def db_url():
    db_path = "test.sqlite"

    if os.path.exists(db_path):
        os.unlink(db_path)

    return "sqlite://%s" % db_path


@pytest.fixture
def app_config(db_url):
    return configparser.ConfigParser(
        defaults={
            "database": {"uri": db_url}
        })


@pytest.fixture
def app(app_config):
    from lanauth.app import app_factory

    la_app = app_factory("test", app_config)
    return la_app


@pytest.fixture
def client(app):
    app.config["TESTING"] = True

    client = app.test_client()
    yield client
