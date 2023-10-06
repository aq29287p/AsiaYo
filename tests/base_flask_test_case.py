import os
from unittest import TestCase

from flask import Flask
from flask.ctx import AppContext
from flask_caching.backends.base import BaseCache


from api import create_app
from api.containers.services_container import ServicesContainer
from config.api_config import Config

TestCase.maxDiff = None


class BaseFlaskTestCase(TestCase):
    app: Flask
    app_context: AppContext
    container: ServicesContainer

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tests_path = os.path.realpath(os.path.dirname(__file__))
        self.fixtures_path = os.path.join(self.tests_path, "file_fixtures")

    @classmethod
    def setUpClass(cls) -> None:

        super().setUpClass()
        cls.app: Flask = create_app()
        cls.app.testing = True
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.app.logger.setLevel("ERROR")
        cls.container = cls.app.extensions["container"]




    @classmethod
    def tearDownClass(cls) -> None:

        setattr(cls, "app", None)
        setattr(cls, "app_context", None)
        setattr(cls, "container", None)

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()
