import json
from rest_framework import status
from rest_framework.test import APITransactionTestCase
from qleader.tests.post_data import post_data, create_test_data_from_example

# Scipy examples
nelder_mead = create_test_data_from_example("./test_data/example_NELDER-MEAD.txt")
bfgs = create_test_data_from_example("./test_data/example_BFGS.txt")
l_bfgs_b = create_test_data_from_example("./test_data/example_L-BFGS-B.txt")
cobyla = create_test_data_from_example("./test_data/example_COBYLA.txt")

# Gradient examples
nesterov = create_test_data_from_example("./test_data/example_NESTEROV.txt")
