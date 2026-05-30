def assert_booking_data(actual_booking: dict, expected_booking: dict):
    assert actual_booking['firstname'] == expected_booking['firstname'], (f"Expected firstname == {expected_booking['firstname']},"
                                                       f" got {actual_booking['firstname']}")
    assert actual_booking['lastname'] == expected_booking['lastname'], (f"Expected lastname == {expected_booking['lastname']},"
                                                     f" got {actual_booking['lastname']}")
    assert actual_booking['totalprice'] == expected_booking['totalprice'], (f"Expected totalprice == {expected_booking['totalprice']},"
                                                         f" got {actual_booking['totalprice']}")
    assert actual_booking['depositpaid'] == expected_booking['depositpaid'], (f"Expected depositpaid == {expected_booking['depositpaid']},"
                                                           f" got {actual_booking['depositpaid']}")
    assert actual_booking['additionalneeds'] == expected_booking['additionalneeds'], (
        f"Expected additionalneeds == {expected_booking['additionalneeds']},"
        f" got {actual_booking['additionalneeds']}")
    assert actual_booking['bookingdates']['checkin'] == expected_booking['bookingdates']['checkin'], (
        f"Expected checkin == {expected_booking['bookingdates']['checkin']},"
        f" got {actual_booking['bookingdates']['checkin']}")
    assert actual_booking['bookingdates']['checkout'] == expected_booking['bookingdates']['checkout'], (
        f"Expected checkout == {expected_booking['bookingdates']['checkout']},"
        f" got {actual_booking['bookingdates']['checkout']}")

