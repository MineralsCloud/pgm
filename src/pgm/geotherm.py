import numpy as np
from qha.type_aliases import Matrix, Vector
from qha.unit_conversion import Avogadro, ry_b3_to_gpa, gpa_to_ry_b3

def geotherm(alpha_tp: Matrix, cp_tp: Matrix, v_tp: Matrix, ts: Vector) -> Matrix:
    """
    Equation used : \partial T/\partial P)_S = \frac{\alpha * T * V}{C_p}
    :param alpha_tp: 
    :param cp_tp: 
    :param v_tp:  
    :param ts:
    :return: \partial T / \partial P)s in unit of K/GPa
    """
    geotherm = alpha_tp * v_tp / cp_tp 
    geotherm = geotherm.T * ts
    return gpa_to_ry_b3(geotherm.T)