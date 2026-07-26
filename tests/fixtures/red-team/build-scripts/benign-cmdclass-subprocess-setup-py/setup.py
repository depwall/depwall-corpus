# INERT FIXTURE — the false-positive trap for the hidden-spawn rule.
#
# A REAL and common benign shape: a cmdclass override that spawns a build
# toolchain. Everything the malicious wave uses is here EXCEPT the concealment —
# no hidden window, no encoded command, no detached-console flag. A rule that
# fires on `subprocess` at all would block every C/C++/Rust-backed sdist.
import subprocess

from setuptools import setup
from setuptools.command.build_ext import build_ext


class CMakeBuild(build_ext):
    def run(self):
        subprocess.check_call(["cmake", "-S", ".", "-B", "build"])
        subprocess.check_call(["cmake", "--build", "build", "--config", "Release"])
        build_ext.run(self)


setup(
    name="native-thing",
    version="2.1.0",
    description="python bindings backed by a cmake project",
    packages=["native_thing"],
    cmdclass={"build_ext": CMakeBuild},
)
