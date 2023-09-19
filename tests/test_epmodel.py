from pathlib import Path
import json
from epmodel import (
    EnergyPlusModel,
)
from epmodel.epmodel import (
    WindowMaterialGas,
    GasType,
)

import pytest

def test_validate(epmodel1):
    assert epmodel1.version is not None

def test_validate2(epmodel2):
    assert epmodel2.version is not None

def test_validate_component():
    gas = WindowMaterialGas(
        gas_type=GasType.air,
        thickness=0.2,
        molecular_weight=28.97,
    )
    gas.thickness = -0.3
    with pytest.raises(Exception) as e_info:
        WindowMaterialGas.model_validate(gas.__dict__)
