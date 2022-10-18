
import pytest


@pytest.mark.usefixtures
def test_case():
    assert 10 == 10

