import json
from rest_framework import status
from rest_framework.test import APITransactionTestCase
from qleader.tests.data_handler import post_data, scipy_examples, gradient_examples, special_examples
from rest_framework.test import force_authenticate, APIRequestFactory
from django.contrib.auth.models import User
from qleader import views


# The test class for views.py.
class ViewsTests(APITransactionTestCase):

    def setup_method(self, method):
        self.factory = APIRequestFactory()
        self.user, self.created = User.objects.get_or_create(username='Testi-Teppo')

    def test_result_list_GET(self):
        request = self.factory.get("/api/")
        force_authenticate(request, user=self.user)
        view = views.result_receiver
        response = view(request)
        print("RESPONSE: ", response)
        # response = self.client.get("/api/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_result_list_POST_valid_call(self):
        response = post_data(self, scipy_examples["NELDER-MEAD"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_result_list_POST_invalid_call(self):
        response = post_data(self, json.dumps([]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_home_GET(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["results"]) == 0)
        post_data(self, scipy_examples["NELDER-MEAD"])

        request = self.factory.get("")
        force_authenticate(request, user=self.user)
        view = views.home
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["results"]) == 1)
        self.assertEqual(response.data["results"][0]["optimizer"], "NELDER-MEAD")

    def test_detail_GET(self):
        response = post_data(self, scipy_examples["NELDER-MEAD"])
        request = self.factory.get("/api/" + str(response.data) + "/")
        force_authenticate(request, user=self.user)
        view = views.detail
        response = view(request, result_id=response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_leaderboard_GET(self):
        response = self.client.get("/leaderboard/")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_invoke_leaderboard_closest_minimum(self):
        post_data(self, scipy_examples["NELDER-MEAD"])
        post_data(self, scipy_examples["BFGS"])
        post_data(self, gradient_examples["NESTEROV"])
        response = self.client.get("/leaderboard/closest_minimum/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["results"]) == 3)
        self.assertEqual(response.data["criterion"], "closest_minimum")
        self.assertEqual(response.data["results"][0].get_optimizer(), "NELDER-MEAD")
        self.assertEqual(response.data["results"][1].get_optimizer(), "BFGS")
        self.assertEqual(response.data["results"][2].get_optimizer(), "NESTEROV")

    def test_invoke_leaderboard_smallest_variance(self):
        post_data(self, scipy_examples["NELDER-MEAD"])
        post_data(self, special_examples["BENCHMARK_NELDER-MEAD"])
        response = self.client.get("/leaderboard/smallest_variance/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["results"]) == 1)
        self.assertEqual(response.data["criterion"], "smallest_variance")
        self.assertEqual(response.data["results"][0].get_optimizer(), "NELDER-MEAD")

    def test_invoke_leaderboard_min_energy(self):
        post_data(self, scipy_examples["NELDER-MEAD"])
        post_data(self, scipy_examples["BFGS"])
        post_data(self, gradient_examples["NESTEROV"])
        response = self.client.get("/leaderboard/min_energy/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["results"]) == 3)
        self.assertEqual(response.data["criterion"], "min_energy")
        self.assertEqual(response.data["results"][0].get_optimizer(), "NESTEROV")
        self.assertEqual(response.data["results"][1].get_optimizer(), "BFGS")
        self.assertEqual(response.data["results"][2].get_optimizer(), "NELDER-MEAD")

    def test_delete_result_when_authenticated(self):
        response = post_data(self, scipy_examples["NELDER-MEAD"])
        request = self.factory.get("")
        force_authenticate(request, user=self.user)
        view = views.home
        response = view(request)
        self.assertTrue(len(response.data["results"]) == 1)
        request = self.factory.delete("/api/" + str(response.data["results"][0]["id"]) + "/delete/")
        force_authenticate(request, user=self.user)
        view = views.delete_result
        response = view(request, result_id=str(response.data["results"][0]["id"]))
        request = self.factory.get("")
        force_authenticate(request, user=self.user)
        view = views.home
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["results"]) == 0)

    def test_delete_result_unsuccess_when_not_authenticated(self):
        response = post_data(self, scipy_examples["NELDER-MEAD"])
        request = self.factory.get("")
        force_authenticate(request, user=self.user)
        view = views.home
        response = view(request)
        self.assertTrue(len(response.data["results"]) == 1)
        request = self.client.delete("/api/" + str(response.data["results"][0]["id"]) + "/delete/")
        request = self.factory.get("")
        force_authenticate(request, user=self.user)
        view = views.home
        response = view(request)
        self.assertTrue(len(response.data["results"]) == 1)

    def test_delete_result_gives_correct_status_GET(self):
        response = post_data(self, scipy_examples["NELDER-MEAD"])
        request = self.factory.get("")
        force_authenticate(request, user=self.user)
        view = views.home
        response = view(request)
        request = self.factory.get("/api/" + str(response.data["results"][0]["id"]) + "/delete/")
        force_authenticate(request, user=self.user)
        view = views.delete_result
        response = view(request, result_id=str(response.data["results"][0]["id"]))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_result_gives_correct_status_if_not_own(self):
        factory = APIRequestFactory()
        user, created = User.objects.get_or_create(username='Testi-Tapio')
        request = factory.post("/api/", data=json.dumps(scipy_examples["NELDER-MEAD"]), format='json')
        view = views.result_receiver
        force_authenticate(request, user=user)
        response = view(request)
        request = self.factory.get("")
        force_authenticate(request, user=user)
        view = views.home
        response = view(request)
        request = self.factory.delete("/api/" + str(response.data["results"][0]["id"]) + "/delete/")
        force_authenticate(request, user=self.user)
        view = views.delete_result
        response = view(request, result_id=str(response.data["results"][0]["id"]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_result_gives_correct_status_when_result_not_found(self):
        request = self.factory.delete("/api/1/delete/")
        force_authenticate(request, user=self.user)
        view = views.delete_result
        response = view(request, result_id=1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)