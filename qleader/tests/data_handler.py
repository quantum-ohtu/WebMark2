import os
import sys
import ast
import json


def create_test_data_from_example(path):
    return ast.literal_eval(
        open(os.path.join(sys.path[0], path), "r").read()
    )


def post_data(self, data):
    response = self.client.post("/api/", data=json.dumps(data), format='json')
    return response


scipy_examples = {
    "NELDER-MEAD": create_test_data_from_example("tests/test_data/example_NELDER-MEAD.txt"),
    "BFGS": create_test_data_from_example("tests/test_data/example_BFGS.txt"),
    "L-BFGS-B": create_test_data_from_example("tests/test_data/example_L-BFGS-B.txt"),
    "COBYLA": create_test_data_from_example("tests/test_data/example_COBYLA.txt")
}

gradient_examples = {
    "ADAGRAD": create_test_data_from_example("tests/test_data/example_ADAGRAD.txt"),
    "ADAM": create_test_data_from_example("tests/test_data/example_ADAM.txt"),
    "ADAMAX": create_test_data_from_example("tests/test_data/example_ADAMAX.txt"),
    "MOMENTUM": create_test_data_from_example("tests/test_data/example_MOMENTUM.txt"),
    "NADAM": create_test_data_from_example("tests/test_data/example_NADAM.txt"),
    "NESTEROV": create_test_data_from_example("tests/test_data/example_NESTEROV.txt"),
    "RMSPROP-NESTEROV": create_test_data_from_example("tests/test_data/example_RMSPROP-NESTEROV.txt"),
    "RMSPROP": create_test_data_from_example("tests/test_data/example_RMSPROP.txt"),
    "SGD": create_test_data_from_example("tests/test_data/example_SGD.txt"),
    "SPSA": create_test_data_from_example("tests/test_data/example_SPSA.txt")
}
