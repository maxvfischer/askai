from pathlib import Path

import pytest
import pytest_mock
import yaml
from askai.entrypoint_init import _init
from askai.utils import ConfigHelper

DUMMY_KEY = "DUMMY_KEY"


def test_init_bad_input(mocker: pytest_mock.plugin.MockerFixture) -> None:
    is_valid_api_key = False
    mocker.patch("askai.utils.KeyHelper._is_valid_api_key", lambda _, __: is_valid_api_key)
    mocker.patch('askai.utils.getpass', lambda _: DUMMY_KEY)

    with pytest.raises(SystemExit):
        _init()


def test_init_written_files(mocker: pytest_mock.plugin.MockerFixture, tmp_path: Path) -> None:
    is_valid_api_key = True
    api_key_path = tmp_path / "key"
    config_path = tmp_path / "config.yml"

    mocker.patch("askai.utils.KeyHelper._is_valid_api_key", lambda _, __: is_valid_api_key)
    mocker.patch('askai.utils.getpass', lambda _: DUMMY_KEY)

    assert not api_key_path.is_file()
    assert not config_path.is_file()

    _init(api_key_path=api_key_path, config_path=config_path)

    assert api_key_path.is_file()
    assert api_key_path.read_text() == DUMMY_KEY
    assert config_path.is_file()

    with open(config_path, "r", encoding="utf8") as f:
        assert yaml.safe_load(f) == ConfigHelper().as_dict()
