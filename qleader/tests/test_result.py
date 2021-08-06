from rest_framework.test import APITransactionTestCase
from qleader.tests.data_handler import post_data, examples
from qleader.models.result import Result
from rest_framework.test import force_authenticate, APIRequestFactory
from django.contrib.auth.models import User
from django.views.generic import TemplateView


# The test class for Result's custom methods
class ResultsTests(APITransactionTestCase):

    def test_get_optimizer(self):



        for optimizer, data in examples:
            response = post_data(self, data)
            result_id = response.data
            result = Result.objects.filter(id=result_id)[0]
            self.assertTrue(optimizer == result.get_optimizer())

    def test_get_runs(self):
        for optimizer, data in examples:
            response = post_data(self, data)
            result_id = response.data
            result = Result.objects.filter(id=result_id)[0]
            self.assertTrue(15 == len(result.get_runs()))
            for run in result.get_runs():
                self.assertEqual(result_id, run.result.id)
                self.assertTrue(optimizer == result.optimizer)
