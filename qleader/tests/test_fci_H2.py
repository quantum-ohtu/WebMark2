import os
import sys
import ast
import pytest

import qleader.fci.fci_H2 as fci
from qleader.fci.fci_basis_sets_H2 import sto_3g, six_31g, def2_QZVPPD


def test_get_fci_basis_set_sto_3g():
    # Test that get_fci returns sto_3g tuple when argument is "sto_3g"
    assert fci.get_fci("sto-3g") == [tuple(item) for item in sto_3g.items()]

def test_get_fci_basis_set_six_31g():
    # Test that get_fci returns six_31g tuple when argument is "6-31g"
    assert fci.get_fci("6-31g") == [tuple(item) for item in six_31g.items()]

def test_get_fci_basis_set_def2_QZVPPD():
    # Test that get_fci returns def2_QZVPPD tuple when argument is "def2-QZVPPD"
    assert fci.get_fci("def2-QZVPPD") == [tuple(item) for item in def2_QZVPPD.items()]

def test_get_fci_rises_value_error_if_unknown_basis_set():
    # Test that if the given basis set is unknown then get_fci rises ValueError.
    with pytest.raises(ValueError):
        fci.get_fci("abc-123")
