# epmodel

epmodel is a pydantic (V2) data model for EnergyPlus modeling.
The data model code itself is automatically generated from the EnergyPlus
JSON schema using the `datamodel-code-generator` package.



## Usage

Due to the size of the official EnergyPlus JSON schema, we reduce the data model scope
down the a few commonly used ones. The name of these data models are list in the `keys.txt`
file, which is also used to generate the data model code.

### Expanding the scope of data model

We can add object to the data model by adding names directly to the `keys.txt` file.

### Generate the source code

To generate the source code, run the following command inside the `codegen` directory:

```bash
python codegen.py
```

As a result, a `src/epmodel/model.py` file will be a generated with the data model code.

### Using the data model
Using the data model object is as simple as:

```python
import json
from epmodel import EnergyPlusModel

with open("model.epJSON", "r") as f:
    data = json.load(f)
model = EnergyPlusModel.model_validate(data)
```

The code above loads in the EnergyPlus epJSON model and validate it against the data model.
If the mode is valid, a `EnergyPlusModel` object will be returned, otherwise, an `ValidationError`
will be raised.

One of the benefits of having such data model, beyond data validation, is that we can use
autocomplete in IDE to help use write the code.

## Dependencies

* [pydantic](https://github.com/pydantic/pydantic)

### Dependency for code generation

* [datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator)
