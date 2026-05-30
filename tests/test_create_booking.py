import allure
from core.clients.api_client import APIClient


@allure.feature("Booking")
@allure.story("Create booking")
def test_create_booking(api_client: APIClient,
                        generate_random_booking_data: dict):
    with allure.step("Sent request to create a booking"):
        response = api_client.create_booking(data := generate_random_booking_data)
    with allure.step("Verify booking ID and booking data in the response"):
        booking = response['booking']
        assert response['bookingid'] > 0, f"Expected bokingid > 0, got {response['bookingid']}"
        assert booking['firstname'] == data['firstname'], (f"Expected firstname == {data['firstname']},"
                                                           f" got {booking['firstname']}")
        assert booking['lastname'] == data['lastname'],  (f"Expected lastname == {data['lastname']},"
                                                          f" got {booking['lastname']}")
        assert booking['totalprice'] == data['totalprice'], (f"Expected totalprice == {data['totalprice']},"
                                                             f" got {booking['totalprice']}")
        assert booking['depositpaid'] == data['depositpaid'], (f"Expected depositpaid == {data['depositpaid']},"
                                                               f" got {booking['depositpaid']}")
        assert booking['additionalneeds'] == data['additionalneeds'], (f"Expected additionalneeds == {data['additionalneeds']},"
                                                                       f" got {booking['additionalneeds']}")
        assert booking['bookingdates']['checkin'] == data['bookingdates']['checkin'], (f"Expected checkin == {data['bookingdates']['checkin']},"
                                                                                       f" got {booking['bookingdates']['checkin']}")
        assert booking['bookingdates']['checkout'] == data['bookingdates']['checkout'], (f"Expected checkout == {data['bookingdates']['checkout']},"
                                                                                         f" got {booking['bookingdates']['checkout']}")
