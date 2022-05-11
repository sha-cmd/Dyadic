from pytest import fixture


def pytest_addoption(parser):
    parser.addoption(
        "--luisappid",
        action="store"
    )
    parser.addoption(
        "--luisapikey",
        action="store"
    )
    parser.addoption(
        "--luisapihostname",
        action="store"
    )


@fixture()
def luisappid(request):
    return request.config.getoption("--luisappid")


@fixture()
def luisapikey(request):
    return request.config.getoption("--luisapikey")


@fixture()
def luisapihostname(request):
    return request.config.getoption("--luisapihostname")
