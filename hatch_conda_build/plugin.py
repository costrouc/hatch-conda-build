import json
import shutil
import typing
import pathlib
import collections
import tempfile
import subprocess

from ruamel.yaml import YAML
from hatchling.builders.plugin.interface import BuilderInterface

from hatch_conda_build.config import CondaBuilderConfig


def construct_meta_yaml_from_pyproject(metadata):
    py_meta = metadata.core_raw_metadata
    conda_meta = collections.defaultdict(dict)

    # package
    conda_meta['package']['name'] = metadata.name
    conda_meta['package']['version'] = metadata.version

    # source
    conda_meta['source']['path'] = str(pathlib.Path(metadata._project_file).parent)

    # build
    conda_meta['build']['number'] = 0
    conda_meta['build']['noarch'] = 'python'
    conda_meta['build']['script'] = 'python -m pip install --no-deps --ignore-installed .'

    # requirements
    conda_meta['requirements']['build'] = []
    conda_meta['requirements']['host'] = [
        'pip',
        'hatchling',
    ]
    conda_meta['requirements']['run'] = py_meta['dependencies']

    # test
    conda_meta['test'] = {}

    # about
    conda_meta['about'] = {

    }

    return conda_meta


def conda_build(
    meta_config: typing.Dict,
    build_directory: pathlib.Path,
    output_directory: pathlib.Path,
    channels: typing.List[str],
    default_numpy_version: str,
):
    conda_meta_filename = build_directory / "meta.yaml"
    with conda_meta_filename.open("w") as f:
        json.dump(meta_config, f)

    command = ['conda-build', 'build', str(build_directory), '--output-folder', str(output_directory), '--override-channels', '--numpy', default_numpy_version, '--debug']
    for channel in channels:
        command += ['--channel', channel]
    print(command)

    import sys
    subprocess.run(command, check=True, stderr=sys.stderr, stdout=sys.stdout)

    package_name = f"{meta_config['package']['name']}-{meta_config['package']['version']}-{meta_config['build']['number']}.tar.bz2"
    return output_directory / 'noarch' / package_name


class CondaBuilder(BuilderInterface):
    PLUGIN_NAME = "conda"

    def get_version_api(self) -> typing.Dict:
        return {"standard": self.build_standard}

    def clean(directory: str, versions: typing.List[str]):
        shutil.rmtree(directory)

    def build_standard(self, directory: str, **build_data: typing.Dict) -> str:
        directory = pathlib.Path(directory)

        conda_meta = construct_meta_yaml_from_pyproject(self.metadata)
        target_config = self.build_config['targets']['conda']

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = pathlib.Path(tmpdir)

            conda_build_filename = conda_build(
                conda_meta,
                build_directory=tmpdir,
                output_directory=tmpdir,
                channels=target_config.get('channels', ['conda-forge']),
                default_numpy_version=target_config.get('default_numpy_version', '1.22'),
            )
            shutil.copy2(conda_build_filename, directory / conda_build_filename.name)

        return str(directory)

    @classmethod
    def get_config_class(cls):
        return CondaBuilderConfig
