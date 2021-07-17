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
