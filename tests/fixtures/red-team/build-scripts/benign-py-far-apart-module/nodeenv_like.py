# INERT FIXTURE — never executed. Host is REDACTED.example.
#
# REDUCED FROM nodeenv (top-300 on PyPI, a pre-commit dependency), which the
# first version of import-following BLOCKED. It fetches a Node tarball because
# that is its entire purpose, and it copies the parent environment far away in
# the file to build a child process environment. Two unrelated statements that
# whole-file co-occurrence welded into an "exfiltration" gate.
#
# The DISTANCE between the two markers is load-bearing: shrink it below
# PY_GATE_WINDOW and this fixture stops testing what it exists to test. The
# prose here deliberately does not name either call — a text scanner matches
# comments too, which is the same reason benign-platform-wheel-setup-py/ avoids
# naming what it does.
import os
import subprocess
import sys
from urllib.request import urlopen

__version__ = "1.9.1"


def download_node(version, dest):
    # Fetches a published runtime tarball by version — an ARTIFACT selected by
    # version, not a victim identified by anything.
    url = "https://REDACTED.example/dist/v%s/node-v%s.tar.gz" % (version, version)
    with urlopen(url, timeout=30) as resp:
        with open(dest, "wb") as out:
            out.write(resp.read())
    return dest


def _bookkeeping():
    # install bookkeeping line 0 — real installers carry hundreds of these
    # install bookkeeping line 1 — real installers carry hundreds of these
    # install bookkeeping line 2 — real installers carry hundreds of these
    # install bookkeeping line 3 — real installers carry hundreds of these
    # install bookkeeping line 4 — real installers carry hundreds of these
    # install bookkeeping line 5 — real installers carry hundreds of these
    # install bookkeeping line 6 — real installers carry hundreds of these
    # install bookkeeping line 7 — real installers carry hundreds of these
    # install bookkeeping line 8 — real installers carry hundreds of these
    # install bookkeeping line 9 — real installers carry hundreds of these
    # install bookkeeping line 10 — real installers carry hundreds of these
    # install bookkeeping line 11 — real installers carry hundreds of these
    # install bookkeeping line 12 — real installers carry hundreds of these
    # install bookkeeping line 13 — real installers carry hundreds of these
    # install bookkeeping line 14 — real installers carry hundreds of these
    # install bookkeeping line 15 — real installers carry hundreds of these
    # install bookkeeping line 16 — real installers carry hundreds of these
    # install bookkeeping line 17 — real installers carry hundreds of these
    # install bookkeeping line 18 — real installers carry hundreds of these
    # install bookkeeping line 19 — real installers carry hundreds of these
    # install bookkeeping line 20 — real installers carry hundreds of these
    # install bookkeeping line 21 — real installers carry hundreds of these
    # install bookkeeping line 22 — real installers carry hundreds of these
    # install bookkeeping line 23 — real installers carry hundreds of these
    # install bookkeeping line 24 — real installers carry hundreds of these
    # install bookkeeping line 25 — real installers carry hundreds of these
    # install bookkeeping line 26 — real installers carry hundreds of these
    # install bookkeeping line 27 — real installers carry hundreds of these
    # install bookkeeping line 28 — real installers carry hundreds of these
    # install bookkeeping line 29 — real installers carry hundreds of these
    # install bookkeeping line 30 — real installers carry hundreds of these
    # install bookkeeping line 31 — real installers carry hundreds of these
    # install bookkeeping line 32 — real installers carry hundreds of these
    # install bookkeeping line 33 — real installers carry hundreds of these
    # install bookkeeping line 34 — real installers carry hundreds of these
    # install bookkeeping line 35 — real installers carry hundreds of these
    # install bookkeeping line 36 — real installers carry hundreds of these
    # install bookkeeping line 37 — real installers carry hundreds of these
    # install bookkeeping line 38 — real installers carry hundreds of these
    # install bookkeeping line 39 — real installers carry hundreds of these
    # install bookkeeping line 40 — real installers carry hundreds of these
    # install bookkeeping line 41 — real installers carry hundreds of these
    # install bookkeeping line 42 — real installers carry hundreds of these
    # install bookkeeping line 43 — real installers carry hundreds of these
    # install bookkeeping line 44 — real installers carry hundreds of these
    # install bookkeeping line 45 — real installers carry hundreds of these
    # install bookkeeping line 46 — real installers carry hundreds of these
    # install bookkeeping line 47 — real installers carry hundreds of these
    # install bookkeeping line 48 — real installers carry hundreds of these
    # install bookkeeping line 49 — real installers carry hundreds of these
    # install bookkeeping line 50 — real installers carry hundreds of these
    # install bookkeeping line 51 — real installers carry hundreds of these
    # install bookkeeping line 52 — real installers carry hundreds of these
    # install bookkeeping line 53 — real installers carry hundreds of these
    # install bookkeeping line 54 — real installers carry hundreds of these
    # install bookkeeping line 55 — real installers carry hundreds of these
    # install bookkeeping line 56 — real installers carry hundreds of these
    # install bookkeeping line 57 — real installers carry hundreds of these
    # install bookkeeping line 58 — real installers carry hundreds of these
    # install bookkeeping line 59 — real installers carry hundreds of these
    # install bookkeeping line 60 — real installers carry hundreds of these
    # install bookkeeping line 61 — real installers carry hundreds of these
    # install bookkeeping line 62 — real installers carry hundreds of these
    # install bookkeeping line 63 — real installers carry hundreds of these
    # install bookkeeping line 64 — real installers carry hundreds of these
    # install bookkeeping line 65 — real installers carry hundreds of these
    # install bookkeeping line 66 — real installers carry hundreds of these
    # install bookkeeping line 67 — real installers carry hundreds of these
    # install bookkeeping line 68 — real installers carry hundreds of these
    # install bookkeeping line 69 — real installers carry hundreds of these
    # install bookkeeping line 70 — real installers carry hundreds of these
    # install bookkeeping line 71 — real installers carry hundreds of these
    # install bookkeeping line 72 — real installers carry hundreds of these
    # install bookkeeping line 73 — real installers carry hundreds of these
    # install bookkeeping line 74 — real installers carry hundreds of these
    # install bookkeeping line 75 — real installers carry hundreds of these
    # install bookkeeping line 76 — real installers carry hundreds of these
    # install bookkeeping line 77 — real installers carry hundreds of these
    # install bookkeeping line 78 — real installers carry hundreds of these
    # install bookkeeping line 79 — real installers carry hundreds of these
    # install bookkeeping line 80 — real installers carry hundreds of these
    # install bookkeeping line 81 — real installers carry hundreds of these
    # install bookkeeping line 82 — real installers carry hundreds of these
    # install bookkeeping line 83 — real installers carry hundreds of these
    # install bookkeeping line 84 — real installers carry hundreds of these
    # install bookkeeping line 85 — real installers carry hundreds of these
    # install bookkeeping line 86 — real installers carry hundreds of these
    # install bookkeeping line 87 — real installers carry hundreds of these
    # install bookkeeping line 88 — real installers carry hundreds of these
    # install bookkeeping line 89 — real installers carry hundreds of these
    # install bookkeeping line 90 — real installers carry hundreds of these
    # install bookkeeping line 91 — real installers carry hundreds of these
    # install bookkeeping line 92 — real installers carry hundreds of these
    # install bookkeeping line 93 — real installers carry hundreds of these
    # install bookkeeping line 94 — real installers carry hundreds of these
    # install bookkeeping line 95 — real installers carry hundreds of these
    # install bookkeeping line 96 — real installers carry hundreds of these
    # install bookkeeping line 97 — real installers carry hundreds of these
    # install bookkeeping line 98 — real installers carry hundreds of these
    # install bookkeeping line 99 — real installers carry hundreds of these
    # install bookkeeping line 100 — real installers carry hundreds of these
    # install bookkeeping line 101 — real installers carry hundreds of these
    # install bookkeeping line 102 — real installers carry hundreds of these
    # install bookkeeping line 103 — real installers carry hundreds of these
    # install bookkeeping line 104 — real installers carry hundreds of these
    # install bookkeeping line 105 — real installers carry hundreds of these
    # install bookkeeping line 106 — real installers carry hundreds of these
    # install bookkeeping line 107 — real installers carry hundreds of these
    # install bookkeeping line 108 — real installers carry hundreds of these
    # install bookkeeping line 109 — real installers carry hundreds of these
    # install bookkeeping line 110 — real installers carry hundreds of these
    # install bookkeeping line 111 — real installers carry hundreds of these
    # install bookkeeping line 112 — real installers carry hundreds of these
    # install bookkeeping line 113 — real installers carry hundreds of these
    # install bookkeeping line 114 — real installers carry hundreds of these
    # install bookkeeping line 115 — real installers carry hundreds of these
    # install bookkeeping line 116 — real installers carry hundreds of these
    # install bookkeeping line 117 — real installers carry hundreds of these
    # install bookkeeping line 118 — real installers carry hundreds of these
    # install bookkeeping line 119 — real installers carry hundreds of these
    # install bookkeeping line 120 — real installers carry hundreds of these
    # install bookkeeping line 121 — real installers carry hundreds of these
    # install bookkeeping line 122 — real installers carry hundreds of these
    # install bookkeeping line 123 — real installers carry hundreds of these
    # install bookkeeping line 124 — real installers carry hundreds of these
    # install bookkeeping line 125 — real installers carry hundreds of these
    # install bookkeeping line 126 — real installers carry hundreds of these
    # install bookkeeping line 127 — real installers carry hundreds of these
    # install bookkeeping line 128 — real installers carry hundreds of these
    # install bookkeeping line 129 — real installers carry hundreds of these
    # install bookkeeping line 130 — real installers carry hundreds of these
    # install bookkeeping line 131 — real installers carry hundreds of these
    # install bookkeeping line 132 — real installers carry hundreds of these
    # install bookkeeping line 133 — real installers carry hundreds of these
    # install bookkeeping line 134 — real installers carry hundreds of these
    # install bookkeeping line 135 — real installers carry hundreds of these
    # install bookkeeping line 136 — real installers carry hundreds of these
    # install bookkeeping line 137 — real installers carry hundreds of these
    # install bookkeeping line 138 — real installers carry hundreds of these
    # install bookkeeping line 139 — real installers carry hundreds of these
    # install bookkeeping line 140 — real installers carry hundreds of these
    # install bookkeeping line 141 — real installers carry hundreds of these
    # install bookkeeping line 142 — real installers carry hundreds of these
    # install bookkeeping line 143 — real installers carry hundreds of these
    # install bookkeeping line 144 — real installers carry hundreds of these
    # install bookkeeping line 145 — real installers carry hundreds of these
    # install bookkeeping line 146 — real installers carry hundreds of these
    # install bookkeeping line 147 — real installers carry hundreds of these
    # install bookkeeping line 148 — real installers carry hundreds of these
    # install bookkeeping line 149 — real installers carry hundreds of these
    # install bookkeeping line 150 — real installers carry hundreds of these
    # install bookkeeping line 151 — real installers carry hundreds of these
    # install bookkeeping line 152 — real installers carry hundreds of these
    # install bookkeeping line 153 — real installers carry hundreds of these
    # install bookkeeping line 154 — real installers carry hundreds of these
    # install bookkeeping line 155 — real installers carry hundreds of these
    # install bookkeeping line 156 — real installers carry hundreds of these
    # install bookkeeping line 157 — real installers carry hundreds of these
    # install bookkeeping line 158 — real installers carry hundreds of these
    # install bookkeeping line 159 — real installers carry hundreds of these
    # install bookkeeping line 160 — real installers carry hundreds of these
    # install bookkeeping line 161 — real installers carry hundreds of these
    # install bookkeeping line 162 — real installers carry hundreds of these
    # install bookkeeping line 163 — real installers carry hundreds of these
    # install bookkeeping line 164 — real installers carry hundreds of these
    # install bookkeeping line 165 — real installers carry hundreds of these
    # install bookkeeping line 166 — real installers carry hundreds of these
    # install bookkeeping line 167 — real installers carry hundreds of these
    # install bookkeeping line 168 — real installers carry hundreds of these
    # install bookkeeping line 169 — real installers carry hundreds of these
    # install bookkeeping line 170 — real installers carry hundreds of these
    # install bookkeeping line 171 — real installers carry hundreds of these
    # install bookkeeping line 172 — real installers carry hundreds of these
    # install bookkeeping line 173 — real installers carry hundreds of these
    # install bookkeeping line 174 — real installers carry hundreds of these
    # install bookkeeping line 175 — real installers carry hundreds of these
    # install bookkeeping line 176 — real installers carry hundreds of these
    # install bookkeeping line 177 — real installers carry hundreds of these
    # install bookkeeping line 178 — real installers carry hundreds of these
    # install bookkeeping line 179 — real installers carry hundreds of these
    # install bookkeeping line 180 — real installers carry hundreds of these
    # install bookkeeping line 181 — real installers carry hundreds of these
    # install bookkeeping line 182 — real installers carry hundreds of these
    # install bookkeeping line 183 — real installers carry hundreds of these
    # install bookkeeping line 184 — real installers carry hundreds of these
    # install bookkeeping line 185 — real installers carry hundreds of these
    # install bookkeeping line 186 — real installers carry hundreds of these
    # install bookkeeping line 187 — real installers carry hundreds of these
    # install bookkeeping line 188 — real installers carry hundreds of these
    # install bookkeeping line 189 — real installers carry hundreds of these
    # install bookkeeping line 190 — real installers carry hundreds of these
    # install bookkeeping line 191 — real installers carry hundreds of these
    # install bookkeeping line 192 — real installers carry hundreds of these
    # install bookkeeping line 193 — real installers carry hundreds of these
    # install bookkeeping line 194 — real installers carry hundreds of these
    # install bookkeeping line 195 — real installers carry hundreds of these
    # install bookkeeping line 196 — real installers carry hundreds of these
    # install bookkeeping line 197 — real installers carry hundreds of these
    # install bookkeeping line 198 — real installers carry hundreds of these
    # install bookkeeping line 199 — real installers carry hundreds of these
    return None


def run_in_env(args, extra_env=None):
    # A child process needs the parent environment plus the venv PATH. Nothing
    # is serialized, sent, or read by a secret name.
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    return subprocess.run(args, env=env, check=False, stdout=sys.stdout)
