import pytest

from askai.utils import _is_int, _is_float


@pytest.mark.parametrize(
    "value, is_int",
    [
        ("1", True),
        ("a", False),
        ("0.1", False),
    ]
)
def test_is_int(value: str, is_int: bool) -> None:
    assert _is_int(value) == is_int


@pytest.mark.parametrize(
    "value, is_float",
    [
        ("1", True),
        ("1.0", True),
        ("a", False),
    ]
)
def test_is_float(value: str, is_float: bool) -> None:
    assert _is_float(value) == is_float
