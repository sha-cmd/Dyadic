import pytest

@pytest.fixture
def inc():
    return 5


def pass_test(inc):
    assert inc == 5
