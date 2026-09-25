"""Configuration model helpers for the Icarus DCC launcher.

This module defines the early launcher configuration pieces used to turn
local machine settings into paths that later launcher code can use. The current
scope is deliberately small: read settings, derive Rez paths, and represent the
final launcher configuration as immutable records.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


def default_repo_root() -> Path:
    """Return the repository root based on this module's location.

    Returns
    -------
    Path
        Repository root containing the project `pyproject.toml`.
    """
    return Path(__file__).resolve().parents[3]


def default_dcc_dev_root(repo_root: Path) -> Path:
    """Return the DCC development root that contains the repository.

    Parameters
    ----------
    repo_root
        Root path of the `icarus-dcc` repository.

    Returns
    -------
    Path
        Parent folder expected to contain shared local DCC infrastructure.
    """
    return repo_root.parent


def default_settings_path(dcc_dev_root: Path) -> Path:
    """Return the default local launcher settings file path.

    Parameters
    ----------
    dcc_dev_root
        Root folder that contains local DCC infrastructure such as `_rez`.

    Returns
    -------
    Path
        Expected path to the local `launcher_settings.json` file.
    """
    return dcc_dev_root / '_rez' / 'config' / 'launcher_settings.json'


def load_settings(settings_path: Path) -> dict:
    """Load raw launcher settings from a JSON file.

    Parameters
    ----------
    settings_path
        Path to the local launcher settings JSON file.

    Returns
    -------
    dict
        Raw settings dictionary loaded from JSON.
    """
    with settings_path.open('r', encoding='utf-8') as settings_file:
        return json.load(settings_file)


def rez_executable(dcc_dev_root: Path) -> Path:
    """Return the expected Rez executable path for a DCC dev root.

    Parameters
    ----------
    dcc_dev_root
        Root folder that contains local DCC infrastructure such as `_rez`.

    Returns
    -------
    Path
        Expected path to the Rez executable.
    """
    return dcc_dev_root / '_rez' / 'install' / 'Scripts' / 'rez' / 'rez.exe'


def rez_config_file(dcc_dev_root: Path) -> Path:
    """Return the expected Rez configuration file path for a DCC dev root.

    Parameters
    ----------
    dcc_dev_root
        Root folder that contains local DCC infrastructure such as `_rez`.

    Returns
    -------
    Path
        Expected path to the local Rez configuration file.
    """
    return dcc_dev_root / '_rez' / 'config' / 'rezconfig.py'


@dataclass(frozen=True)
class LauncherConfig:
    """Final launcher configuration consumed by process and UI code.

    This is the product of the config-building flow. It contains resolved paths
    and launch metadata, not raw JSON data.

    Attributes
    ----------
    dcc_name
        Name of the target DCC application.
    version
        Major DCC version represented by this configuration.
    dcc_dev_root
        Root folder that contains local DCC infrastructure.
    install_location
        Local install root for the target DCC version.
    rez_package
        Rez package request used to create the runtime environment.
    rez_executable
        Path to the Rez executable used by the launcher.
    rez_config_file
        Path to the local Rez configuration file.
    launch_command
        Command Rez should run after resolving the package request.
    env_var_name
        Environment variable used to pass the DCC install location to Rez.
    """

    dcc_name: str
    version: int
    dcc_dev_root: Path
    install_location: Path
    rez_package: str
    rez_executable: Path
    rez_config_file: Path
    launch_command: str
    env_var_name: str


@dataclass(frozen=True)
class LauncherSettingsRecord:
    """Typed record created from local launcher settings JSON.

    The JSON file stores machine-local choices as strings. This record converts
    them into Python-friendly values for the builder layer.

    Attributes
    ----------
    dcc_dev_root
        Root folder that contains local DCC infrastructure.
    maya_locations
        Mapping from Maya major version to local Maya install root.
    """

    dcc_dev_root: Path
    maya_locations: dict[int, Path]

    @classmethod
    def from_settings(cls, *, settings: dict) -> 'LauncherSettingsRecord':
        """Create a settings record from raw JSON settings data.

        Parameters
        ----------
        settings
            Raw settings dictionary loaded from `launcher_settings.json`.

        Returns
        -------
        LauncherSettingsRecord
            Typed settings record with paths normalized to `Path` objects.
        """
        maya_locations = {
            int(version): Path(values['location'])
            for version, values in settings['maya'].items()
        }

        return cls(
            dcc_dev_root=Path(settings['dcc_dev_root']),
            maya_locations=maya_locations,
        )