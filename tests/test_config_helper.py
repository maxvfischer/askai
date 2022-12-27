from functools import partial
from pathlib import Path
from typing import Union, Callable

import pytest
from pytest import MonkeyPatch
import yaml

from askai.constants import DEFAULT_MODEL, DEFAULT_TEMPERATURE, DEFAULT_NUM_ANSWERS, DEFAULT_MAX_TOKENS, DEFAULT_TOP_P, \
    DEFAULT_FREQUENCY_PENALTY, DEFAULT_PRESENCE_PENALTY
from askai.utils import ConfigHelper, AvailableModels

DUMMY_CONFIG_CONTENT = {
    "model": "text-ada-001",
    "num_answers": 10,
    "max_tokens": 10,
    "temperature": 0.1,
    "top_p": 0.1,
    "frequency_penalty": 0.1,
    "presence_penalty": 0.1
}


def test_default_init() -> None:
    config_helper = ConfigHelper()
    assert config_helper.model == DEFAULT_MODEL
    assert config_helper.num_answers == DEFAULT_NUM_ANSWERS
    assert config_helper.max_tokens == DEFAULT_MAX_TOKENS
    assert config_helper.temperature == DEFAULT_TEMPERATURE
    assert config_helper.top_p == DEFAULT_TOP_P
    assert config_helper.frequency_penalty == DEFAULT_FREQUENCY_PENALTY
    assert config_helper.presence_penalty == DEFAULT_PRESENCE_PENALTY


def test_init_with_args_and_as_dict() -> None:
    config_helper = ConfigHelper(**DUMMY_CONFIG_CONTENT)
    assert DUMMY_CONFIG_CONTENT == config_helper.as_dict()


def test_from_file_config_exists(tmp_path: Path) -> None:
    config_path = tmp_path / "dummy_config.yml"
    _write_config_file(content=DUMMY_CONFIG_CONTENT, path=config_path)

    config_helper = ConfigHelper.from_file(config_path=config_path)
    assert DUMMY_CONFIG_CONTENT == config_helper.as_dict()


def _write_config_file(content: dict, path: Path) -> None:
    with open(path, "w") as f:
        yaml.dump(content, f)


def test_from_file_config_does_not_exist(tmp_path: Path) -> None:
    config_path = tmp_path / "dummy_config.yml"
    with pytest.raises(SystemExit):
        _ = ConfigHelper.from_file(config_path=config_path)


@pytest.mark.parametrize(
    "user_input",
    ["1", "2", "3", "4"]
)
def test_input_model_ok(monkeypatch: MonkeyPatch, user_input: str) -> None:
    _mock_input_value(value=user_input, monkeypatch=monkeypatch)
    config_helper = ConfigHelper()
    config_helper.input_model(max_input_tries=1)
    assert config_helper.model == AvailableModels(int(user_input)).name.replace("_", "-").lower()


def test_input_num_answer_ok(monkeypatch: MonkeyPatch) -> None:
    user_input = "2"
    min_value = int(user_input) - 1
    _mock_input_value(value=user_input, monkeypatch=monkeypatch)

    config_helper = ConfigHelper()
    assert int(user_input) != config_helper.num_answers
    config_helper.input_num_answer(
        min_value=min_value,
        max_input_tries=1
    )
    assert int(user_input) == config_helper.num_answers


def test_input_max_token_ok(monkeypatch: MonkeyPatch) -> None:
    user_input = "2"
    min_value = int(user_input) - 1
    _mock_input_value(value=user_input, monkeypatch=monkeypatch)

    config_helper = ConfigHelper()
    assert int(user_input) != config_helper.max_tokens
    config_helper.input_max_token(
        min_value=min_value,
        max_input_tries=1
    )
    assert int(user_input) == config_helper.max_tokens


def test_input_temperature_ok(monkeypatch: MonkeyPatch) -> None:
    user_input = "1.5"
    min_value = float(user_input) - 1.0
    max_value = float(user_input) + 1.0
    _mock_input_value(value=user_input, monkeypatch=monkeypatch)

    config_helper = ConfigHelper()
    assert float(user_input) != config_helper.temperature
    config_helper.input_temperature(
        min_value=min_value,
        max_value=max_value,
        max_input_tries=1
    )
    assert float(user_input) == config_helper.temperature


