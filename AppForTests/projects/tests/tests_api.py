import json
import os
from unittest import TestCase
import allure
import django
from django.test import Client
from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AppForTests.settings')
django.setup()


def http_request(method, url=reverse("crypto_projects-list"), data=None, content_type='application/json'):
    client = Client()
    request_method = getattr(client, method.lower())
    if data:
        response = request_method(url, data=json.dumps(data), content_type=content_type)
    else:
        response = request_method(url)
    return response


@allure.tag("api", "get")
class TestsGetCryptoProjects(TestCase):
    @allure.title("Verify non-empty list of crypto projects")
    @allure.description("Send a GET request to the API and verify that the response contains a non-empty list of "
                        "crypto projects")
    def test_get_list_content_with_crypto_projects(self) -> None:
        with allure.step("Send GET request to retrieve the list of projects"):
            response = http_request("GET")
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

    def test_one_project_exists_should_succeed(self):
        response = http_request("GET")
        response_content = json.loads(response.content)[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content.get("id"), 1)
        self.assertEqual(response_content.get("name"), "Bitcoin")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")


@allure.tag("api", "post")
class TestsPostCryptoProjects(TestCase):
    def test_adding_already_created_crypto_project(self):
        data = {
            "id": 7,
            "name": "Sui"}
        response = http_request("POST", data=data)
        self.assertTrue(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"name": ["crypto projects with this name already exists."]})

    def test_adding_new_crypto_project_without_required_field(self):
        data = {"id": 8}
        response = http_request("POST", data=data)
        self.assertTrue(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {"name": ["This field is required."]})