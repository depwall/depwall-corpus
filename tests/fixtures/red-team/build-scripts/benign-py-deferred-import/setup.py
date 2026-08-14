# INERT FIXTURE — never executed.
#
# FALSE-POSITIVE TRAP for import following, and the reason that feature judges
# the imported module rather than the fact of the import. Structurally identical
# to `exfil-py-deferred-import/`: a `cmdclass` install override that imports a
# project module inside `run()` and calls it.
#
# Deferring a post-install step to a module is ordinary packaging — compiling
# extensions, building caches, writing a config template. Following the import
# must therefore judge the helper on what the helper DOES; this one must produce
# zero findings.
from setuptools import setup, find_packages
from setuptools.command.install import install


class BuildAssets(install):
    def run(self):
        install.run(self)
        from _postinstall import build_cache

        build_cache()


setup(
    name="inert-fixture-benign-deferred",
    version="1.4.2",
    author="REDACTED",
    description="none",
    long_description="none",
    long_description_content_type="text/markdown",
    cmdclass={"install": BuildAssets},
    install_requires=["numpy"],
    packages=find_packages(),
)
