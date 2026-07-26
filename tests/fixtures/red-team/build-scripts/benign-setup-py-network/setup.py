# Realistic benign setup.py that downloads test data during build and reads
# ordinary toolchain env vars — must NOT trip the deterministic signal.
import os
import requests
from setuptools import setup

cflags = os.environ.get("CFLAGS", "-O2")
requests.get("https://data.example/testdata.bin", timeout=30)

setup(name="datapkg", version="1.4.0")
