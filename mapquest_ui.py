import PySimpleGUI as sg
import urllib.parse
import requests
import datetime

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "rT6wCu7ekTjG9wRb42Cg4NBJ1SkuF8hs"
sg.theme("DarkAmber")

x = datetime.datetime.now()

layout = [

    [sg.Text(x.strftime("%X"))],
    [sg.Text(x.strftime("%A, %B %d"))],
    [sg.Text('Find out how to get to your destination!')],
    [sg.Text('Your location:', size =(15, 1)), sg.InputText()],
    [sg.Text('Where to?', size =(15, 1)), sg.InputText()],
    [sg.Submit("Go"), sg.Cancel()]

]

window = sg.Window('Get Directions', layout)

while True: 
    event, values = window.read()
    url = main_api + urllib.parse.urlencode({"key":key, "from":values[0], "to":values[1]})
    window.close()

    json_data = requests.get(url).json()

    json_status = json_data["info"]["statuscode"]


    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")
        "URL: " + (url),
        "Directions from: " + values[0] + " to " + values[1],
        "Trip Duration: " + (json_data["route"]["formattedTime"]),
        "Kilometers: " + str("{:.2f}".format((json_data["route"]["distance"])*1.61)),
        "Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)),
        directions = " "
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            print ((each["narrative"]) + " (" + str ("{:.2f}".format ((each["distance"])*1.61) + " km) "))
            route = (each["narrative"]) + " (" + str ("{:.2f}".format ((each["distance"])*1.61) + " km) ")
            directions = (directions + "\n" + route)

        sg.popup_scrolled (
        
      
            
        'Directions from ' + values[0] + ' to ' + values[1],
        "Trip Duration: " + (json_data["route"]["formattedTime"]),
        "Kilometer: " + str ("{:.2f}".format((json_data["route"]["distance"])*1.61)),
        "Fuel Used (Ltr): " + str ("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)),
        directions,
        size = (70,15),
        title = "Travel Information"
        )
        

            

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

    else:
            print("For Staus Code: " + str(json_status) + "; Refer to:")
            print("https://developer.mapquest.com/documentation/directions-api/status-codes")
            
            sg.popup(

                "Staus Code: " + str(json_status),
                "Refer to: https://developer.mapquest.com/documentation/directions-api/status-codes",
                title = "Something went wrong"

                )
