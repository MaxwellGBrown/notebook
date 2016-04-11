import pytest


@pytest.fixture
def fixture1(request):
    fixture_list = list(['fixture1'])
    return fixture_list


@pytest.fixture
def fixture2(fixture1):
    new_fixture_list = list(fixture1)
    new_fixture_list.append("fixture2")
    return new_fixture_list


@pytest.fixture
@pytest.mark.usefixtures("fixture2")
def fixture3(request):
    new_fixture_list = list(request._funcargs['fixture2'])
    new_fixture_list.append("fixture3")
    return new_fixture_list


# works because of pytests arg-fixture-matching black magic
@pytest.mark.usefixtures("fixture2")
def test_nested_fixtures_are_nested(request):
    fixture1_list = request._funcargs['fixture1']
    assert "fixture1" in fixture1_list
    assert "fixture2" not in fixture1_list
    assert "fixture3" not in fixture1_list

    fixture2_list = request._funcargs['fixture2']
    assert "fixture1" in fixture2_list
    assert "fixture2" in fixture2_list
    assert "fixture3" not in fixture2_list


# if a fixture uses pytest.mark.usesfixtures, the nested fixtures must also
# be supplied (e.g. if we want fixture3, fixture2 & fixture1 must also be used)
@pytest.mark.usefixtures("fixture1", "fixture2", "fixture3")
def test_nested_fixtures_cant_use_mark(request):
    fixture3_list = request._funcargs['fixture3']
    assert "fixture1" in fixture3_list
    assert "fixture2" in fixture3_list
    assert "fixture3" in fixture3_list

