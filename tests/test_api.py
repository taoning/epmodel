from pathlib import Path
import json
from epmodel import EnergyPlusModel
import pytest

@pytest.fixture
def test_data_dir():
    return Path(__file__).parent / 'data'

@pytest.fixture
def test_file1(test_data_dir):
    return test_data_dir / "RefBldgPrimarySchoolNew2004_Chicago.epJSON"

@pytest.fixture
def test_file2(test_data_dir):
    return test_data_dir / "RefBldgMediumOfficeNew2004_Chicago_epJSON.epJSON"


def test_validate(test_file1):
    with open(test_file1, 'r') as f:
        json_data = json.load(f)
    model = EnergyPlusModel.model_validate(json_data)
    assert model.version is not None

def test_validate2(test_file2):
    with open(test_file2, 'r') as f:
        json_data = json.load(f)
    model = EnergyPlusModel.model_validate(json_data)
    assert model.version is not None
