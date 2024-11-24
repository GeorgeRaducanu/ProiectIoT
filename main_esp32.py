import dht
import machine
import time

DHT_PIN = 4  # Pinul pentru senzor

dht_sensor = dht.DHT11(machine.Pin(DHT_PIN))

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

