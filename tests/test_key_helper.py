from pathlib import Path

import pytest
import pytest_mock.plugin

from askai.utils import KeyHelper


DUMMY_KEY = "DUMMY_KEY"


def test_input_bad(mocker: pytest_mock.plugin.MockerFixture) -> None:
    is_valid_api_key = False
    mocker.patch("askai.utils.KeyHelper._is_valid_api_key", lambda _, __: is_valid_api_key)
    mocker.patch('askai.utils.getpass', lambda _: DUMMY_KEY)
    with pytest.raises(SystemExit):
        key_helper = KeyHelper()
        key_helper.input()


def test_input_good(mocker: pytest_mock.plugin.MockerFixture) -> None:
    is_valid_api_key = True
    mocker.patch("askai.utils.KeyHelper._is_valid_api_key", lambda _, __: is_valid_api_key)
    mocker.patch('askai.utils.getpass', lambda _: DUMMY_KEY)

    key_helper = KeyHelper()
    key_helper.input()

    assert key_helper._api_key == DUMMY_KEY


def test_save(tmp_path: Path) -> None:
    api_key_path = tmp_path / "key"

    assert not api_key_path.is_file()

    key_helper = KeyHelper()
    key_helper._api_key = DUMMY_KEY
    key_helper.save(api_key_path=api_key_path)

    assert api_key_path.read_text(encoding="utf8") == DUMMY_KEY


def test_remove_file_does_not_exist(tmp_path: Path) -> None:
    api_key_path = tmp_path / "key"

    with pytest.raises(SystemExit):
        KeyHelper().remove(api_key_path=api_key_path)


def test_remove_file_exist(tmp_path: Path) -> None:
    api_key_path = tmp_path / "key"
    api_key_path.write_text(DUMMY_KEY)

    assert api_key_path.is_file()
    KeyHelper().remove(api_key_path=api_key_path)
    assert not api_key_path.is_file()


def test_from_file_does_not_exist(tmp_path: Path) -> None:
    api_key_path = tmp_path / "key"

    with pytest.raises(SystemExit):
        _ = KeyHelper().from_file(api_key_path=api_key_path)


def test_from_file_does_exist(tmp_path: Path) -> None:
    api_key_path = tmp_path / "key"
    api_key_path.write_text(DUMMY_KEY)

    actual_key = KeyHelper().from_file(api_key_path=api_key_path)

    assert DUMMY_KEY == actual_key
