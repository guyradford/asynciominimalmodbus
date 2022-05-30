import os
from setuptools import find_packages, setup

setup(
    name='AsyncioMinimalModbus',
    packages=find_packages(),
    version=os.getenv('CI_COMMIT_TAG'),
    description='AsyncioMinimalModbus',
    author='Guy Radford',
    author_email='guy.radford@gmail.com',
    license='Apache License, Version 2.0',
    install_requires=['minimalmodbus==2.0.1'],
    setup_requires=['pytest-runner'],
    # tests_require=['pytest==6.2.5', 'pylint==2.13.9'],
    test_suite='tests',
    python_requires='>=3.6',
)
