# INERT FIXTURE — never executed. Modeled on DeepSolid@99.6 and HLLM@912.6
# (DataDog/malicious-software-packages-dataset, pypi/malicious_intent).
#
# KNOWN GAP, deliberately asserted clean. The setup.py itself does nothing
# hostile: it defers to an install-command override that imports a module from
# the package and calls it. No network call, no environment read, no
# concealment, no shell — every deterministic pattern stays silent, and it
# should, because `cmdclass` + a project import is also how legitimate packages
# run post-install steps.
#
# What makes it malicious lives in `main.py`, one file over — the same
# body-not-read gap the npm `preinstall: node index.js` shape has. Closing it
# means scanning the module the install hook reaches, not adding a pattern here.
from setuptools import setup, find_packages
from setuptools.command.install import install


class CrazyInstallStrat(install):
    def run(self):
        install.run(self)
        from main import m

        m()


setup(
    name="DeepSolid",
    version="99.6",
    author="REDACTED",
    description="none",
    long_description="none",
    long_description_content_type="text/markdown",
    cmdclass={"install": CrazyInstallStrat},
    install_requires=["requests", "psutil"],
    setup_requires=["setuptools"],
    packages=find_packages(),
)
