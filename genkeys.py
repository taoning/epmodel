"""
Generate a list of commonly used EnergyPlus model objects
from example files.
"""
import json
from pathlib import Path
import os
import subprocess as sp


eproot = Path("/Applications/EnergyPlus-23-1-0")
epegpath = eproot / "ExampleFiles"

# All DOE reference building models
refpaths = list(epegpath.glob("Ref*.idf"))

# ASHRAE 90.1 models
ashpaths = list(epegpath.glob("ASHRAE*.idf"))

# Complex fenestration models
cfspaths = list(epegpath.glob("Cmplx*.idf"))

# N Zone models
nzpaths = list(epegpath.glob("[0-9]Zone*.idf"))

# WCE models
wcepaths = list(epegpath.glob("WCE*.idf"))

# All models
allpaths = list(epegpath.glob("*.idf"))


epaths = [
    *refpaths,
    *ashpaths,
    *cfspaths,
]


keys = []
for pth in epaths:
    # convert to json
    sp.run(["energyplus", "--convert-only", str(pth)])
    json_path = pth.with_suffix(".epJSON").name
    with open(json_path) as f:
        data = json.load(f)
    # get keys
    keys.extend(list(data.keys()))
    os.remove(json_path)


with open("keys.txt", "w") as f:
    f.write("\n".join(list(set(keys))))
