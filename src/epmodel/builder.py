"""
Functions: helper function usually to create base level components
Classes: Factory class to create systems
"""
from typing import List

from epmodel import epmodel as epm


def get_matrix_two_dimension_single_row(
    matrix: List[float]
) -> epm.MatrixTwoDimension:
    """Build MatrixTwoDimension object from single row matrix.

    Args:
        matrix: single row matrix

    Returns:
        MatrixTwoDimension object
    """
    return epm.MatrixTwoDimension(
        number_of_columns=len(matrix),
        number_of_rows=1,
        values=[epm.Value(value=val) for val in matrix]
    )

def get_matrix_two_dimension(
    matrix: List[List[float]]
) -> epm.MatrixTwoDimension:
    """Get MatrixTwoDimension object from matrix.

    Args:
        matrix: List of list of float matrix data

    Returns:
        MatrixTwoDimension object
    """
    return epm.MatrixTwoDimension(
        number_of_columns=len(matrix[0]),
        number_of_rows=len(matrix),
        values=[epm.Value(value=val) for row in matrix for val in row]
    )


def get_construction_complex_fenestration_state(
    epmodel: "EnergyPlusModel",
    name: str,
    layer_name: List[str],
    rho_sol_back: List[List[float]],
    tau_sol_back: List[List[float]],
    tau_vis_back: List[List[float]],
    tau_vis_front: List[List[float]],
    alpha_back: List[List[float]],
    alpha_front: List[List[float]],
    gaps,
    layers,
) -> epm.ConstructionComplexFenestrationState:
    basis_matrix_name = f"{name}_Basis"
    rho_sol_back_name = f"{name}_RbSol"
    tau_sol_back_name = f"{name}_TfSol"
    tau_vis_back_name = f"{name}_Tbvis"
    tau_vis_front_name = f"{name}_Tfvis"
    alpha_back_outside_layer_name = f"{name}_layer_1_bAbs"
    alpha_front_outside_layer_name = f"{name}_layer_1_fAbs"

    epmodel.add(
        "matrix_two_dimension",
        basis_matrix_name,
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
        )
    )
    epmodel.add(
        "matrix_two_dimension",
        rho_sol_back_name,
        get_matrix_two_dimension(rho_sol_back)
    )
    epmodel.add(
        "matrix_two_dimension",
        tau_sol_back_name,
        get_matrix_two_dimension(tau_sol_back)
    )
    epmodel.add(
        "matrix_two_dimension",
        tau_vis_back_name,
        get_matrix_two_dimension(tau_vis_back)
    )
    epmodel.add(
        "matrix_two_dimension",
        tau_vis_front_name,
        get_matrix_two_dimension(tau_vis_front)
    )
    epmodel.add(
        "matrix_two_dimension",
        alpha_back_outside_layer_name,
        get_matrix_two_dimension_single_row(alpha_back[0])
    )
    epmodel.add(
        "matrix_two_dimension",
        alpha_front_outside_layer_name,
        get_matrix_two_dimension_single_row(alpha_front[0])
    )

    cfs_layer_name_paris = []
    # Define layer absorptance names and matrices for the rest of the layers.
    for i in range(len(alpha_back) - 1):
        _layer_name = f"{name}_layer_{i+2}"
        _alpha_back_name = f"{_layer_name}_bAbs"
        _alpha_front_name = f"{_layer_name}_fAbs"
        cfs_layer_name_paris.append(
            [
                f"layer_{i+2}_directional_back_absoptance_matrix_name",
                _alpha_back_name,
            ]
        )
        epmodel.add(
            "matrix_two_dimension",
            _alpha_back_name,
            get_matrix_two_dimension_single_row(alpha_back[i + 1])
        )
        cfs_layer_name_paris.append(
            [
                f"layer_{i+2}_directional_front_absoptance_matrix_name",
                _alpha_front_name,
            ]
        )
        epmodel.add(
            "matrix_two_dimension",
            _alpha_front_name,
            get_matrix_two_dimension_single_row(alpha_front[i + 1])
        )
        cfs_layer_name_paris.append(
            [
                f"layer_{i+2}_name",
                layer_name[i + 1],
            ]
        )

    for i, gap in enumerate(gaps, 1):
        _gap_name = f"{name}_gap_{i}"
        cfs_layer_name_paris.append(
            [
                f"gap_{i}_name",
                f"{_gap_name}_layer",
            ]
        )
        _gas_name = f"gas_{i}"
        epmodel.add(
            "window_material_gap",
            f"{_gap_name}_layer",
            epm.WindowMaterialGap(
                gas_or_gas_mixture_=_gas_name,
                thickness=gap[-1],
            )
        )
        # TODO: Add gas mixture
        epmodel.add(
            "window_material_gas",
            "_gas_name",
            epm.WindowMaterialGas(
                gas_type=gap[0][0].name.capitalize(),
                thickness=gap[-1],
            )
        )

    for layer in layers:
        if layer.product_type == "glazing":
            epmodel.add(
                "window_material_glazing",
                layer.product_name,
                epm.WindowMaterialGlazing(
                    back_side_infrared_hemispherical_emissivity=layer.emissivity_back,
                    conductivity=layer.conductivity,
                    front_side_infrared_hemispherical_emissivity=layer.emissivity_front,
                    infrared_transmittance_at_normal_incidence=layer.ir_transmittance,
                    optical_data_type=epm.OpticalDataType.bsdf,
                    poisson_s_ratio=0.22,
                    thickness=layer.thickness,
                    window_glass_spectral_data_set_name="",
                )
            )
        # Assuming complex shade if not glazing
        else:
            epmodel.add(
                "window_material_complex_shade",
                layer.product_name,
                epm.WindowMaterialComplexShade(
                    back_emissivity=layer.emissivity_back,
                    top_opening_multiplier=0,
                    bottom_opening_multiplier=0,
                    left_side_opening_multiplier=0,
                    right_side_opening_multiplier=0,
                    front_opening_multiplier=0.05,
                    conductivity=layer.conductivity,
                    front_emissivity=layer.emissivity_front,
                    ir_transmittance=layer.ir_transmittance,
                    layer_type=epm.LayerType.bsdf,
                    thickness=layer.thickness,
                ),
            )

    epmodel.add(
        "window_thermal_model_params",
        "ThermParam_1",
        epm.WindowThermalModelParams(
            standard=epm.Standard.iso15099,
            thermal_model=epm.ThermalModel.iso15099,
            sdscalar=1.0,
            deflection_model=epm.DeflectionModel.no_deflection,
        )
    )

    ccfs = epm.ConstructionComplexFenestrationState(
        basis_matrix_name=basis_matrix_name,
        basis_symmetry_type=epm.BasisSymmetryType.none,
        basis_type=epm.BasisType.lbnlwindow,
        solar_optical_complex_back_reflectance_matrix_name=rho_sol_back_name,
        solar_optical_complex_front_transmittance_matrix_name=tau_sol_back_name,
        visible_optical_complex_back_transmittance_matrix_name=tau_vis_back_name,
        visible_optical_complex_front_transmittance_matrix_name=tau_vis_front_name,
        window_thermal_model="ThermParam_1",
        outside_layer_directional_back_absoptance_matrix_name=alpha_back_outside_layer_name,
        outside_layer_directional_front_absoptance_matrix_name=alpha_front_outside_layer_name,
        outside_layer_name=layer_name[0],
    )
    for pair in cfs_layer_name_paris:
        setattr(ccfs, *pair)
    return ccfs


