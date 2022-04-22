import pytest

@pytest.fixture
def inc():
    return 5


def pass_test(inc):
    for x in inc:
        assert x == 5
