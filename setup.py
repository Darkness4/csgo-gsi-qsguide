# -*- coding: utf-8 -*-
from setuptools import setup
import sys

scripts = ["csgogsilcd"]
if sys.platform == "win32":
    scripts.append("csgogsilcd.bat")
setup(
    name="csgo_gsi_arduino_lcd",
    version="1.4.0",
    description="CSGO's informations displayed on an Arduino featuring a bomb timer.",
    author="Marc NGUYEN",
    author_email="nguyen_marc@live.fr",
    license="MIT",
    url="https://github.com/Darkness4/csgo-gsi-arduino-lcd",
    packages=["csgo_gsi_arduino_lcd"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    scripts=scripts,
    package_data={"assets": ["*"]},
    install_requires=[
        "PySide2",
        "pyserial",
        "QtPy",
    ],
    zip_safe=False,
)
