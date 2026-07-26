# Realistic benign setup.py for a C-extension package: compiler env vars,
# subprocess to the toolchain, no network, no secret reads.
import os
import subprocess
from setuptools import setup, Extension

cflags = os.environ.get("CFLAGS", "-O2").split()
subprocess.check_call(["pkg-config", "--exists", "zlib"])

setup(
    name="fastcodec",
    version="2.3.1",
    ext_modules=[Extension("fastcodec._native", sources=["src/native.c"], extra_compile_args=cflags)],
)
