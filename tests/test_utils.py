import pytest
from best_practices.utils import add_numbers, format_greeting


def test_add_numbers() -> None:
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0


@pytest.mark.parametrize(
    "name, expected",
    [
        ("Alice", "Hello, Alice!"),
        ("", "Hello, Stranger!"),
        ("World", "Hello, World!"),
    ],
)
def test_format_greeting(name: str, expected: str) -> None:
    assert format_greeting(name) == expected


def test_add_numbers_wrong_type() -> None:
    # This demonstrates why we use Mypy, but also how to test logic
    # pytest.raises can be used if you expect an error
    with pytest.raises(TypeError):
        # We tell mypy to ignore this intentional error for the test
        add_numbers("1", 2)  # type: ignore
