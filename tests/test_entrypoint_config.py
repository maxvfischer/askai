from pathlib import Path
from typing import List, Callable

import pytest
import yaml
from pytest import MonkeyPatch

from askai.entrypoint_config import _reset, _update_all, _model, _num_answers, _max_tokens, _temperature, _top_p, \
    _frequency_penalty, _presence_penalty
from askai.utils import ConfigHelper, AvailableModels
from tests.test_config_helper import mock_input_value


CONFIG_FILE_NAME = "config.yml"


@pytest.mark.parametrize(
    "user_input",
    ["n", "N", "No", "no", "1", "\n"]
)
def test_reset_abort_user_input(monkeypatch: MonkeyPatch, tmp_path: Path, user_input: str) -> None:
    config_path = tmp_path / CONFIG_FILE_NAME

    mock_input_value(value=user_input, monkeypatch=monkeypatch)

    assert not config_path.is_file()
    _reset(config_path=config_path)
    assert not config_path.is_file()


@pytest.mark.parametrize(
    "user_input",
    ["y", "Y", "yes", "Yes"]
)
def test_reset_verified_user_input(monkeypatch: MonkeyPatch, tmp_path: Path, user_input: str) -> None:
    config_path = tmp_path / CONFIG_FILE_NAME

    mock_input_value(value=user_input, monkeypatch=monkeypatch)

    assert not config_path.is_file()
    _reset(config_path=config_path)
    assert config_path.is_file()
    with open(config_path, "r", encoding="utf8") as f:
        assert yaml.safe_load(f) == ConfigHelper().as_dict()


@pytest.mark.parametrize(
    "bad_user_inputs",
    [
        ["bad", "bad", "bad"],  # input_model
        ["1", "bad", "bad", "bad"],  # input_num_answers
        ["1", "1", "bad", "bad", "bad"],  # input_max_tokens
        ["1", "1", "15", "bad", "bad", "bad"],  # input_temperature
        ["1", "1", "15", "0.0", "bad", "bad", "bad"],  # input_top_p
        ["1", "1", "15", "0.0", "0.0", "bad", "bad", "bad"],  # input_frequency_penalty
        ["1", "1", "15", "0.0", "0.0", "0.0", "bad", "bad", "bad"],  # input_presence_penalty
    ]
)
def test_update_all_bad_user_input(monkeypatch: MonkeyPatch, bad_user_inputs: List[str]) -> None:
    bad_user_inputs = iter(bad_user_inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(bad_user_inputs))

    with pytest.raises(SystemExit):
        _update_all(config_path=Path("does", "not", "matter", "dummy.yml"))


def test_update_all_good_user_input(monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    config_path = tmp_path / CONFIG_FILE_NAME
    expected_config = {
        "model": "text-ada-001",
        "num_answers": 42,
        "max_tokens": 42,
        "temperature": 0.42,
        "top_p": 0.42,
        "frequency_penalty": 0.42,
        "presence_penalty": 0.42
    }

    good_user_inputs = iter(["1", "42", "42", "0.42", "0.42", "0.42", "0.42"])
    monkeypatch.setattr('builtins.input', lambda _: next(good_user_inputs))

    _assert_config_update(config_path=config_path, config_update_func=_update_all, expected_config=expected_config)


@pytest.mark.parametrize(
    "config_update_func",
    [
        _model,
        _num_answers,
        _max_tokens,
        _temperature,
        _top_p,
        _frequency_penalty,
        _presence_penalty
    ]
)
def test_update_individual_bad_user_input(monkeypatch: MonkeyPatch, config_update_func: Callable[[Path], None]) -> None:
    bad_user_input = "bad"
    mock_input_value(value=bad_user_input, monkeypatch=monkeypatch)

    with pytest.raises(SystemExit):
        config_update_func(Path("does", "not", "matter", "dummy.yml"))


def test_update_model_good_user_input(monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    config_path = tmp_path / CONFIG_FILE_NAME
    good_user_input = 1

    expected_config = ConfigHelper().as_dict()
    expected_config["model"] = AvailableModels(good_user_input).name.replace("_", "-").lower()

    mock_input_value(value=str(good_user_input), monkeypatch=monkeypatch)

    _assert_config_update(config_path=config_path, config_update_func=_model, expected_config=expected_config)


@pytest.mark.parametrize(
    "config_update_func, instance_variable_name",
    [
        (_temperature, "temperature"),
        (_top_p, "top_p"),
        (_frequency_penalty, "frequency_penalty"),
        (_presence_penalty, "presence_penalty")
    ]
)
def test_update_float_good_user_input(monkeypatch: MonkeyPatch, tmp_path: Path, config_update_func: Callable[[Path], None], instance_variable_name: str) -> None:
    config_path = tmp_path / CONFIG_FILE_NAME
    good_user_input = 0.42

    expected_config = ConfigHelper().as_dict()
    expected_config[instance_variable_name] = good_user_input

    mock_input_value(value=str(good_user_input), monkeypatch=monkeypatch)

    _assert_config_update(config_path=config_path, config_update_func=config_update_func, expected_config=expected_config)


@pytest.mark.parametrize(
    "config_update_func, instance_variable_name",
    [
        (_num_answers, "num_answers"),
        (_max_tokens, "max_tokens")
    ]
)
def test_update_int_good_user_input(monkeypatch: MonkeyPatch, tmp_path: Path, config_update_func: Callable[[Path], None], instance_variable_name: str) -> None:
    config_path = tmp_path / CONFIG_FILE_NAME
    good_user_input = 42

    expected_config = ConfigHelper().as_dict()
    expected_config[instance_variable_name] = good_user_input

    mock_input_value(value=str(good_user_input), monkeypatch=monkeypatch)

    _assert_config_update(config_path=config_path, config_update_func=config_update_func, expected_config=expected_config)


def _assert_config_update(config_path: Path, config_update_func: Callable[[Path], None], expected_config: dict) -> None:
    ConfigHelper().reset(config_path=config_path)  # Create config to update
    with open(config_path, "r", encoding="utf8") as f:
        assert yaml.safe_load(f) != expected_config

    config_update_func(config_path)

    with open(config_path, "r", encoding="utf8") as f:
        assert yaml.safe_load(f) == expected_config
