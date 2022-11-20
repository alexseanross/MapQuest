import PySimpleGUI as sg
import urllib.parse
import requests
import json
import datetime


#API Key
openweather_key = "e6e32084500535420729103249e1b405"
mapquest_key = "rT6wCu7ekTjG9wRb42Cg4NBJ1SkuF8hs"
 
#API URL
openwather_api = "http://api.openweathermap.org/data/2.5/weather?"
mapquest_api = "https://www.mapquestapi.com/directions/v2/route?"

sg.theme("BlueMono") #"sg" is the object for the simpoleGUI

x = datetime.datetime.now()

#contains the layout for GUI
layout = [

    [sg.Text(x.strftime("%X"))],
    [sg.Text(x.strftime("%A, %B %d"))],
    [sg.Text('Find out how to get to your destination!')],
    [sg.Text('Your location:', size =(15, 1)), sg.InputText()],#input is automatically assigned to value array
    [sg.Text('Where to?', size =(15, 1)), sg.InputText()],#input is automatically assigned to value array
    [sg.Submit("Go"), sg.Cancel("Cancel")]

]

window = sg.Window('Get Directions', layout)#window is sg calling layout. 'Get Directions' is the name of the window

while True: 
    event, values = window.read() # Call window as event
    url = mapquest_api + urllib.parse.urlencode({"key":mapquest_key, "from":values[0], "to":values[1]})
    weather_url = openwather_api + "appid=" + openweather_key + "&q=" + values[1]
    window.close()

    #MapQuest
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    #OpenWeather
    response = requests.get(weather_url)
    data = json.loads(response.text)

    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")
    
        #Full direction information
        directions = " "
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            route = (each["narrative"]) + " (" + str ("{:.2f}".format ((each["distance"])*1.61) + " km) ")
            directions = (directions + "\n" + route)
        
        sg.popup_scrolled (
        
        'Directions from ' + values[0] + ' to ' + values[1],
        "\n"
        "Trip Duration: " + (json_data["route"]["formattedTime"]),
        "Kilometer: " + str ("{:.2f}".format((json_data["route"]["distance"])*1.61)),
        "\n"
        "The current temperature in " + values[1] + ': ' + str ("{:.2f}".format((data['main']['temp'])-273.15)) + "°C",
        "The current weather status in " + values[1] + ': '+ str (data['weather'][0]['description']),
        directions,
        
        size = (70,15),
        title = "Travel Information"
        )
        
    elif event == "Cancel" or event == None:
     break
            
    elif json_status == 402:
            print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
            
            sg.popup(
                
                "Invalid user inputs for one or both locations.",
                title = "Something went wrong"
                
                )

    elif json_status == 611:
            print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
            
            sg.popup(
                
                "Missing an entry for one or both locations.",
                title = "Something went wrong"
                
                )
    
    elif event == 'Cancel' or event == None:
        break


    else:
            print("For Staus Code: " + str(json_status) + "; Refer to:")
            print("https://developer.mapquest.com/documentation/directions-api/status-codes")
            
            sg.popup(

                "Staus Code: " + str(json_status),
                "Refer to: https://developer.mapquest.com/documentation/directions-api/status-codes",
                title = "Something went wrong"

                )

exit()