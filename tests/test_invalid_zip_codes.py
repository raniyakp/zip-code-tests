import pytest
import requests
from utils import API_PATH


@pytest.mark.invalid_zip
def test_invalid_zip_codes():

    # Valid country and invalid zip code
    response = requests.get(API_PATH + "us/1111111")
    assert response.status_code == 404

    # Invalid country and valid zip code
    response = requests.get(API_PATH + "abc/90211")
    assert response.status_code == 404

    # Without zip code
    response = requests.get(API_PATH + "us/")
    assert response.status_code == 404

    response = requests.get(API_PATH + "us/%20")
    assert response.status_code == 404

@pytest.mark.invalid_zip
def test_empty_country_zipcode():

    response = requests.get(API_PATH + "/%20")
    assert response.status_code == 404

    response = requests.get(API_PATH + "%20/")
    assert response.status_code == 404

    response = requests.get(API_PATH + "*/")
    assert response.status_code == 404
