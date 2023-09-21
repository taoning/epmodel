"""
Tests configuration
"""
import json
from pathlib import Path

from epmodel.builder import EnergyPlusModel

import pytest

@pytest.fixture(scope="session")
def test_data_dir():
    return Path(__file__).parent / 'data'

@pytest.fixture(scope="session")
def test_file1(test_data_dir):
    return test_data_dir / "RefBldgPrimarySchoolNew2004_Chicago.epJSON"

@pytest.fixture(scope="session")
def test_file2(test_data_dir):
    return test_data_dir / "RefBldgMediumOfficeNew2004_Chicago_epJSON.epJSON"

@pytest.fixture(scope="session")
def epmodel1(test_file1):
    with open(test_file1, 'r') as f:
        json_data = json.load(f)
    model = EnergyPlusModel.model_validate(json_data)
    assert model.version is not None
    return model

@pytest.fixture(scope="session")
def epmodel2(test_file2):
    with open(test_file2, 'r') as f:
        json_data = json.load(f)
    model = EnergyPlusModel.model_validate(json_data)
    assert model.version is not None
    return model
