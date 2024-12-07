import dht
import machine
import time
import network
import urequests
import ussl
DHT_PIN = 4  # Pinul pentru senzor

dht_sensor = dht.DHT11(machine.Pin(DHT_PIN))

ssid = "Numele retelei"
password = "Parola retelei"
url = "https://192.168.1.5:5001/"

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(ssid, password)


while True:
    try:
        # Masor folosind biblioteca
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()

        print("Temperatura: {}°C".format(temperature))
        print("Umiditate: {}%".format(humidity))
    except Exception as e:
        print("Eroare citire DHT11:", e)

    time.sleep(2)

