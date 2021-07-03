import os
import sys
import ast

import qleader.helpers as helpers


# example files are outputs generated with the basic VQE example
# here we simply test that the information is extracted correctly.
nelder_mead = ast.literal_eval(
    open(os.path.join(sys.path[0], "example_nelder_mead.txt"), "r").read()
    )
bfgs = ast.literal_eval(open(os.path.join(sys.path[0], "example_BFGS.txt"), "r").read())


def test_get_history_returns_dict():
    history_dict = helpers.get_history(nelder_mead, 0)
    assert type(history_dict) is dict


def test_get_history_returns_energies():
    history_dict = helpers.get_history(nelder_mead, 1)
    energy_list = ast.literal_eval(history_dict['energies'])
    assert energy_list[0] == -1.0661086491853138


def test_get_hamiltonian():
    hamiltonian = helpers.get_hamiltonian(nelder_mead, 0)
    assert "+0.3798+0.2139Z(0)+0.2139Z(1)-0.3691Z(2)-0.3691Z(3)" in hamiltonian


def test_scipy_results_returns_dict():
    scipy_dict = helpers.get_scipy_results(nelder_mead, 0)
    assert type(scipy_dict) is dict


def test_scipy_results_for_nelder_mead():
    scipy_dict = helpers.get_scipy_results(nelder_mead, 0)
    fields = ['final_simplex', 'fun', 'message', 'nfev', 'nit', 'status', 'success', 'x']
    for field in fields:
        assert field in scipy_dict.keys()


def test_scipy_results_for_bfgs():
    scipy_dict = helpers.get_scipy_results(bfgs, 0)
    fields = ['fun', 'hess_inv', 'jac', 'message', 'nfev', 'nit', 'njev', 'status', 'success', 'x']
    for field in fields:
        assert field in scipy_dict.keys()


def test_qbatch_creation_nelder_mead():
    result = helpers.create_result(nelder_mead)
    assert result is "NoErr"

def test_qbatch_creation_bfgs():
    result = helpers.create_result(bfgs)
    assert result is "NoErr"

