import os.path

import paramiko
import pinject
from flask import Flask

from config.api_config import Config

service_classes = [

]


class BindingSpec(pinject.BindingSpec):
    """Binding setup"""

    def __init__(self, app: Flask):
        self.app = app

    def configure(self, bind):
        bind('app', to_instance=self.app)
        bind('config', to_instance=Config())
        bind('logger', to_instance=self.app.logger)
