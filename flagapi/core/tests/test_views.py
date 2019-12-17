import pytest

from flagapi.core.views import line_breaker


@pytest.mark.parametrize("l_breaker, expected", [
    ("\r\n", "\r\n"),
    ("\n", "\n"),
    ("\r", "\r"),
    ("", ""),
    ]
)
def test_line_breaker(client, l_breaker, expected):
    assert l_breaker == line_breaker(l_breaker)
