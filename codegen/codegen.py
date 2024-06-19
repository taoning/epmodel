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

# Define the reusable enum
ep_boolean = {
    "type": "string",
    "enum": [
        "No",
        "Yes"
    ],
    "default": "No"
}

def remove_empty_string_enums(schema):
    if isinstance(schema, dict):
        for key, value in schema.items():
            if key == "enum" and isinstance(value, list):
                schema[key] = [item for item in value if item != ""]
            else:
                remove_empty_string_enums(value)
    elif isinstance(schema, list):
        for item in schema:
            remove_empty_string_enums(item)

# Add the reusable enum to the definitions section
# Function to replace enums with a reference to the reusable enum
def replace_enum_with_ref(obj):
    if isinstance(obj, dict):
        for key, value in list(obj.items()):
            if key == 'enum' and "No" in value and "Yes" in value:
                obj.clear()
                obj['$ref'] = "#/definitions/EPBoolean"
            else:
                replace_enum_with_ref(value)
    elif isinstance(obj, list):
        for item in obj:
            replace_enum_with_ref(item)

# Load in the keys to keep from schema
key_paths = Path("keys.txt")
keys = key_paths.read_text().splitlines()

# load schema
schema_path = Path("Energy+.schema.epJSON")
with open(schema_path) as f:
    schema = json.load(f)


# Replace yes no enums in the schema
replace_enum_with_ref(schema)

# Remove empty strings from enum lists
remove_empty_string_enums(schema)

root_props = schema["properties"]
trimmed_props = {k: v for k, v in root_props.items() if k in keys}

schema["properties"] = trimmed_props
if 'definitions' not in schema:
    schema['definitions'] = {}
schema['definitions']['EPBoolean'] = ep_boolean
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
    field_constraints=True,
    use_annotated=True,
    set_default_enum_member=True,
    target_python_version=PythonVersion.PY_39,
    class_name="EnergyPlusModel",
)
