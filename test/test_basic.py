"""
.. module:: config
   :platform: Unix, Windows
   :synopsis: Config module to specify global constants

.. moduleauthor:: Sebastian Brunner


"""

import os
from os import path
import logging
from yaml_configuration.config import DefaultConfig


def read_file(file_path, filename=None):
    file_path = os.path.realpath(file_path)
    if filename:
        file_path = os.path.join(file_path, filename)

    file_content = ""
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file_pointer:
            file_content = file_pointer.read()

    return file_content


CONFIG_FILE = "basic_config.yaml"
DEFAULT_CONFIG = read_file(path.dirname(__file__), CONFIG_FILE)


class BasicConfig(DefaultConfig):

    def __init__(self, logger_object=None):
        super(BasicConfig, self).__init__(DEFAULT_CONFIG, logger_object)
        self.load(CONFIG_FILE, path=path.dirname(__file__))


def test_basic_config():
    basic_config = BasicConfig(logging.getLogger("TestLogger"))
    assert basic_config.get_config_value("BOOL_VALUE")
    assert basic_config.get_config_value("STRING_VALUE") == "test"
    assert basic_config.get_config_value("NUMBER_VALUE") == 42
    print "All tests successful!"


if __name__ == '__main__':
    test_basic_config()


