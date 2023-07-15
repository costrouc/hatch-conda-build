# hatch-conda-build

Conda package builder for [Hatch](https://hatch.pypa.io/latest/). Hatch is modern, extensible Python project manager.

## Usage

Add `hatch-conda-build` within the build-system.requires field in your pyproject.toml file.

```toml
[build-system]
requires = ["hatchling", "hatch-conda-build"]
build-backend = "hatchling.build"
```

Additionally `conda-build` must be in your current path when running a
hatch build.

### Configuration

Additional optional configuration settings may be set within the
`pyproject.toml`.

```toml
[tool.hatch.build.targets.conda]
channels = ["conda-forge"]
default_numpy_version = "1.22"
```

## Building Conda Package

The [builder plugin](https://hatch.pypa.io/latest/plugins/builder/reference/) name is called `conda`.

To start build process, run `hatch build -t conda`:

```shell
$ hatch build -t conda
[conda]
...
```

