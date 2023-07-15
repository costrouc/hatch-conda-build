import sys
import subprocess

import pytest


def hatch_build_target(target: str):
    subprocess.run([
        "hatch", "build", "-t", target
    ], capture_output=False, check=True)


@pytest.mark.slow()
def test_build(new_project):
    directory = new_project(name='project-a', version='0.1.0', dependencies=["requests"])
    hatch_build_target("conda")
