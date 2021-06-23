from webmark2.settings import INSTALLED_APPS
import pytest
from ..helpers import create_qbatch, create_qresults

f = open('mock_nelder_mead.txt', 'r')
nelder = f.read()

f = open('mock_bfgs', 'r')
bfgs = f.read()


class TestHelpers:
    # Test that mock outputs go through without any raised errors
    def test_nelder_mead_pass():
        create_qbatch(nelder)
        create_qresults(nelder)

    def test_bfgs_pass():
        create_qbatch(bfgs)
        create_qresults(bfgs)