class EnergyPlusModel(epm.EnergyPlusModel):

    def add(self, objkey, key, obj):
        """Add object to EnergyPlusModel.

        Args:
            objkey: key of object in EnergyPlusModel
            key: name of the object
            obj: object to add
        """
        if getattr(self, objkey) is None:
            setattr(self, objkey, {key: obj})
        else:
            getattr(self, objkey)[key] = obj

    def add_construction_complex_fenestration_state(
        self,
        layers,
        gaps,
        name: str,
        layer_names: List[str],
        rho_sol_back: List[List[float]],
        tau_sol_back: List[List[float]],
        tau_vis_back: List[List[float]],
        tau_vis_front: List[List[float]],
        alpha_back: List[List[float]],
        alpha_front: List[List[float]],
    ) -> None:
        """Add glazing system to EnergyPlusModel's epjs dictionary.

        Args:
            name: name of glazing system
            rho_sol_back: solar reflectance matrix of back of glazing system
            tau_sol_back: solar transmittance matrix of back of glazing system
            tau_vis_back: visible transmittance matrix of back of glazing system
            tau_vis_front: visible transmittance matrix of front of glazing system
            alpha_back: absorptance matrix of back of each layer
            alpha_front: absorptance matrix of front of each layer

        Raises:
            ValueError: If solar and photopic results are not computed.
            ValueError: If more than 6 layers in glazing system.
        """
        ccfs = get_construction_complex_fenestration_state(
            self,
            name,
            layer_names,
            rho_sol_back,
            tau_sol_back,
            tau_vis_back,
            tau_vis_front,
            alpha_back,
            alpha_front,
            gaps,
            layers
        )

        self.add("construction_complex_fenestration_state", name, ccfs)
        if self.construction_complex_fenestration_state is None:
            raise ValueError("No construction_complex_fenestration_state")

        # Set the all fenestration surface constructions to the 1st cfs
        first_cfs = next(iter(self.construction_complex_fenestration_state.keys()))
        for window in self.fenestration_surface_detailed.values():
            window.construction_name = first_cfs
