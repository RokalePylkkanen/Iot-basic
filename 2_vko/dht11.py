# fyysinen pico 2 w kytkettynä joy-it pico protoilulautaan, jossa kiinteä DHT11 anturi pinnissä GP0.
# Käytin kännykän mobiilitukiasemaa yhteyden muodostamisessa ThingSpeakiin, minne syötetään omiin fieldeihin lämpötila ja ilmankosteus.
# Erilliseen secretshit.py tiedostoon tallennettu wifi salasana ja ThingSpeak API avain.


import secretshit     # Erillisessä tiedostossa arkaluontoiset asiat

import network       # For Wi-Fi connectivity

import time          # For delays and timing

import urequests     # For making HTTP requests

import dht           # For interfacing with DHT sensors

from machine import Pin  # For controlling GPIO pins





# Wi-Fi credentials

ssid = secretshit.WIFI_SSID     # SSID of the Wi-Fi network

password = secretshit.WIFI_PASS            # Password (empty for open networks like Wokwi-GUEST)



# ThingSpeak API configuration

THINGSPEAK_API_KEY = secretshit.THING_API_W  # Your ThingSpeak Write API Key

THINGSPEAK_URL = 'https://api.thingspeak.com/update'  # ThingSpeak endpoint



# Set up Wi-Fi in station mode

wlan = network.WLAN(network.STA_IF)  # Create a WLAN object in station mode, the device connects to a Wi-Fi network as a client. 

wlan.active(True)                    # Activate the Wi-Fi interface

wlan.connect(ssid, password)         # Connect to the specified Wi-Fi network



# Wait until connected

print("Connecting to Wi-Fi...", end="")

while not wlan.isconnected():

    print(".", end="")               # Print dots while waiting

    time.sleep(0.5)                  # Wait half a second before retrying



# Once connected, print confirmation and IP address

print("\nConnected!")

print("IP address:", wlan.ifconfig()[0])  # Display the assigned IP address



# Initialize the DHT11 sensor on GPIO pin 15

sensor = dht.DHT11(Pin(0))



# Function to send temperature data to ThingSpeak

def send_to_thingspeak(temp, humidity):

    if temp is None or humidity is None:

        print("No temperature or humidity data to send.")

        return

    try:

        # Send HTTP POST request to ThingSpeak with temperature data

        response = urequests.post(

            THINGSPEAK_URL,

            data='api_key={}&field1={}&field2={}'.format(THINGSPEAK_API_KEY, temp, humidity),

            headers={'Content-Type': 'application/x-www-form-urlencoded'}

        )

        print("ThingSpeak response:", response.text)  # Print server response
        

        response.close()  # Close the connection
        

    except Exception as e:

        print("Failed to send data:", e)  # Handle any errors



# Main loop: read sensor and send data every 15 seconds

while True:

    try:

        sensor.measure()                      # Trigger sensor measurement

        temperature: float = sensor.temperature()    # Read temperature in Celsius

        humidity: float = sensor.humidity()

        print(f"Temperature: {temperature:.1f}C")  # Display temperature
        print(f"Humidity: {humidity:.1f}%")  # Display humidity

        send_to_thingspeak(temperature, humidity)       # Send data to ThingSpeak

    except Exception as e:

        print("Error reading sensor or sending data:", e)  # Handle errors

    

    time.sleep(15)  # Wait 15 seconds before next reading