

import json
from pathlib import Path

from epmodel import EnergyPlusModel

ipath = Path("data/RefBldgPrimarySchoolNew2004_Chicago.epJSON")

with open(ipath) as f:
    data = json.load(f)

model = EnergyPlusModel.model_validate(data)


