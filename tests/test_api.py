from pathlib import Path
import json
from epmodel import EnergyPlusModel
import pytest

@pytest.fixture
def test_data_dir():
    return Path(__file__).parent / 'data'

@pytest.fixture
def test_file(test_data_dir):
    return test_data_dir / "RefBldgPrimarySchoolNew2004_Chicago.epJSON"


def test_validate(test_file):
    with open(test_file, 'r') as f:
        json_data = json.load(f)
    model = EnergyPlusModel.model_validate(json_data)
    assert model.version is not None
