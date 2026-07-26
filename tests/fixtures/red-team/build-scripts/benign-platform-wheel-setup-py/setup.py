# INERT FIXTURE — the false-positive trap for the identity-recon rule.
#
# A REAL and common benign shape: inspect the host platform, then download the
# matching prebuilt binary. Network call + host inspection are both present, so
# any rule of the form "network AND host-recon" fires here and blocks a large
# slice of legitimate scientific/native packaging.
#
# The distinction the rule must draw: platform/machine/sys.platform lookups
# select an ARTIFACT; login-name, host-name and cwd lookups identify a VICTIM.
#
# Written without naming those calls even in prose: the scanner reads raw text,
# so a comment that quotes the call syntax trips it exactly like real code would.
# That is a known limitation of a regex scanner, recorded in this corpus' notes.
import platform
import sys
import urllib.request

from setuptools import setup

ARCH = {"x86_64": "x64", "arm64": "arm64", "aarch64": "arm64"}[platform.machine()]
OS = "macos" if sys.platform == "darwin" else platform.system().lower()

urllib.request.urlretrieve(
    f"https://cdn.example/libfast/1.4.0/libfast-{OS}-{ARCH}.tar.gz",
    "vendor/libfast.tar.gz",
)

setup(
    name="fastlib",
    version="1.4.0",
    description="bindings for libfast, with prebuilt binaries",
    packages=["fastlib"],
)
