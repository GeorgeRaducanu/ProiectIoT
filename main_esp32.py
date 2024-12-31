import dht
import machine
import time
import network
import urequests
import socket
import json
import ssl
import requests


bot_token = '7561752951:AAHvTCV2qX3gRv2CjbAKFQkqLKxZqEsfids'
chat_id = '5387449451'

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

connect_to_wifi()

print("Conectat la retea")

def send_request_seq(temperature, humidity):
    try:
        # Load the CA certificate
        with open("cert.pem", "rb") as f:
            cert = f.read()

        # Create a socket and wrap it with SSL
        addr_info = socket.getaddrinfo("192.168.28.191", 5001)[0][-1]
        s = socket.socket()
        s.connect(addr_info)
        s = ssl.wrap_socket(s)

        # Create JSON payload
        payload = json.dumps({
            "temperature": temperature,
            "humidity": humidity
        })

        # Build HTTP POST request
        request = (
            f"POST /submit HTTP/1.1\r\n"
            f"Host: 192.168.28.191\r\n"
            f"Content-Type: application/json\r\n"
            f"Content-Length: {len(payload)}\r\n"
            f"\r\n"
            f"{payload}"
        )

        # Send the HTTP request
        s.write(request.encode('utf-8'))

        # Read the HTTP response
        response = s.read(1024)
        print("Server Response:", response.decode('utf-8'))

        s.close()
    except Exception as e:
        print("Error sending request:", e)

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    try:
        response = requests.post(url, json=payload)
        response.close()
        print("Message sent successfully!")
    except Exception as e:
        print(f"Error sending message: {e}")
while True:
    dht_sensor.measure()
    temperature = dht_sensor.temperature()
    if temperature >= 20.0:
        send_telegram_message("E mai cald de 20")
    humidity = dht_sensor.humidity()
    print("Temperatura: {}°C".format(temperature))
    print("Umiditate: {}%".format(humidity))
    send_request_seq(temperature, humidity)
    time.sleep(4)
