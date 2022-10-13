import PySimpleGUI as sg
import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "rT6wCu7ekTjG9wRb42Cg4NBJ1SkuF8hs"

sg.theme("DarkAmber")

layout = [
    [sg.Text('Find out how to get to your destination here!')],
    [sg.Text('Your location:', size =(15, 1)), sg.InputText()],
    [sg.Text('Where to?', size =(15, 1)), sg.InputText()],
    [sg.Submit(), sg.Cancel()]
]

window = sg.Window('Get Directions', layout)
event, values = window.read()
url = main_api + urllib.parse.urlencode({"key":key, "from":values[0], "to":values[1]})
window.close()


json_data = requests.get(url).json()
json_status = json_data["info"]["statuscode"]
if json_status == 0:
     print("API Status: " + str(json_status) + " = A successful route call.\n")

sg.popup(
    
    "URL: " + (url),
    "Directions from: " + values[0] + " to " + values[1],
    "Trip Duration: " + (json_data["route"]["formattedTime"]),
    "Kilometers: " + str("{:.2f}".format((json_data["route"]["distance"])*1.61)),
    "Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)),
    )   
