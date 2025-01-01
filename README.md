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

Serverul central se rulează pe laptolul/PC ul de acasă conectat la rețeaua de Wi-Fi.
Fiecare placuta va rula codul ce trimite cereri HTTP catre serverul central. 

Siguranta conumicatiei este garantata si de SSL prin HTTPS insa si securitatea retelei locale 
are un rol important.

Reteaua locala si modalitatea de comunicatie prin Wi-Fi reprezinta backbone-ul arhitecturii gandite.

Am ales Wi-Fi ul si HTTP ul in proiectare in detrimentul altor modalitati tocmai din cauza replicabilitatii
in majoritatea caselor.

## Folosire & Rulare:

Se va urca codul Micropython (fisierul main_esp32.py) pe placa cu ajutorul unui 
IDE specializat sau din command-line. Se recomanda utilizarea IDE-ului Thonny pentru 
lucru usor si rapid.

Pentru rularea serverului se utilizează python. Este necesara o instalare locala de python cu Flask, 
fie nativ, fie cu un mediu virtual.

python main.py

## Implementare

Serverul este implementat in Flask.

Se utilizeaza o baza de date SQLite  pentru stocarea tuturor datelor de la senzori.

Pentru realizarea codului pe ESP-32 am utilizat Micopython datorita timpului mai mic 
de dezvoltare si facilitatilor incluse.

## Vizualizarea si procesarea datelor

Pentru vizualizarea datelor am utilizat Chart.js deoarece este usor de implementat intr-un 
site web, este flexibil si relativ usor de utilizat.

Pentru procesare am decis calculul catorva caracteristici ale datelor colectate pana in prezent,
atat pentru temperatura cat si pentru umiditate: minim, maxim si medie.

De asemenea, am utilizat ARIMA pentru predictia urmatoarelor valori folosindu-le pe cele anterioare.

## Securitate

Securitatea este asigurata atat prin plasarea in reteaua locala, cat si prin utilizarea SSL din https.

Serverul Flask are certificate ce ii permit comunicarea in acest fel.

In acest mod solutia este fiabila, sigura si arhicunoscuta pentru eficienta ei.

## Provocari si solutii

Utilizarea bibliotecii SSL pe placuta, neexistand in Micropython pentru ESP-32, rezolvat 
prin instalarea separata a bibliotecii cu ajutorul IDE-ului.

Problema ca pornirea ventilatorului sa fie usor de introdus, fara a transforma placuta in server,
a fost realizata cu o ruta suplimentara, la care placuta trimite un GET periodic si obtine starea acestuia.
Am decis utilizarea async din Micropython pentru ajutor in rezolvarea acestei probleme.

De asemenea, legarea switchului si a ventilatorului la baterie si placuta au fost provocatoare, dar cu ajutorul 
tutorialelor si schemelor electrice (manuale), problema a fost rezolvata.

## Resurse & Bibliografie:

* Laboratoare PRIoT
* Laboratoare & Tema ASC
* https://www.w3schools.com/
* https://www.youtube.com/watch?v=Bj0j6fP0FPs
* https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf