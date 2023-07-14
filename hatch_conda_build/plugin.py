import shutil
import typing
import pathlib

from hatchling.builders.plugin.interface import BuilderInterface

from hatch_conda_build.config import CondaBuilderConfig


def generate_yaml():
    pass


class CondaBuilder(BuilderInterface):
    PLUGIN_NAME = "conda"

    def get_version_api(self) -> typing.Dict:
        return {"standard": self.build_standard}

    def clean(directory: str, versions: typing.List[str]):
        shutil.rmtree(directory)

    def build_standard(self, directory: str, **build_data: typing.Dict) -> str:
        directory = pathlib.Path(directory)
        print("args", directory, build_data)
        print("build_config", self.build_config)
        print("target_config", self.target_config)
        print("builder_config", self.config)

        (directory / "asdf").mkdir()
        (directory / "test.txt").write_text("asdf")

        return str(directory)

    @classmethod
    def get_config_class(cls):
        return CondaBuilderConfig
