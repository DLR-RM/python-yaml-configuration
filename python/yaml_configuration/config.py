# Copyright (C) 2016-2017 DLR
#
# All rights reserved. This program and the accompanying materials are made
# available under the terms of the 2-Clause BSD License ("Simplified BSD
# License") which accompanies this distribution, and is available at
# https://opensource.org/licenses/BSD-2-Clause
#
# Contributors:
# Benno Voggenreiter <benno.voggenreiter@dlr.de>
# Franz Steinmetz <franz.steinmetz@dlr.de>
# Sebastian Brunner <sebastian.brunner@dlr.de>

"""
.. module:: config
   :platform: Unix, Windows
   :synopsis: A python module to easily read from and write to yaml config files.

.. moduleauthor:: Sebastian Brunner


"""

import os
from os.path import expanduser, expandvars, isdir, isfile
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import argparse
import logging


def write_dict_to_yaml(dictionary, path, **kwargs):
    """
    Writes a dictionary to a yaml file
    :param dictionary:  the dictionary to be written
    :param path: the absolute path of the target yaml file
    :param kwargs: optional additional parameters for dumper
    """
    with open(path, 'w') as f:
        yaml.dump(dictionary, f, Dumper=Dumper, indent=4, **kwargs)


def load_dict_from_yaml(path):
    """
    Loads a dictionary from a yaml file
    :param path: the absolute path of the target yaml file
    :return:
    """
    f = open(path, 'r')
    dictionary = yaml.load(f, Loader=Loader)
    f.close()
    return dictionary


def config_path(path):
    if not path or path == 'None':
        return None
    # replace ~ with /home/user
    path = expanduser(path)
    path = expandvars(path)
    if not isfile(path) and not isdir(path):
        raise argparse.ArgumentTypeError("{0} is not a valid path".format(path))
    if os.access(path, os.R_OK):
        return path
    else:
        raise argparse.ArgumentTypeError("{0} is not a readable dir".format(path))


class DefaultConfig(object):
    """Class to hold and load the global configurations."""

    def __init__(self, default_config, logger_object=None, rel_config_path='yaml_configuration'):
        self.logger = logger_object
        self.rel_config_path = rel_config_path
        if logger_object is None:
            self.logger = logging.getLogger(__name__)
        assert isinstance(default_config, str)
        self.config_file_path = None
        self.default_config = default_config
        self.path = None

        if not default_config:
            self._config_dict = {}
        else:
            self._config_dict = yaml.load(self.default_config)

    def get_all_keys(self):
        """ Hand list of keys
        
        :return: All keys of the config dictionary
        :rtype: list
        """
        return list(self._config_dict.keys())

    def load(self, config_file, path=None):
        try:
            assert isinstance(config_file, str)
            if path is None:
                path = os.path.join(os.path.expanduser('~'), '.config', self.rel_config_path)

            if not os.path.exists(path):
                self.logger.warn('No configuration found at {0}, using temporary default config and create path on file'
                                 'system.'.format(path))
                os.makedirs(path)

            config_file_path = os.path.join(path, config_file)

            # If no config file is found, create one in the desired directory
            if not os.path.isfile(config_file_path):
                try:
                    if not os.path.exists(path):
                        os.makedirs(path)
                    write_dict_to_yaml(self._config_dict, config_file_path, width=80, default_flow_style=False)
                    self.config_file_path = config_file_path
                    self.logger.debug("Created config file {0}".format(config_file_path))
                except Exception as e:
                    self.logger.error('Could not write to config {0}, using temporary default configuration. '
                                      'Error: {1}'.format(config_file_path, e))
            # Otherwise read the config file from the specified directory
            else:
                try:
                    self._config_dict = load_dict_from_yaml(config_file_path)
                    self.config_file_path = config_file_path
                    self.logger.debug("Configuration loaded from {0}".format(os.path.abspath(config_file_path)))
                except Exception as e:
                    self.logger.error('Could not read from config {0}, using temporary default configuration. '
                                      'Error: {1}'.format(config_file_path, e))

                # Check if all attributes of the default config exists and introduce them if missing
                default_config_dict = yaml.load(self.default_config) if self.default_config else {}
                for k, v in default_config_dict.items():
                    if k not in self._config_dict:
                        self.logger.info("{0} use default-config-file parameter '{1}': {2}.".format(type(self).__name__, k, v))
                        self._config_dict[k] = v
        finally:
            if not isinstance(self._config_dict, dict):  # Ensure config_dict is always a dict
                self._config_dict = {}

        self.path = path

    def get_config_value(self, key, default=None):
        """Get a specific configuration value

        :param key: the key to the configuration value
        :param default: what to return if the key is not found
        :return: The value for the given key, if the key was found. Otherwise the default value
        """
        if key in self._config_dict:
            return self._config_dict[key]
        return default

    def set_config_value(self, key, value):
        """Get a specific configuration value

        :param key: the key to the configuration value
        :param value: The new value to be set for the given key
        """
        self._config_dict[key] = value

    def save_configuration(self):
        if self.config_file_path:
            write_dict_to_yaml(self._config_dict, self.config_file_path, width=80, default_flow_style=False)
            self.logger.debug("Saved configuration to {0}".format(self.config_file_path))
        else:
            self.logger.warning("The config_file_path needs to be set for {0}".format(self.__class__.__name__))


class ConfigError(Exception):
    """Exception raised for errors loading the config files"""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)
