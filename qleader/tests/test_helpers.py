import os
import sys
import ast

from qleader.models import QBatch
import qleader.helpers as helpers

import pytest

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
    qbatch = helpers.create_qbatch(nelder_mead)
    assert type(qbatch) is QBatch
    assert qbatch.optimizer == "Nelder-Mead"


def test_qbatch_creation_bfgs():
    qbatch = helpers.create_qbatch(bfgs)
    assert qbatch.optimizer == "BFGS"


def test_qresult_creation_nelder_mead():
    qbatch = helpers.create_qbatch(nelder_mead)
    qresults = helpers.create_qresults(nelder_mead, qbatch)
    assert len(qresults) == 4
    assert qresults[0].batch is qbatch


def test_qresult_creation_bfgs():
    qbatch = helpers.create_qbatch(bfgs)
    qresults = helpers.create_qresults(bfgs, qbatch)
    assert len(qresults) == 4
    assert qresults[1].batch is qbatch


class TestClass:
    def test_errorOnInvalidInput(self):
        with pytest.raises(TypeError):
            helpers.create_qbatch("nothing important")
