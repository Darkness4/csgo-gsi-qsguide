# -*- coding: utf-8 -*-
from setuptools import setup
import sys

scripts = ["csgogsilcd"]
if sys.platform == "win32":
    scripts.append("csgogsilcd.bat")
setup(name='csgo_gsi_arduino_lcd',
      version='1.3.0',
      description="CSGO's informations displayed on an Arduino featuring a bomb timer.",
      url='https://github.com/Darkness4/csgo-gsi-arduino-lcd',
      packages=['csgo_gsi_arduino_lcd'],
      scripts=scripts,
      zip_safe=False)
