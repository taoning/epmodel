"""
Functions: helper function usually to create base level components
Classes: Factory class to create systems
"""
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

from epmodel import epmodel as epm


class Spectrum(Enum):
    """Spectrum for optical properties."""

    solar = "solar"
    visible = "visible"


class Direction(Enum):
    """Direction for optical properties."""

    front = "front"
    back = "back"


class RadiativeType(Enum):
    """Radiative type for optical properties."""

    transmittance = "transmittance"
    reflectance = "reflectance"
    absorptance = "absorptance"


class GlazingLayerType(Enum):
    """Product type for layer."""

    glazing = "glazing"
    shading = "shading"


class ConstructionComplexFenestrationStateInput(BaseModel):
    """Input for ConstructionComplexFenestrationState."""

    layer_names: List[str]
    product_types: List[str]
    layer_thickness: List[float]
    gap_thickness: List[float]
    gap_gas: List[epm.GasType]
    layer_emissivity_back: List[float]
    layer_emissivity_front: List[float]
    layer_conductivity: List[float]
    layer_ir_transmittance: List[float]
    solar_reflectance_back: List[List[float]]
    solar_transmittance_back: List[List[float]]
    visible_transmittance_back: List[List[float]]
    visible_transmittance_front: List[List[float]]
    layer_absorptance_back: List[List[float]]
    layer_absorptance_front: List[List[float]]
    gap_absorptance_back: List[List[float]]
    gap_absorptance_front: List[List[float]]
    matrix_basis: str = "Full Klems"


def get_matrix_two_dimension_single_row(matrix: List[float]) -> epm.MatrixTwoDimension:
    """Build MatrixTwoDimension object from single row matrix.

    Args:
        matrix: single row matrix

    Returns:
        MatrixTwoDimension object
    """
    return epm.MatrixTwoDimension(
        number_of_columns=len(matrix),
        number_of_rows=1,
        values=[epm.Value(value=val) for val in matrix],
    )


def get_matrix_two_dimension(matrix: List[List[float]]) -> epm.MatrixTwoDimension:
    """Get MatrixTwoDimension object from matrix.

    Args:
        matrix: List of list of float matrix data

    Returns:
        MatrixTwoDimension object
    """
    return epm.MatrixTwoDimension(
        number_of_columns=len(matrix[0]),
        number_of_rows=len(matrix),
        values=[epm.Value(value=val) for row in matrix for val in row],
    )


