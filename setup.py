#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import (setup, find_packages)

setup(
    name="aio-tinder",
    version="0.1.dev1",
    description="Tinder API library with asyncio",
    url="https://github.com/faruken/aio-tinder",
    author="faruken",
    author_email="",
    license="Whichever works for you",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython"
    ],
    keywords="tinder api asyncio",
    packages=find_packages(exclude=["tests", "examples"]),
    install_requires=[
        "aiohttp==0.22.5",
        "cchardet==1.0.0",
        "chardet==2.3.0",
        "multidict==1.2.2",
        "ujson==1.35"
    ],
    extras_require={
        "test": ["coverage==4.2", "Logbook==1.0.0", "pytest==3.0.0",
                 "pytest-asyncio==0.4.1", "pytest-cov==2.3.1"]
    }
)
