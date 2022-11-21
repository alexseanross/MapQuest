import mapquest_ui
import urllib.parse

def test_weather_isLooking_for_correct_location():
    targetLocation = mapquest_ui.values[1]
    weatherURL = mapquest_ui.weather_url
    assert targetLocation in weatherURL;
    print("Correct weather location")


