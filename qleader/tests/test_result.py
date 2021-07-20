from rest_framework.test import APITransactionTestCase
from qleader.tests.data_handler import post_data, scipy_examples, gradient_examples
from qleader.models.result import Result


class ResultsTests(APITransactionTestCase):

    def get_optimizer_tester(self, items):
        for key, value in items:
            response = post_data(self, value)
            result_id = response.data
            result = Result.objects.filter(id=result_id)[0]
            self.assertTrue(key == result.get_optimizer())

    def test_get_optimizer(self):
        self.get_optimizer_tester(scipy_examples.items())
        self.get_optimizer_tester(gradient_examples.items())

    def get_runs_tester(self, items):
        for key, value in items:
            response = post_data(self, value)
            result_id = response.data
            result = Result.objects.filter(id=result_id)[0]
            self.assertTrue(15 == len(result.get_runs()))
            for run in result.get_runs():
                self.assertEqual(result_id, run.result.id)
                self.assertTrue(key == result.optimizer)

    def test_get_runs(self):
        self.get_runs_tester(scipy_examples.items())
        self.get_runs_tester(gradient_examples.items())
