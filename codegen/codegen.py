"""
This module uses datamodel-code-generator to generate the EnergyPlus
pydantic model. The schema is trimmed to only include the keys in keys.txt
"""

import json
from pathlib import Path

from datamodel_code_generator import (
    InputFileType,
    generate,
    DataModelType,
    LiteralType,
    PythonVersion,
)


# Load in the keys to keep from schema
key_paths = Path("keys2.txt")
keys = key_paths.read_text().splitlines()

# load schema
schema_path = Path("Energy+.schema.epJSON")
with open(schema_path) as f:
    schema = json.load(f)

root_props = schema["properties"]
trimmed_props = {k: v for k, v in root_props.items() if k in keys}

schema["properties"] = trimmed_props
json_schema = json.dumps(schema)
with open("trimmed_schema.json", "w") as f:
    f.write(json_schema)


# generate code
output = Path("epmodel.py")
generate(
    json_schema,
    input_file_type=InputFileType.JsonSchema,
    output=output,
    # set up the output model types
    output_model_type=DataModelType.PydanticV2BaseModel,
    snake_case_field=True,
    use_double_quotes=True,
    enum_field_as_literal=LiteralType.One,
    reuse_model=True,
    field_constraints=False,
    use_annotated=False,
    set_default_enum_member=True,
    target_python_version=PythonVersion.PY_38,
    class_name="EnergyPlusModel",
)
