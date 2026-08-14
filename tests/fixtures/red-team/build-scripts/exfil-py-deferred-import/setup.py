# INERT FIXTURE — never executed. Modeled on DeepSolid@99.6 and HLLM@912.6
# (DataDog/malicious-software-packages-dataset, pypi/malicious_intent).
#
# The DECOY, and it stays asserted clean ON ITS OWN. This setup.py does nothing
# hostile: it defers to an install-command override that imports a module from
# the package and calls it. No network call, no environment read, no
# concealment, no shell — every deterministic pattern stays silent, and it
# should, because `cmdclass` + a project import is also how legitimate packages
# run post-install steps.
#
# What makes it malicious lives in `main.py`, one file over. This was the pinned
# known gap (`gap-deferred-cmdclass-setup-py/`) until the sdist walker learned to
# resolve the modules a setup.py imports and read them out of the same archive —
# the Python twin of the npm require hop. Its false-positive twin is
# `benign-py-deferred-import/`, identical in shape, which must stay clean.
#
# The import sits INSIDE `run()`, deferred until install time, which is exactly
# why a scanner that reads only setup.py sees nothing worth reporting.
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
