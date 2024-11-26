"""
Test epmodel systems builder
"""

import pytest

from epmodel.builder import (
    ConstructionComplexFenestrationStateBuilder,
    ConstructionComplexFenestrationStateInput,
    ConstructionComplexFenestrationStateLayerInput,
    GlazingLayerType,
)
from epmodel.epmodel import GasType, WindowMaterialGas


@pytest.fixture
def layer1_input():
    return ConstructionComplexFenestrationStateLayerInput(
        name="layer1",
        product_type=GlazingLayerType.glazing,
        thickness=0.003,
        conductivity=1.0,
        emissivity_back=0.3,
        emissivity_front=0.3,
        infrared_transmittance=0,
        directional_absorptance_back=[0 for _ in range(145)],
        directional_absorptance_front=[0 for _ in range(145)],
    )


@pytest.fixture
def layer2_input():
    return ConstructionComplexFenestrationStateLayerInput(
        name="layer2",
        product_type=GlazingLayerType.glazing,
        thickness=0.003,
        conductivity=1.0,
        emissivity_back=0.3,
        emissivity_front=0.3,
        infrared_transmittance=0,
        directional_absorptance_back=[0 for _ in range(145)],
        directional_absorptance_front=[0 for _ in range(145)],
    )


@pytest.fixture
def input(layer1_input, layer2_input):
    return ConstructionComplexFenestrationStateInput(
        layers=[layer1_input, layer2_input],
        gaps=[WindowMaterialGas(gas_type=GasType.air, thickness=0.01)],
        solar_reflectance_back=[[0 for _ in range(145)] for _ in range(145)],
        solar_transmittance_front=[[0 for _ in range(145)] for _ in range(145)],
        visible_reflectance_back=[[0 for _ in range(145)] for _ in range(145)],
        visible_transmittance_front=[[0 for _ in range(145)] for _ in range(145)],
    )


def test_ccfs_builder(epmodel1, input):
    builder = ConstructionComplexFenestrationStateBuilder("test", epmodel1, input)
    builder.add_to_enenrgyplus_model()
    assert epmodel1.construction_complex_fenestration_state is not None
    assert epmodel1.construction_complex_fenestration_state["test"] is not None
