#!/usr/bin/env python3

import setuptools

setuptools.setup(
    entry_points={
        "console_scripts": [
            "cci = cci:main",
        ],

        "distutils.commands": [
            "release = distutils_twine:release",
        ],
    },
)

