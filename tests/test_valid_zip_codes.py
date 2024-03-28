import pytest
import requests
from utils import API_PATH


@pytest.mark.valid_zip
def test_valid_zip_code_case_insensitivity():

    response_1 = requests.get(API_PATH + "us/90210")
    assert response_1.status_code == 200

    response_2 = requests.get(API_PATH + "US/90210")
    assert response_2.status_code == 200

    response_3 = requests.get(API_PATH + "uS/90210")
    assert response_3.status_code == 200

    expected_output = {
        "post code": "90210",
        "country": "United States",
        "country abbreviation": "US",
        "places": [
            {
                "place name": "Beverly Hills",
                "longitude": "-118.4065",
                "state": "California",
                "state abbreviation": "CA",
                "latitude": "34.0901"
            }
        ]
    }

    assert response_1.json() == response_2.json() == response_3.json() == expected_output


@pytest.mark.valid_zip
def test_valid_zip_code_with_characters():
    response = requests.get(API_PATH + "BR/01000-000")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["post code"] == "01000-000"
    assert response_data["country"] == "Brazil"
    assert response_data["places"][0]["place name"] == "São Paulo"

    # test with space the zip code is not found
    response = requests.get(API_PATH + "BR/%2001000-000")
    assert response.status_code == 404

    response = requests.get(API_PATH + "LK/%20*")
    assert response.status_code == 200

    # Test without space before
    response = requests.get(API_PATH + "LK/*")
    assert response.status_code == 404

    response = requests.get(API_PATH + "CZ/798%2062")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["country"] == "Czech Republic"

@pytest.mark.valid_zip
def test_multiple_places_same_zip():
    response = requests.get(API_PATH + "CZ/100%2000")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["country"] == "Czech Republic"
    assert len(response_data["places"]) == 10

    expected_places = ["Praha 10-Strašnice", "Praha 10-Vršovice", "Praha 10-Vinohrady", "Strašnice",
        "Malešice", "Vršovice", "Vinohrady", "Žižkov", "Praha 10-Žižkov", "Praha 10-Malešice"
    ]
    assert sorted([place["place name"].split(" (")[0] for place in response_data["places"]]) == sorted(expected_places)

@pytest.mark.valid_zip
def test_api_params():
    response = requests.get(
        API_PATH + "BR/01000-000",
        params={"param1": "testparam"}
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["post code"] == "01000-000"
    assert response_data["country"] == "Brazil"
    assert response_data["places"][0]["place name"] == "São Paulo"
