import sys
import subprocess

import pytest


def run(*args, check=True):
    process = subprocess.run(
        [sys.executable, "-m", *args],  # noqa: S603
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
    )
    if check and process.returncode:
        pytest.fail(process.stdout)

    return process.stdout


def hatch_build_target(target, *args, check=True):
    return run("hatch", "build", "-t", target, *args, check=check)


@pytest.mark.slow()
def test_build(new_project):
    directory = new_project(name='project-a', version='0.1.0', dependencies=["requests"])
    hatch_build_target("conda")
