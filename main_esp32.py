import dht
import machine
import time
import network
import urequests
import socket
import json
DHT_PIN = 32  # Pinul pentru senzor

dht_sensor = dht.DHT11(machine.Pin(DHT_PIN))

ssid = "Georgeeee"
password = "zsaq7163"

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

def connect_to_wifi():
    """
    Attempt to connect to Wi-Fi and debug connection issues using try-except.
    """
    if not sta_if.isconnected():
        print("Attempting to connect to Wi-Fi...")
        try:
            sta_if.connect(ssid, password)  # Attempt connection
            timeout = time.time() + 15  # Timeout after 15 seconds
            while not sta_if.isconnected():
                if time.time() > timeout:
                    print("Wi-Fi connection timeout.")
                    break
                print(".", end="")
                time.sleep(1)

            if sta_if.isconnected():
                print("\nConnected to Wi-Fi!")
                print("Network configuration:", sta_if.ifconfig())
            else:
                print("\nFailed to connect to Wi-Fi after timeout.")
        except Exception as e:
            print(f"\nError during Wi-Fi connection: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)
            connect_to_wifi()  # Retry connection
    else:
        print("Already connected to Wi-Fi!")
        print("Network configuration:", sta_if.ifconfig())

url = "https://192.168.1.5:5001/submit"

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(ssid, password)

while not sta_if.isconnected():
    time.sleep(1)

print("Conectat la retea")

def send_request(temperature, humidity):
    try:
        addr_info = socket.getaddrinfo("192.168.1.5", 5001)[0][-1]
        s = socket.socket()
        s.connect(addr_info)

        ssock = ussl.wrap_socket(s)

        # Create JSON payload
        payload = json.dumps({
            "temperature": temperature,
            "humidity": humidity
        })

        request = f"POST /submit HTTP/1.1\r\nHost: 192.168.1.5\r\nContent-Type: application/json\r\nContent-Length: {len(payload)}\r\n\r\n{payload}"
        ssock.write(request.encode('utf-8'))

        response = ssock.read(1024)
        print("Server Response:", response.decode('utf-8'))

        ssock.close()
    except Exception as e:
        print("Eroare trimitere request:", e)

while True:
    try:
        # Masor folosind biblioteca
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()

        print("Temperatura: {}°C".format(temperature))
        print("Umiditate: {}%".format(humidity))

        send_request(temperature, humidity)
        #sleep(200)
    except Exception as e:
        print("Eroare citire DHT11:", e)

    time.sleep(2)
