print("Xin chào ThingsBoard")
import paho.mqtt.client as mqttclient
import time
import json
from geopy.geocoders import Nominatim
import requests
from bs4 import BeautifulSoup

geolocator = Nominatim(user_agent="my_user_agent")
city ="HCM"
country ="VietNam"

# creating url and requests instance
url = "https://www.google.com/search?q=" + "weather" + city
html = requests.get(url).content

# getting raw data
soup = BeautifulSoup(html, 'html.parser')
temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

# formatting data
data = str.split('\n')
times = data[0]
sky = data[1]

# getting all div tag
listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
strd = listdiv[5].text









BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "3URjDOLQO6iDnl1yTS65"


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {'value': True}
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "setValue":
            temp_data['value'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
    except:
        pass


def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+")
    else:
        print("Connection is failed")


client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message



counter = 0
while True:
    loc = geolocator.geocode(city + ',' + country)
    print("latitude is :-", loc.latitude, "\nlongtitude is:-", loc.longitude)
    collect_data = {'Times': times,'temperature': temp, 'Sky Description': sky,'longitude':loc.longitude,'latitude': loc.latitude }

    client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)
    # printing all data
    print("Temperature is", temp)
    print("Time: ", times)
    print("Sky Description: ", sky)
    time.sleep(5)