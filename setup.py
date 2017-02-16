from setuptools import setup, find_packages


setup(
    name='yaml_configuration',
    version='0.1.0',
    url='https://rmc-github.robotic.dlr.de/common/python_yaml_configuration',
    license='BSD',
    author='Sebastian Brunner',
    maintainer='Sebastian Brunner',
    author_email='sebastian.brunner@dlr.de',
    maintainer_email='sebastian.brunner@dlr.de',
    description='This python module can be used easily read and write to yaml config files.',
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

    python_requires='<=2.7',
    setup_requires=['pytest-runner'],
    install_requires=[],
    tests_require=['pytest'],

    zip_safe=True
)
