import inspect
import importlib

# Import all classes from module_a
epmodel = importlib.import_module('.epmodel', 'epmodel')
for name, obj in inspect.getmembers(epmodel):
    if inspect.isclass(obj) and obj.__module__ == epmodel.__name__:
        globals()[name] = obj


from .builder import (
    ConstructionComplexFenestrationStateInput,
    ConstructionComplexFenestrationStateLayerInput,
    ConstructionComplexFenestrationStateGapInput,
    ConstructionComplexFenestrationStateBuilder,
    EnergyPlusModel,
)
