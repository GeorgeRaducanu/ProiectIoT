# Proiect IoT 2024-2025
# Smart home temperature and humidity monitoring
## Răducanu George-Cristian 341C1

## Descrierea proiectului:
Proiectul consta intr-un sistem smart-home, ce masoara temperatura si umiditatea 
din casa. Datele sunt transmise prin intermediul Wi-Fi ului si sunt prelucrate 
datele obtinute. De asemenea, se poate actiona prin intermediul serverului un actuator 
(ventilator conectat la ESP32) utilizat pentru circularea aerului si in mod direct 
reducere (uniformizarea) umiditatii.

## Detalii implementare software
Pentru o implementare ușoară, am decis utilizarea limbajului
MicroPython.

IDE-ul utilizat este Thonny, intrucat ofera suport usor de lucru cu ESP32 
si exista multe instructiuni referitoare la setup.
Cu ajutorul MicroPython, se ia temperatura si umiditatea de la senzorul DHT11.

## Componente necesare:

* Placa (placi) de tip ESP32-WROOM
* Senzor(i) temperatura tip DHT11
* Breadboard
* Fire auxiliare de legare
* Baterii pentru alimentare placutelor (nu sunt necesare pentru proof of concept)

## Arhitectura:

## Folosire & Rulare:

Se va urca codul Micropython (fisierul main_esp32.py) pe placa cu ajutorul unui 
IDE specializat sau din command-line. Se recomanda utilizarea IDE-ului Thonny pentru 
lucru usor si rapid.

Pentru rularea serverului se utilizează python. Este necesara o instalare locala de python cu Flask, 
fie nativ, fie cu un mediu virtual.

python main.py

## Resurse & Bibliografie: