from pytest import fixture


def pytest_addoption(parser):
    parser.addoption(
        "--luisapiid",
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
def luisapiid(request):
    return request.config.getoption("--luisapiid")

@fixture()
def luisapikey(request):
    return request.config.getoption("--luisapikey")

@fixture()
def luisapihostname(request):
    return request.config.getoption("--luisapihostname")
