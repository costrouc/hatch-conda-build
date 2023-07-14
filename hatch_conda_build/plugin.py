import typing
import json

from hatchling.builders.plugin.interface import BuilderInterface

from hatch_conda_build.config import CondaBuilderConfig


def generate_yaml():
    pass


class CondaBuilder(BuilderInterface):
    PLUGIN_NAME = 'conda'

    def get_version_api(self) -> typing.Dict:
        return {"standard": self.build_standard}

    def build_standard(self, directory: str, **_build_data) -> str:
        """Initialize the plugin."""
        breakpoint()
        return "directory"

    # @classmethod
    # def get_config_class(cls):
    #     return CondaBuilderConfig
