# Copyright

"""
.. module:: config
   :platform: Unix, Windows
   :synopsis: Config module to specify global constants

.. moduleauthor:: Sebastian Brunner


"""

import os
import logging
from pytest import raises
from yaml_configuration.config import DefaultConfig, ConfigError


def read_file(file_path, filename):
    file_path = os.path.join(file_path, filename)
    with open(file_path, 'r') as file_pointer:
        file_content = file_pointer.read()
    return file_content


class BasicConfig(DefaultConfig):

    def __init__(self, config_string, config_file, logger_object=None):
        super(BasicConfig, self).__init__(config_string, logger_object)
        # this is already done in the init
        # self.load(config_file, path=os.path.dirname(__file__))


def test_basic_config():
    config_file = "basic_config.yaml"
    config_string = read_file(os.path.dirname(__file__), config_file)
    basic_config = BasicConfig(config_string, config_file, logging.getLogger("TestLogger"))
    assert basic_config.get_config_value("BOOL_VALUE")
    assert basic_config.get_config_value("STRING_VALUE") == "test"
    assert basic_config.get_config_value("NUMBER_VALUE") == 42
    print "All test successful!"


if __name__ == '__main__':
    config_file = "basic_config.yaml"
    config_string = read_file(os.path.dirname(__file__), config_file)
    basic_config = BasicConfig(config_string, config_file, logging.getLogger("TestLogger"))
    basic_config.set_config_value("number_value", 10)
    basic_config.set_config_value("string_value", "test_string")
    assert basic_config.get_config_value("string_value") == "test_string"
    assert basic_config.get_config_value("not_existing_config_value", default=42) == 42
    with raises(ConfigError):
        if not basic_config.get_config_value("value_that_should_exist"):
            raise ConfigError("The config value with key 'value_that_should_exist' should exist")

    # test_basic_config()