class ConstructionComplexFenestrationStateBuilder:
    """Builder class for ConstructionComplexFenestrationState."""

    def __init__(
        self,
        name: str,
        energyplus_model: "EnergyPlusModel",
        input: Optional[ConstructionComplexFenestrationStateInput],
    ):
        self.energyplus_model = energyplus_model
        self.name = name
        self.attributes = {}
        if input is not None:
            self.set_all_input(input)

    def add_to_enenrgyplus_model(self):
        self.energyplus_model.add(
            "construction_complex_fenestration_state",
            self.name,
            epm.ConstructionComplexFenestrationState(**self.attributes),
        )

    def set_all_input(self, input: ConstructionComplexFenestrationStateInput):
        if input.matrix_basis == "Full Klems":
            basis_matrix_name = "FullKlemsBasis"
            self.set_basis_matrix_name(basis_matrix_name)
        else:
            raise NotImplementedError("Only Full Klems is supported")

        # Fixed basis type, basis symmetry type, and window thermal model
        self.set_basis_type(epm.BasisType.lbnlwindow)
        self.set_basis_symmetry_type(epm.BasisSymmetryType.none)
        self.set_window_thermal_model("ThermParam_1")

        self.set_optical_complex_matrix_name(
            Spectrum.solar,
            Direction.back,
            RadiativeType.reflectance,
            f"{self.name}_RbSol",
            input.solar_reflectance_back,
        )
        self.set_optical_complex_matrix_name(
            Spectrum.solar,
            Direction.back,
            RadiativeType.transmittance,
            f"{self.name}_TfSol",
            input.solar_transmittance_back,
        )
        self.set_optical_complex_matrix_name(
            Spectrum.visible,
            Direction.back,
            RadiativeType.transmittance,
            f"{self.name}_Tbvis",
            input.visible_transmittance_back,
        )
        self.set_optical_complex_matrix_name(
            Spectrum.visible,
            Direction.front,
            RadiativeType.transmittance,
            f"{self.name}_Tfvis",
            input.visible_transmittance_front,
        )

        for idx, fabs in enumerate(input.layer_absorptance_front):
            self.set_layer_directional_absorptance_matrix_name(
                idx + 1,
                Direction.front,
                f"{self.name}_layer_{idx+1}_fAbs",
                fabs,
            )
        for idx, babs in enumerate(input.layer_absorptance_back):
            self.set_layer_directional_absorptance_matrix_name(
                idx + 1,
                Direction.back,
                f"{self.name}_layer_{idx+1}_bAbs",
                babs,
            )
        for idx, gas in enumerate(input.gap_gas):
            self.set_gap(
                idx + 1,
                f"{self.name}_gap_{idx + 1}",
                gas,
                input.gap_thickness[idx],
            )
        for idx, gapabs in enumerate(input.gap_absorptance_back):
            self.set_cfs_gap_directional_absorptance_matrix_name(
                idx + 1,
                Direction.back,
                f"{self.name}_gap_{idx+1}_bAbs",
                gapabs,
            )
        for idx, gapabs in enumerate(input.gap_absorptance_front):
            self.set_cfs_gap_directional_absorptance_matrix_name(
                idx + 1,
                Direction.front,
                f"{self.name}_gap_{idx+1}_fAbs",
                gapabs,
            )
        for idx, name in enumerate(input.layer_names):
            self.set_layer(
                idx + 1,
                name,
                getattr(GlazingLayerType, input.product_types[idx]),
                input.layer_emissivity_front[idx],
                input.layer_emissivity_back[idx],
                input.layer_conductivity[idx],
                input.layer_ir_transmittance[idx],
                input.layer_thickness[idx],
            )

    def set_gap(
        self,
        layer_index: int,
        name: str,
        gas_type: epm.GasType,
        thickness: float,
    ) -> "ConstructionComplexFenestrationStateBuilder":
        """Set gap layer.

        Args:
            layer_index: index of layer
            name: name of gap
            gas_type: gas type
            thickness: thickness of gap

        Returns:
            ConstructionComplexFenestrationStateBuilder

        Raises:
            ValueError: If layer index is not between 1 and 4.
        """
        if layer_index < 1 or layer_index > 4:
            raise ValueError("Layer index must be between 1 and 4.")
        self.energyplus_model.add(
            "window_material_gas",
            gas_type,
            epm.WindowMaterialGas(
                gas_type=gas_type,
                thickness=thickness,
            ),
        )
        self.energyplus_model.add(
            "window_material_gap",
            name,
            epm.WindowMaterialGap(
                gas_or_gas_mixture_=str(gas_type),
                thickness=thickness,
            ),
        )
        self.attributes[f"gap_{layer_index}_name"] = name
        return self

    def set_basis_type(self, basis_type: epm.BasisType):
        self.attributes["basis_type"] = basis_type
        return self

    def set_basis_symmetry_type(self, basis_symmetry_type: epm.BasisSymmetryType):
        self.attributes["basis_symmetry_type"] = basis_symmetry_type
        return self

    def set_window_thermal_model(self, name: str):
        """Fixed thermal model settings for CFS."""
        self.energyplus_model.add(
            "window_thermal_model_params",
            name,
            epm.WindowThermalModelParams(
                standard=epm.Standard.iso15099,
                thermal_model=epm.ThermalModel.iso15099,
                sdscalar=1.0,
                deflection_model=epm.DeflectionModel.no_deflection,
            ),
        )
        self.attributes["window_thermal_model"] = name
        return self

    def set_basis_matrix_name(self, name: str):
        self.energyplus_model.add(
            "matrix_two_dimension",
            name,
            get_matrix_two_dimension(
                [
                    [0.0, 1.0],
                    [10.0, 8.0],
                    [20.0, 16.0],
                    [30.0, 20.0],
                    [40.0, 24.0],
                    [50.0, 24.0],
                    [60.0, 24.0],
                    [70.0, 16.0],
                    [82.5, 12.0],
                ]
            ),
        )
        self.attributes["basis_matrix_name"] = name
        return self

    def set_optical_complex_matrix_name(
        self,
        spectrum: Spectrum,
        direction: Direction,
        radiative_type: RadiativeType,
        name: str,
        matrix_data: List[List[float]],
    ) -> "ConstructionComplexFenestrationStateBuilder":
        self.energyplus_model.add(
            "matrix_two_dimension",
            name,
            get_matrix_two_dimension(matrix_data),
        )
        attribute_key = f"{spectrum.value}_optical_complex_{direction.value}_{radiative_type.value}_matrix_name"
        self.attributes[attribute_key] = name
        return self

    def set_layer(
        self,
        layer_index: int,
        name: str,
        product_type: GlazingLayerType,
        emissivity_front: float,
        emissivity_back: float,
        ir_transmittance: float,
        conductivity: float,
        thickness: float,
    ) -> "ConstructionComplexFenestrationStateBuilder":
        """Set layer.

        Args:
            layer_index: index of layer
            name: name of layer
            product_type: product type
            emissivity_front: front side emissivity
            emissivity_back: back side emissivity
            ir_transmittance: infrared transmittance
            conductivity: conductivity
            thickness: thickness

        Returns:
            ConstructionComplexFenestrationStateBuilder

        Raises:
            ValueError: If layer index is not between 1 and 5.
        """
        if layer_index < 1 or layer_index > 5:
            raise ValueError("Layer index must be between 1 and 5.")

        if product_type == GlazingLayerType.glazing:
            self.energyplus_model.add(
                "window_material_glazing",
                name,
                epm.WindowMaterialGlazing(
                    back_side_infrared_hemispherical_emissivity=emissivity_back,
                    conductivity=conductivity,
                    front_side_infrared_hemispherical_emissivity=emissivity_front,
                    infrared_transmittance_at_normal_incidence=ir_transmittance,
                    optical_data_type=epm.OpticalDataType.bsdf,
                    poisson_s_ratio=0.22,
                    thickness=thickness,
                    window_glass_spectral_data_set_name="",
                ),
            )
        # Assuming shading if not glazing
        else:
            self.energyplus_model.add(
                "window_material_complex_shade",
                name,
                epm.WindowMaterialComplexShade(
                    back_emissivity=emissivity_back,
                    top_opening_multiplier=0,
                    bottom_opening_multiplier=0,
                    left_side_opening_multiplier=0,
                    right_side_opening_multiplier=0,
                    front_opening_multiplier=0.05,
                    conductivity=conductivity,
                    front_emissivity=emissivity_front,
                    ir_transmittance=ir_transmittance,
                    layer_type=epm.LayerType.bsdf,
                    thickness=thickness,
                ),
            )
        layer_key = (
            f"layer_{layer_index}_name" if layer_index > 1 else "outside_layer_name"
        )
        self.attributes[layer_key] = name
        return self

    def set_layer_directional_absorptance_matrix_name(
        self,
        layer_index: int,
        direction: Direction,
        name: str,
        layer_absorptance: List[float],
    ) -> "ConstructionComplexFenestrationStateBuilder":
        """Set layer directional absorptance matrix name.

        Args:
            layer_index: index of layer
            direction: direction of optical properties
            name: name of matrix
            layer_absorptance: layer absorptance matrix

        Returns:
            ConstructionComplexFenestrationStateBuilder

        Raises:
            ValueError: If layer index is not between 1 and 5.

        """
        if layer_index < 1 or layer_index > 5:
            raise ValueError("Layer index must be between 1 and 5.")

        self.energyplus_model.add(
            "matrix_two_dimension",
            name,
            get_matrix_two_dimension_single_row(layer_absorptance),
        )
        if layer_index == 1:
            attribute_key = (
                f"outside_layer_directional_{direction.value}_absoptance_matrix_name"
            )
        else:
            attribute_key = f"layer_{layer_index}_directional_{direction.value}_absoptance_matrix_name"
        self.attributes[attribute_key] = name
        return self

    def set_cfs_gap_directional_absorptance_matrix_name(
        self,
        layer_index: int,
        direction: Direction,
        name: str,
        layer_absorptance: List[float],
    ):
        if layer_index < 1 or layer_index > 4:
            raise ValueError("Layer index must be between 1 and 4.")

        self.energyplus_model.add(
            "matrix_two_dimension",
            name,
            get_matrix_two_dimension_single_row(layer_absorptance),
        )
        attribute_key = f"cfs_gap_{layer_index}_directional_{direction.value}_absoptance_matrix_name"
        self.attributes[attribute_key] = name
        return self


