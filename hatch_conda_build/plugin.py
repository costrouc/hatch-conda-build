import json
import shutil
import typing
import pathlib
import collections
import tempfile
import subprocess

from hatchling.builders.plugin.interface import BuilderInterface

from hatch_conda_build.config import CondaBuilderConfig
from grayskull.strategy.py_toml import get_all_toml_info


class CondaBuilder(BuilderInterface):
    PLUGIN_NAME = "conda"

    def get_version_api(self) -> typing.Dict:
        return {"standard": self.build_standard}

    def clean(directory: str, versions: typing.List[str]):
        shutil.rmtree(directory)

    def build_standard(self, directory: str, **build_data: typing.Dict) -> str:
        directory = pathlib.Path(directory)

        py_meta = self.metadata.core_raw_metadata
        conda_meta = collections.defaultdict(dict)

        # package
        conda_meta['package']['name'] = self.metadata.name
        conda_meta['package']['version'] = self.metadata.version

        # source
        conda_meta['source']['path'] = str(pathlib.Path(self.metadata._project_file).parent)

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

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = pathlib.Path(tmpdir)
            conda_meta_filename = tmpdir / "meta.yaml"
            with conda_meta_filename.open("w") as f:
                json.dump(conda_meta, f)

            subprocess.run(
                ['conda-build', 'build', str(tmpdir), '--output-folder', str(tmpdir)],
                check=True)

            conda_build_filename = tmpdir / 'noarch' / f"{conda_meta['package']['name']}-{conda_meta['package']['version']}-{conda_meta['build']['number']}.tar.bz2"
            shutil.copy2(conda_build_filename, directory / conda_build_filename.name)

        return str(directory)

    @classmethod
    def get_config_class(cls):
        return CondaBuilderConfig
