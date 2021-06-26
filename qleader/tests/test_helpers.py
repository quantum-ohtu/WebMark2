# import ast
from qleader.helpers import create_qbatch

# from qleader.models import QBatch, QResult
import pytest


def test_totalDummy():
    assert 2 == 2


class TestClass:
    def test_errorOnInvalidInput(self):
        with pytest.raises(TypeError):
            create_qbatch("nothing important")
