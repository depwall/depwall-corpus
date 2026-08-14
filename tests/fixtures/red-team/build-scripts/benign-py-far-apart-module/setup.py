# INERT FIXTURE — never executed.
#
# The setup.py half of the `nodeenv` shape: it imports the project's own module
# at top level purely to read `__version__`. This is one of the most common
# patterns on PyPI (`dill`, `six`, `lxml`, `grpcio-status` all do a version of
# it), and it means import-following routinely hands the scanner a full
# application module rather than a short build script.
from setuptools import setup

import nodeenv_like

setup(
    name="inert-fixture-far-apart",
    version=nodeenv_like.__version__,
    description="none",
    long_description="none",
    py_modules=["nodeenv_like"],
)