class EnergyPlusModel(epm.EnergyPlusModel):
    def add(self, objkey, objname, obj):
        """Add object to EnergyPlusModel.
        This method assume the object is a dictionary in
        EnergyPlusModel.

        Args:
            objkey: key of object in EnergyPlusModel
            objname: name of the object
            obj: object to add
        """
        if getattr(self, objkey) is None:
            setattr(self, objkey, {objname: obj})
        else:
            getattr(self, objkey)[objname] = obj

    def add_construction_complex_fenestration_state(
        self,
        name: str,
        input: ConstructionComplexFenestrationStateInput,
    ) -> None:
        """Add glazing system to EnergyPlusModel's epjs dictionary.

        Args:
            name: name of glazing system
            input: input parameters for glazing system
        """
        if self.fenestration_surface_detailed is None:
            raise ValueError("No fenestration_surface_detailed found in this model")

        builder = ConstructionComplexFenestrationStateBuilder(name, self, input)
        builder.add_to_enenrgyplus_model()

        if self.construction_complex_fenestration_state is None:
            raise ValueError("No construction_complex_fenestration_state")

        # Set the all fenestration surface constructions to the 1st cfs
        first_cfs = next(iter(self.construction_complex_fenestration_state.keys()))
        for window in self.fenestration_surface_detailed.values():
            window.construction_name = first_cfs
