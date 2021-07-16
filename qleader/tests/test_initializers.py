import os
import sys
import ast
# import pytest

import qleader.initializers as initializers


# example files are outputs generated with the basic VQE example
# here we simply test that the information is extracted correctly.
nelder_mead = ast.literal_eval(
    open(os.path.join(sys.path[0], "example_NELDER_MEAD.txt"), "r").read()
)
bfgs = ast.literal_eval(open(os.path.join(sys.path[0], "example_BFGS.txt"), "r").read())


def test_get_history_returns_dict():
    history_dict = initializers.get_history(nelder_mead, 0)
    assert type(history_dict) is dict


def test_get_history_returns_energies():
    history_dict = initializers.get_history(nelder_mead, 1)
    energy_list = ast.literal_eval(history_dict["energies"])
    assert energy_list[0] == 0.16417501091932965


def test_get_hamiltonian():
    hamiltonian = initializers.get_hamiltonian(nelder_mead, 0)
    assert "+5.0607+0.3008Z(0)+0.3008Z(0)Z(1)-0.7265Z(2)" in hamiltonian


def test_scipy_results_returns_dict():
    scipy_dict = initializers.get_scipy_results(nelder_mead, 0)
    assert type(scipy_dict) is dict


def test_scipy_results_for_nelder_mead():
    scipy_dict = initializers.get_scipy_results(nelder_mead, 0)
    fields = [
        "final_simplex",
        "fun",
        "message",
        "nfev",
        "nit",
        "status",
        "success",
        "x",
    ]
    for field in fields:
        assert field in scipy_dict.keys()


def test_scipy_results_for_bfgs():
    scipy_dict = initializers.get_scipy_results(bfgs, 0)
    fields = [
        "fun",
        "hess_inv",
        "jac",
        "message",
        "nfev",
        "nit",
        "njev",
        "status",
        "success",
        "x",
    ]
    for field in fields:
        assert field in scipy_dict.keys()
