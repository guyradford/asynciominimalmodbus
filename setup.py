import os
from setuptools import find_packages, setup

setup(
    name='AsyncioMinimalModbus',
    packages=find_packages(),
    version=os.getenv('CI_COMMIT_TAG'),
    description='AsyncioMinimalModbus',
    author='Guy Radford',
    author_email='guy.@gmail.com',
    license='Apache License, Version 2.0',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.2.5'],
    test_suite='tests',
    python_requires='>=3.7',
)
