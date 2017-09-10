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
          data_files=[
           ('resources', ['resources/csgo-16.ico', 'resources/csgo-20.ico', 'resources/csgo-24.ico', 'resources/csgo-32.ico', 'resources/csgo-48.ico', 'resources/csgo-64.ico', 'resources/csgo-128.ico', 'resources/csgo-256.ico', 'resources/csgo-512.ico'])],
      zip_safe=False)
