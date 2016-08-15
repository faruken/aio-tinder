#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import (setup, find_packages)

setup(
    name="aio-tinder",
    version="0.1.dev0",
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
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "aiohttp==0.22.5",
        "cchardet==1.0.0",
        "chardet==2.3.0",
        "multidict==1.2.2",
        "ujson==1.35"
    ],
    extras_require={
        "test": ["coverage==4.2", "Logbook==1.0.0", "nose==1.3.7"]
    }
)