def test_input_top_p_ok(monkeypatch: MonkeyPatch) -> None:
    user_input = "1.5"
    min_value = float(user_input) - 1.0
    max_value = float(user_input) + 1.0
    _mock_input_value(value=user_input, monkeypatch=monkeypatch)

    config_helper = ConfigHelper()
    assert float(user_input) != config_helper.top_p
    config_helper.input_top_p(
        min_value=min_value,
        max_value=max_value,
        max_input_tries=1
    )
    assert float(user_input) == config_helper.top_p


def test_input_frequency_penalty_ok(monkeypatch: MonkeyPatch) -> None:
    user_input = "1.5"
    min_value = float(user_input) - 1.0
    max_value = float(user_input) + 1.0
    _mock_input_value(value=user_input, monkeypatch=monkeypatch)

    config_helper = ConfigHelper()
    assert float(user_input) != config_helper.frequency_penalty
    config_helper.input_frequency_penalty(
        min_value=min_value,
        max_value=max_value,
        max_input_tries=1
    )
    assert float(user_input) == config_helper.frequency_penalty


def test_input_presence_penalty_ok(monkeypatch: MonkeyPatch) -> None:
    user_input = "1.5"
    min_value = float(user_input) - 1.0
    max_value = float(user_input) + 1.0
    _mock_input_value(value=user_input, monkeypatch=monkeypatch)

    config_helper = ConfigHelper()
    assert float(user_input) != config_helper.presence_penalty
    config_helper.input_presence_penalty(
        min_value=min_value,
        max_value=max_value,
        max_input_tries=1
    )
    assert float(user_input) == config_helper.presence_penalty


@pytest.mark.parametrize(
    "user_input",
    [
        "-1",  # Too low
        "5",  # Too high
    ]
)
def test_input_model_out_of_allowed_range(monkeypatch: MonkeyPatch, user_input: str) -> None:
    _mock_input_value(value=user_input, monkeypatch=monkeypatch)
    with pytest.raises(SystemExit):
        config_helper = ConfigHelper()
        config_helper.input_model(max_input_tries=1)


@pytest.mark.parametrize(
    "input_func",
    [
        ConfigHelper().input_temperature,
        ConfigHelper().input_top_p,
        ConfigHelper().input_frequency_penalty,
        ConfigHelper().input_presence_penalty,
    ]
)
def test_input_min_max_out_of_range(monkeypatch: MonkeyPatch, input_func: Callable) -> None:
    user_input_too_low = "1.0"
    user_input_too_high = "5.0"
    min_value = float(user_input_too_low) + 1.0
    max_value = float(user_input_too_high) - 1.0

    with pytest.raises(SystemExit):
        _mock_input_value(value=user_input_too_low, monkeypatch=monkeypatch)
        input_func(
            min_value=min_value,
            max_value=max_value,
            max_input_tries=1
        )
    with pytest.raises(SystemExit):
        _mock_input_value(value=user_input_too_high, monkeypatch=monkeypatch)
        input_func(
            min_value=min_value,
            max_value=max_value,
            max_input_tries=1
        )


@pytest.mark.parametrize(
    "input_func",
    [
        ConfigHelper().input_num_answer,
        ConfigHelper().input_max_token,
    ]
)
def test_input_min_out_of_range(monkeypatch: MonkeyPatch, input_func: Callable) -> None:
    user_input_too_low = "1.0"
    min_value = float(user_input_too_low) + 1.0

    with pytest.raises(SystemExit):
        _mock_input_value(value=user_input_too_low, monkeypatch=monkeypatch)
        input_func(
            min_value=min_value,
            max_input_tries=1
        )


def _mock_input_value(value: str, monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr('builtins.input', lambda _: value)


def test_update(tmp_path: Path) -> None:
    config_path = tmp_path / "dummy_config.yml"

    config_helper = ConfigHelper(**DUMMY_CONFIG_CONTENT)
    config_helper.update(config_path=config_path)

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    assert config == config_helper.as_dict()


def test_reset(tmp_path: Path) -> None:
    config_path = tmp_path / "dummy_config.yml"

    config_helper = ConfigHelper(**DUMMY_CONFIG_CONTENT)
    config_helper.update(config_path=config_path)

    with open(config_path, "r") as f:
        config_before_reset = yaml.safe_load(f)

    config_helper.reset(config_path=config_path)

    with open(config_path, "r") as f:
        config_after_reset = yaml.safe_load(f)

    assert config_before_reset != config_after_reset
    assert config_after_reset == ConfigHelper().as_dict()
