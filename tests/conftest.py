import json
import os
from pathlib import Path

import pytest
import yaml
from confz import ConfZDataSource

import script_master.const
from script_master import cli
from script_master.settings import Settings


def pytest_sessionstart():
    pass


def pytest_unconfigure():
    pass


@pytest.fixture(autouse=True)
def before_test(tmp_path):
    os.environ[script_master.const.HOME_DIR_VARNAME] = str(tmp_path.parent)
    print(f"\nHOMEPATH={tmp_path.parent}")
    cli.init()


@pytest.fixture(scope='session')
def settings(tmp_path):
    new_source = ConfZDataSource(
        data={"workplanner_host": "", "executor_host": ""}
    )
    with Settings.change_config_sources(new_source):
        yield


@pytest.fixture(scope='session')
def variables_json():
    data = {'int': 1, 'list': ['s1', 's2'], 'str': 'name', 'float': 1.1}
    path = Settings().VARIABLES_DIR / "test_variables.json"
    with open(path, 'w') as f:
        json.dump(data, f)

    yield path, data


@pytest.fixture(scope='session')
def variables_yaml():
    data = {'int': 1, 'list': ['s1', 's2'], 'str': 'name', 'float': 1.1}
    path = Settings().VARIABLES_DIR / "test_variables.yaml"
    with open(path, 'w') as f:
        yaml.dump(data, f)

    yield path, data


@pytest.fixture(scope='session')
def variables_text():
    data = "SELECT 1"
    path = Path(Settings().VARIABLES_DIR / "test_variables.txt")
    path.write_text(data)

    yield path, data
