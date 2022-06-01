import os
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AsyncioMinimalModbus",
    version=os.getenv("GITHUB_REF_NAME") if os.getenv("GITHUB_REF_NAME") and os.getenv(
        "GITHUB_REF_TYPE") == "tag" else "0.0.0",

    author="Guy Radford",
    description="Async Easy-to-use Modbus RTU and Modbus ASCII implementation for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/guyradford/asynciominimalmodbus",
    project_urls={
        "Bug Tracker": "https://github.com/guyradford/asynciominimalmodbus/issues",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Manufacturing",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Communications",
        "Topic :: Home Automation",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "Topic :: Terminals :: Serial",
        "Framework :: AsyncIO"
    ],
    py_modules=['asynciominimalmodbus'],
    python_requires=">=3.6",
    install_requires=['minimalmodbus>=2.0.1'],
    test_suite='tests',
)
