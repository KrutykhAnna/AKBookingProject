import allure
import pytest
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
                                                    generate_random_booking_data: dict,
                                                     mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"error": "Bad Request"}
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)

    booking_data = generate_random_booking_data.copy()
    del booking_data[required_field]

    with allure.step("Sent request to create a booking"):
        response = api_client.create_booking(booking_data)
    with allure.step("Assert status code"):
        assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
        assert response.json() == {"error": "Bad Request"}, f"Expected error message 'Bad Request', but got {response.json()}"



@allure.feature("Booking")
@allure.story("Create booking")
@allure.title("Verify booking creation fails with empty request body")
def test_create_booking_with_empty_request_body(api_client: APIClient, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"error": "Bad Request"}
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with allure.step("Sent request to create a booking"):
        response = api_client.create_booking({})
    with allure.step("Assert status code"):
        assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
        assert response.json() == {"error": "Bad Request"}, f"Expected error message 'Bad Request', but got {response.json()}"


@allure.feature("Booking")
@allure.story("Create booking")
@allure.title("Verify booking creation fails with invalid_field_type")
@pytest.mark.parametrize("field, invalid_value", [
    ("firstname", 999),
    ("lastnamme", True),
    ("totalprice", "one"),
    ("depositpaid", "yes"),
    ("bookingdates", "invalid_date")
])
def test_create_booking_with_empty_request_body(field, invalid_value,
                                                api_client: APIClient, mocker,
                                                generate_random_booking_data: dict):
    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"error": "Bad Request"}
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    booking_data = generate_random_booking_data.copy()
    booking_data[field] = invalid_value
    with allure.step("Sent request to create a booking"):
        response = api_client.create_booking(booking_data)
    with allure.step("Assert status code"):
        assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
        assert response.json() == {"error": "Bad Request"}, f"Expected error message 'Bad Request', but got {response.json()}"


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









