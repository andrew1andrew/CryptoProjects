import json
import os
from unittest import TestCase
import allure
import django
from django.test import Client
from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AppForTests.settings')
django.setup()


@allure.tag("api", "positive")
class TestsGetCryptoProjects(TestCase):
    @allure.title("Verify non-empty list of crypto projects")
    @allure.description("Send a GET request to the API and verify that the response contains a non-empty list of "
                        "crypto projects")
    def test_get_list_content_with_crypto_projects(self) -> None:
        client = Client()
        crypto_projects_url = reverse("crypto_projects-list")
        with allure.step("Send GET request to retrieve the list of projects"):
            response = client.get(crypto_projects_url)
        with allure.step("Verify that the response status code is 200"):
            self.assertEqual(response.status_code, 200), f"Error. Response status code is {response.status_code}"
        with allure.step("Check that the list of projects is not empty"):
            content = json.loads(response.content)
            self.assertTrue(len(content) > 0), f"Error. The list of projects is empty"

    @allure.title("Verify non-empty list for each crypto projects")
    @allure.description("Send a GET request to the API and verify that the response contains a non-empty list for each "
                        "crypto projects")
    def test_get_list_for_each_project(self):
        client = Client()
        crypto_projects_url = reverse("crypto_projects-list")
        expected_names = {
            1: "Bitcoin",
            2: "Ethereum",
            3: "Tether",
            4: "BNB",
            5: "Solana",
            6: "XRP"
        }
        for project_id, expected_name in expected_names.items():
            with self.subTest(project_id=project_id):
                with allure.step(f"Send GET request to fetch details of project with ID {project_id}"):
                    response = client.get(f"{crypto_projects_url}{project_id}/", follow=True)
                with allure.step("Verify that the response status code is 200"):
                    self.assertEqual(response.status_code, 200), f"Error. Response status code is {response.status_code}"
                json_response = json.loads(response.content)
                with allure.step(f"Verify project ID in the response matches the requested project ID {project_id}"):
                    self.assertEqual(json_response["id"], project_id)
                with allure.step(f"Verify project name {expected_name} for project ID {project_id}"):
                    self.assertEqual(json_response["name"], expected_name)

