import allure
import pytest
import requests.exceptions

from tests.assertions.booking_assert import assert_booking_data
from core.clients.api_client import APIClient
from pydantic import ValidationError
from core.models.booking import BookingResponse


@allure.feature("Booking")
@allure.story("Create booking")
@allure.title("Create booking with random data")
def test_create_booking_with_random_data(api_client: APIClient,
                        generate_random_booking_data: dict):
    with allure.step("Sent request to create a booking"):
        response = api_client.create_booking(data := generate_random_booking_data)
    with allure.step("Assert status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        try:
            BookingResponse(**response.json())
        except ValidationError as e:
            raise ValidationError(f"Response validation failed {e}")

    with allure.step("Verify booking ID and booking data in the response"):
        booking = response.json()['booking']
        assert response.json()['bookingid'] > 0, f"Expected bokingid > 0, got {response['bookingid']}"
        assert_booking_data(booking,data)


@allure.feature("Booking")
@allure.story("Create booking")
@allure.title("Verify booking creation fails when required field is missing")
@pytest.mark.parametrize("required_field", [
    "firstname", "lastname", "totalprice"
])
def test_create_booking_with_missing_required_fields(required_field: str,
                                                     api_client: APIClient,
                                                    generate_random_booking_data: dict,):

    booking_data = generate_random_booking_data.copy()
    del booking_data[required_field]
    with allure.step(f"Send request without required field: {required_field}"):
        with pytest.raises(requests.exceptions.HTTPError):
            api_client.create_booking(booking_data)



@allure.feature("Booking")
@allure.story("Create booking")
@allure.title("Verify booking creation fails with empty request body")
def test_create_booking_with_empty_request_body(api_client: APIClient):
    with allure.step("Sent request with empty request body"):
        with pytest.raises(requests.exceptions.HTTPError):
            api_client.create_booking({})


@allure.feature("Booking")
@allure.story("Create booking")
@allure.title("Verify booking creation fails with invalid_field_type")
@pytest.mark.parametrize("field, invalid_value", [
    ("firstname", 999),
    ("bookingdates", "invalid_date")
])
def test_create_booking_with_invalid_field_type(field, invalid_value,
                                                api_client: APIClient,
                                                generate_random_booking_data: dict):
    booking_data = generate_random_booking_data.copy()
    booking_data[field] = invalid_value
    with allure.step(f"Sent request with invalid type field == {field}"):
        with pytest.raises(requests.exceptions.HTTPError):
            api_client.create_booking(booking_data)



@allure.feature("Booking")
@allure.story("Create booking")
@allure.title("Verify create booking can be retrieved by ID")
def test_create_booking_can_be_retrieved_by_id(api_client: APIClient,
                        generate_random_booking_data: dict):
    with allure.step("Sent request to create a booking"):
        response = api_client.create_booking(data := generate_random_booking_data)
    with allure.step("Assert status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    with allure.step(f"Sent request to get booking with id {response.json()["bookingid"]}"):
        response_get = api_client.get_booking_by_id(response.json()["bookingid"])
    with allure.step( f"Check created booking can be found by ID {response.json()["bookingid"]}"):
        assert_booking_data(response_get,data)









