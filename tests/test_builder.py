from pathlib import Path
import json
from epmodel.epmodel import (
    GasType,
)
from epmodel.builder import (
    ConstructionComplexFenestrationStateInput,
    ConstructionComplexFenestrationStateBuilder
)

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


@pytest.fixture
def test_ccfs_three_layers():
    input = ConstructionComplexFenestrationStateInput(
        layer_names=["test"],
        product_types=["glazing", "glazing", "shading"],
        layer_thickness=[0.003, 0.003, 0.001],
        gap_thickness=[0.01, 0.01],
        gap_gas=[GasType.Air, GasType.Air],
        layer_conductivity=[],
        layer_emissivity_back=[],
        layer_emissivity_front=[],
        layer_ir_transmittance=[],
        solar_reflectance_back= [],
        solar_transmittance_back=[] ,
        visible_transmittance_back= [],
        visible_transmittance_front= [],
        layer_absorptance_back= [],
        layer_absorptance_front= [],
        gap_absorptance_back=[],
        gap_absorptance_front=[],
    )
    assert input.layer_names == ["test"]
    return input

def test_ccfs_builder(epmodel1, test_ccfs_input):
    builder = ConstructionComplexFenestrationStateBuilder("test", epmodel1, test_ccfs_input)

