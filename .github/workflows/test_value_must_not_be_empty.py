import mapquest_ui

def test_notEmpty():
    testing = len(mapquest_ui.values)
    assert testing != 0

def test_location_1_array():
    assert "valenzuela" in mapquest_ui.values

