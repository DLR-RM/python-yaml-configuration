# Copyright (C) 2017 DLR
#
# All rights reserved. This program and the accompanying materials are made
# available under the terms of the Eclipse Public License v1.0 which
# accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
#
# Contributors:
# Franz Steinmetz <franz.steinmetz@dlr.de>
# Sebastian Brunner <sebastian.brunner@dlr.de>

from setuptools import setup, find_packages


setup(
    name='yaml_configuration',
    version='0.0.6',
    url='https://rmc-github.robotic.dlr.de/common/python_yaml_configuration',
    license='BSD',
    author='Sebastian Brunner',
    maintainer='Sebastian Brunner',
    author_email='sebastian.brunner@dlr.de',
    maintainer_email='sebastian.brunner@dlr.de',
    description='A python module to easily read from and write to yaml config files.',
    keywords=('yaml', 'configuration'),

    packages=find_packages('python'),  # include all packages under python
    package_dir={'': 'python'},   # tell distutils packages are under python

    # works but not sufficient => see MANIFEST.in for extra files to include
    # package_data={'': ['*basic_config.yaml']},
    # package_data={'yaml_configuration': ['*basic_config.yaml']},

    # does not work
    # package_data={'': ['yaml_configuration/basic_config.yaml']},
    # package_data={'python': ['*basic_config.yaml']},
    # include_package_data=True,
    # data_files=[('yaml_configuration', ['/etc/locale.conf'])],

    python_requires='>=2.6, !=3.*',
    setup_requires=['pytest-runner'],
    install_requires=[],
    tests_require=['pytest'],

    zip_safe=True
)
