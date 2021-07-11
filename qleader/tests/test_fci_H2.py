import os
import sys
import ast
import pytest

import qleader.fci.fci_H2 as fci
from qleader.fci.fci_basis_sets_H2 import sto_3g


def test_get_fci_basis_set_sto_3g():
    # Test that get_fci returns sto_3g tuple when argument is "sto_3g"
    assert fci.get_fci("sto-3g") == [tuple(item) for item in sto_3g.items()]