
from pathlib import Path

from icarus_dcc.launcher.config import (
    default_dcc_dev_root,
    default_settings_path,
    load_settings,
    rez_config_file,
    rez_executable,
    LauncherConfig,
    LauncherSettingsRecord,
)


def test_default_dcc_dev_root_uses_repo_parent():

    repo_root = Path('C:/dev/icarus-dcc')
    
    dcc_dev_root = default_dcc_dev_root(repo_root=repo_root)
    
    assert dcc_dev_root == Path('C:/dev')
    
def test_default_settings_path_uses_rez_config_folder():
    
    dcc_dev_root = Path('C:/dev')
    
    settings_path = default_settings_path(dcc_dev_root=dcc_dev_root)
    
    assert settings_path == Path('C:/dev/_rez/config/launcher_settings.json')
    
def test_load_settings_reads_json(tmp_path):
    
    settings_path = tmp_path / "launcher_settings.json"
    
    settings_path.write_text(
        """
        {
            "dcc_dev_root": "C:/fake/dcc",
            "maya": {
                "2024": {
                    "location": "C:/Fake/Maya2024"
                }
            }
        }
        """,
        encoding="utf-8"
    )
    
    settings = load_settings(
        settings_path=settings_path
    )
    
    assert settings['dcc_dev_root'] == 'C:/fake/dcc'
    assert settings['maya']['2024']['location'] == 'C:/Fake/Maya2024'
    
def test_rez_executable_uses_rez_install_scripts_folder():
    
    dcc_dev_root = Path("C:/dev")

    path = rez_executable(dcc_dev_root)

    assert path == Path("C:/dev/_rez/install/Scripts/rez/rez.exe")

def test_rez_config_file_uses_rez_config_folder():
    
    dcc_dev_root = Path("C:/dev")

    path = rez_config_file(dcc_dev_root)

    assert path == Path("C:/dev/_rez/config/rezconfig.py")
    
def test_launcher_config_stores_final_values():
    
    config = LauncherConfig(
        dcc_name='maya',
        version=2024,
        dcc_dev_root=Path('C:/dev'),
        install_location=Path('C:/Fake/Maya2024'),
        rez_package='maya-2024',
        rez_executable=Path('C:/dev/_rez/install/Scripts/rez/rez.exe'),
        rez_config_file=Path('C:/dev/_rez/config/rezconfig.py'),
        launch_command='maya',
        env_var_name='ICARUS_MAYA_2024_LOCATION'
    )
    
    assert config.rez_package == 'maya-2024'
    assert config.env_var_name == 'ICARUS_MAYA_2024_LOCATION'
    
def test_launcher_settings_record_from_settings():
    
    settings = {
        'dcc_dev_root': 'C:/fake/dcc',
        'maya': {
            '2024': {
                'location': 'C:/Fake/Maya2024'
            }
        }
    }
    
    record = LauncherSettingsRecord.from_settings(
        settings=settings
    )
    
    assert record.dcc_dev_root == Path('C:/fake/dcc')
    assert record.maya_locations[2024] == Path('C:/Fake/Maya2024')