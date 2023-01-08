from pathlib import Path

import pytest
import pytest_mock
from pytest import MonkeyPatch

from askai.entrypoint_key import _add, _remove
from tests.test_config_helper import mock_input_value

DUMMY_KEY = "DUMMY_KEY"


def test_add_key_bad_user_input(mocker: pytest_mock.plugin.MockerFixture) -> None:
    is_valid_api_key = False
    mocker.patch("askai.utils.KeyHelper._is_valid_api_key", lambda _, __: is_valid_api_key)
    mocker.patch('askai.utils.getpass', lambda _: DUMMY_KEY)
    with pytest.raises(SystemExit):
        _add()


def test_add_key_good_user_input(mocker: pytest_mock.plugin.MockerFixture, tmp_path: Path) -> None:
    api_key_path = tmp_path / "key"
    is_valid_api_key = True
    mocker.patch("askai.utils.KeyHelper._is_valid_api_key", lambda _, __: is_valid_api_key)
    mocker.patch('askai.utils.getpass', lambda _: DUMMY_KEY)

    assert not api_key_path.is_file()
    _add(api_key_path=api_key_path)
    assert api_key_path.read_text() == DUMMY_KEY


@pytest.mark.parametrize(
    "user_input",
    ["n", "N", "No", "no", "1", "\n"]
)
def test_remove_abort_user_input(monkeypatch: MonkeyPatch, tmp_path: Path, user_input: str) -> None:
    api_key_path = tmp_path / "key"

    mock_input_value(value=user_input, monkeypatch=monkeypatch)

    api_key_path.write_text(DUMMY_KEY)

    assert api_key_path.is_file()
    _remove(api_key_path=api_key_path)
    assert api_key_path.is_file()


@pytest.mark.parametrize(
    "user_input",
    ["y", "Y", "yes", "Yes"]
)
def test_remove_verified_user_input(monkeypatch: MonkeyPatch, tmp_path: Path, user_input: str) -> None:
    api_key_path = tmp_path / "key"

    mock_input_value(value=user_input, monkeypatch=monkeypatch)

    api_key_path.write_text(DUMMY_KEY)

    assert api_key_path.is_file()
    _remove(api_key_path=api_key_path)
    assert not api_key_path.is_file()
