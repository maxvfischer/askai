from askai.utils import AvailableModels


def test_name_values() -> None:
    assert "TEXT_ADA_001" in AvailableModels.__members__
    assert "TEXT_BABBAGE_001" in AvailableModels.__members__
    assert "TEXT_CURIE_001" in AvailableModels.__members__
    assert "TEXT_DAVINCI_003" in AvailableModels.__members__


def test_members_as_list() -> None:
    enum_list = AvailableModels.members_as_list(openai_style=False)
    assert type(enum_list) == list
    assert len(AvailableModels) == len(enum_list)
    for name in AvailableModels.__members__:
        assert name in enum_list


def test_members_as_list_openai_style() -> None:
    enum_list = AvailableModels.members_as_list(openai_style=True)
    assert type(enum_list) == list
    assert len(AvailableModels) == len(enum_list)
    for name in AvailableModels.__members__:
        assert name.replace("_", "-").lower() in enum_list
