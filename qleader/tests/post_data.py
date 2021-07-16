import os
import sys
import ast
import json


def create_test_data_from_example(path):
    data = ast.literal_eval(
        open(os.path.join(sys.path[0], path), "r").read()
    )
    return json.dumps(data)


nelder_mead = create_test_data_from_example("example_NELDER_MEAD.txt")
bfgs = create_test_data_from_example("example_BFGS.txt")
nesterov = create_test_data_from_example("example_NESTEROV.txt")


def post_data(self, data):
    response = self.client.post("/api/", data=data, format='json')
    return response
