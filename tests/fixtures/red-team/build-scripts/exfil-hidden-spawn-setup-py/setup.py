# INERT FIXTURE — never executed. Modeled on the "esquelesquad" PyPI wave
# (2023, hundreds of packages: libencodepypost, selfvisarandompush,
# tpvirtualcontrolmc, …) as published in DataDog/malicious-software-packages-dataset.
#
# Shape: setup.py spawns a HIDDEN interpreter with a base64-ENCODED command at
# import time. There is no `curl`/`wget`, no `os.environ` read, and no
# recognizable URL in the source — the whole payload is inside the encoded blob,
# so every network/secret pattern in the pre-existing rule set stays silent.
#
# Redaction: the original blob decoded to a PowerShell downloader for an
# attacker-hosted .exe. Here it is base64 of the literal string "REDACTED" —
# the detectable structure survives, the payload does not.
from distutils.core import setup

try:
    import subprocess
    import os

    if not os.path.exists('tahg'):
        subprocess.Popen(
            'powershell -WindowStyle Hidden -EncodedCommand UkVEQUNURUQ=',
            shell=False,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
except Exception:
    pass

setup(
    name='libencodepypost',
    packages=['modlib'],
    version='8.42',
    description='encoding helpers',
    author='REDACTED',
)
