# Raspberry Pi Based Smart Sensor and Motor Control System (EN)


## About the Project

This project enables the autonomous control of a DC motor based on specific conditions using a Raspberry Pi 3, a DHT11 temperature-humidity sensor, an HC-SR04 ultrasonic distance sensor, and an L293D motor driver. Additionally, to monitor the overall health and performance of the system, CPU temperature, CPU, and RAM usage rates are measured, integrating resource and thermal management capabilities.

## Key Features

*  **Sensor Data Reading**: Measures ambient temperature and humidity with DHT11, and ultrasonic distance with HC-SR04.
*  **Data Filtering**: Uses a moving average of the last N sensor readings for more stable measurements.
*  **Smart Decision Mechanism**: The motor operates based on defined distance (default: < 30 cm) **AND** temperature (default: > 23°C) thresholds.
*  **Tolerant Control**: If conditions are not met, the motor does not stop immediately; it waits for a specified number of consecutive cycles (default: 3). This reduces susceptibility to momentary fluctuations.
*  **System Resource Management**: Monitors CPU temperature, CPU, and RAM usage. If high load or thermal thresholds are exceeded, the loop delay is increased for system stability, or the motor is stopped for safety.

## File Structure

The project uses the following modular file structure:

* `sensors.py`: Contains the `SensorReader` class for reading data from DHT11 temperature/humidity and HC-SR04 ultrasonic distance sensors.
* `system_stats.py`: Includes utility functions for measuring the Raspberry Pi's CPU temperature, CPU, and RAM usage.
* `utils.py`: Contains a moving average filter class to smooth out sensor data.
* `motor_control.py`: Includes the `MotorController` class that controls the motor based on specified conditions (AND logic) and a tolerance counter.
* `main.py`: The main script that integrates all modules, manages the main control loop, and serves as the project's entry point.

## Requirements

### Hardware

* Raspberry Pi 3 or 3B+ (with Raspberry Pi OS or a compatible Linux distribution installed)
* DHT11 Temperature and Humidity Sensor
* HC-SR04 Ultrasonic Distance Sensor
* L293D Motor Driver IC/Module
* DC Motor (5V)
* Breadboard and Jumper Wires
* ~1kΩ and ~2kΩ resistors for the HC-SR04 ECHO pin (for voltage divider) or a pre-made voltage divider. (Pi's GPIOs operate at 3.3V, the HC-SR04 ECHO pin can output a 5V signal, so this is necessary to protect the GPIO pin.)
* External power supply for the motor (optional but recommended, especially if the motor draws more current than the Pi can safely provide).

### Software

* Python 3.7+
* Required Python libraries: `RPi.GPIO`, `psutil`, `adafruit-blinka`, `adafruit-circuitpython-dht`.
    For installation:
    ```bash
    sudo apt update
    sudo apt install python3-pip python3-rpi.gpio python3-psutil git
    pip3 install adafruit-blinka adafruit-circuitpython-dht
    ```

## Hardware Connections

**Important Note:** Ensure the Raspberry Pi is turned off while making connections. GPIO pin numbers (BCM) and physical pin numbers are different. This documentation uses **physical pin numbers** (sequential numbers on the board layout). BCM GPIO numbers are provided in parentheses.

1.  **DHT11 Temperature-Humidity Sensor**
    * VCC → Pin 1 (3.3V)
    * GND → Pin 6 (GND)
    * DATA → Pin 11 (GPIO17)

2.  **HC-SR04 Ultrasonic Distance Sensor**
    * VCC → Pin 2 (5V)
    * GND → Pin 9 (GND)
    * TRIG → Pin 16 (GPIO23)
    * ECHO → **Voltage Divider** → Pin 18 (GPIO24)
        * **Voltage Divider Detail:** The HC-SR04 ECHO pin outputs a 5V signal. Raspberry Pi GPIOs are 3.3V tolerant. To protect GPIO24, a voltage divider (e.g., 1kΩ resistor between ECHO and GPIO, and a 2kΩ resistor between GPIO and GND) must be connected between the ECHO pin and GPIO24.

3.  **L293D Motor Driver**
    * Logic VCC (VCC1 or Pin 16 on IC) → Pin 4 (Raspberry Pi 5V)
    * Motor VCC (VCC2 or Pin 8 on IC) → **External 5V Power Supply** (For the motor. Powering from Raspberry Pi might damage the Pi or be insufficient.)
    * GND (Pins 4,5,12,13 on IC) → Raspberry Pi GND (e.g., Pin 14, 20, 25)
    * EN1 (Enable 1 - Pin 1 on IC, for motor speed control) → Pin 12 (GPIO18 - PWM capable pin)
    * IN1 (Input 1 - Pin 2 on IC, for motor direction control) → Pin 13 (GPIO27)
    * IN2 (Input 2 - Pin 7 on IC, for motor direction control) → Pin 15 (GPIO22)
    * OUT1 / OUT2 (Output 1/2 - Pins 3 & 6 on IC) → DC Motor terminals

## Setup and Running

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Keray535/Raspberry-Pi-Based-Smart-Sensor-and-Motor-Control-System.git
    ```

2.  **Install Required System Packages (If not already installed):**
    ```bash
    sudo apt update
    sudo apt install python3-pip python3-rpi.gpio python3-psutil
    ```

3.  **Create and Activate a Python Virtual Environment (Recommended):**
    ```bash
    python3 -m venv .venv
    source venv/bin/activate
    ```
    *(To exit the virtual environment, use the `deactivate` command.)*

4.  **Install Required Python Libraries:**
    ```bash
    pip install --upgrade pip setuptools wheel
    pip install adafruit-blinka adafruit-circuitpython-dht psutil RPi.GPIO
    ```
    *(If a `requirements.txt` file is created, all dependencies can be installed at once using `pip install -r requirements.txt`.)*

5.  **Run the Main Program:**
    `sudo` is required for GPIO pin access.
    ```bash
    sudo python3 main.py
    ```

## Configuration Parameters

The following basic parameters can be easily edited at the beginning of the `main.py` file:

* `DIST_THRESH`: Maximum distance threshold (cm) for the motor to operate.
* `TEMP_THRESH`: Minimum temperature threshold (°C) for the motor to operate.
* `STOP_TOLERANCE`: Number of consecutive tolerance cycles before stopping the motor if conditions are not met.
* `BASE_DELAY`: Base delay time (seconds) for the main control loop. Can be dynamically adjusted based on system load.
* `DIST_SIZE` / `TEMP_SIZE`: Window sizes (number of samples to take) for the moving average filter for distance and temperature measurements.

## Contributing

Contributions are welcome! If you find a bug, want to improve a feature, or have any suggestions, please:
1.  Fork the project.
2.  Create a new feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push your branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request (PR).


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Raspberry Pi Based Smart Sensor and Motor Control System (DE)


Dieses Projekt ermöglicht die autonome Steuerung eines Gleichstrommotors basierend auf bestimmten Bedingungen unter Verwendung eines Raspberry Pi 3, eines DHT11 Temperatur-Feuchtigkeitssensors, eines HC-SR04 Ultraschall-Distanzsensors und eines L293D Motortreibers. Zusätzlich werden zur Überwachung des Gesamtzustands und der Leistung des Systems CPU-Temperatur, CPU- und RAM-Auslastungsraten gemessen, wodurch Ressourcen- und Wärmemanagementfunktionen integriert werden.

## Hauptmerkmale

*  **Sensordaten lesen**: Misst Umgebungstemperatur und Luftfeuchtigkeit mit DHT11 und Ultraschallentfernung mit HC-SR04.
*  **Datenfilterung**: Verwendet einen gleitenden Durchschnitt der letzten N Sensormesswerte für stabilere Messungen.
*  **Intelligenter Entscheidungsmechanismus**: Der Motor arbeitet basierend auf definierten Entfernungs- (Standard: < 30 cm) **UND** Temperaturschwellenwerten (Standard: > 23°C).
*  **Tolerante Steuerung**: Wenn die Bedingungen nicht erfüllt sind, stoppt der Motor nicht sofort; er wartet eine bestimmte Anzahl von aufeinanderfolgenden Zyklen (Standard: 3). Dies reduziert die Anfälligkeit für kurzzeitige Schwankungen.
*  **Systemressourcenmanagement**: Überwacht CPU-Temperatur, CPU- und RAM-Auslastung. Bei hoher Last oder Überschreitung thermischer Schwellenwerte wird die Schleifenverzögerung zur Systemstabilität erhöht oder der Motor aus Sicherheitsgründen gestoppt.

## Dateistruktur

Das Projekt verwendet die folgende modulare Dateistruktur:

* `sensors.py`: Enthält die `SensorReader`-Klasse zum Lesen von Daten von DHT11 Temperatur-/Feuchtigkeits- und HC-SR04 Ultraschall-Distanzsensoren.
* `system_stats.py`: Enthält Hilfsfunktionen zur Messung der CPU-Temperatur, CPU- und RAM-Auslastung des Raspberry Pi.
* `utils.py`: Enthält eine Filterklasse für den gleitenden Durchschnitt zur Glättung von Sensordaten.
* `motor_control.py`: Enthält die `MotorController`-Klasse, die den Motor basierend auf festgelegten Bedingungen (AND-Logik) und einem Toleranzzähler steuert.
* `main.py`: Das Hauptskript, das alle Module integriert, die Hauptsteuerschleife verwaltet und als Einstiegspunkt des Projekts dient.

## Anforderungen

### Hardware

* Raspberry Pi 3 oder 3B+ (mit installiertem Raspberry Pi OS oder einer kompatiblen Linux-Distribution)
* DHT11 Temperatur- und Feuchtigkeitssensor
* HC-SR04 Ultraschall-Distanzsensor
* L293D Motortreiber-IC/Modul
* DC-Motor (5V)
* Steckplatine (Breadboard) und Jumperkabel
* ~1kΩ und ~2kΩ Widerstände für den HC-SR04 ECHO-Pin (für Spannungsteiler) oder ein fertiger Spannungsteiler. (Die GPIOs des Pi arbeiten mit 3,3V, der HC-SR04 ECHO-Pin kann ein 5V-Signal ausgeben, daher ist dies zum Schutz des GPIO-Pins erforderlich.)
* Externe Stromversorgung für den Motor (optional, aber empfohlen, insbesondere wenn der Motor mehr Strom zieht, als der Pi sicher liefern kann).

### Software

* Python 3.7+
* Erforderliche Python-Bibliotheken: `RPi.GPIO`, `psutil`, `adafruit-blinka`, `adafruit-circuitpython-dht`.
    Zur Installation:
    ```bash
    sudo apt update
    sudo apt install python3-pip python3-rpi.gpio python3-psutil git
    pip3 install adafruit-blinka adafruit-circuitpython-dht
    ```

## Hardware-Verbindungen

**Wichtiger Hinweis:** Stellen Sie sicher, dass der Raspberry Pi ausgeschaltet ist, während Sie Verbindungen herstellen. GPIO-Pinnummern (BCM) und physische Pinnummern sind unterschiedlich. Diese Dokumentation verwendet **physische Pinnummern** (fortlaufende Nummern auf dem Board-Layout). BCM GPIO-Nummern sind in Klammern angegeben.

1.  **DHT11 Temperatur-Feuchtigkeitssensor**
    * VCC → Pin 1 (3.3V)
    * GND → Pin 6 (GND)
    * DATA → Pin 11 (GPIO17)

2.  **HC-SR04 Ultraschall-Distanzsensor**
    * VCC → Pin 2 (5V)
    * GND → Pin 9 (GND)
    * TRIG → Pin 16 (GPIO23)
    * ECHO → **Spannungsteiler** → Pin 18 (GPIO24)
        * **Spannungsteiler-Detail:** Der HC-SR04 ECHO-Pin gibt ein 5V-Signal aus. Raspberry Pi GPIOs sind 3,3V-tolerant. Zum Schutz von GPIO24 muss ein Spannungsteiler (z.B. 1kΩ Widerstand zwischen ECHO und GPIO, und ein 2kΩ Widerstand zwischen GPIO und GND) zwischen den ECHO-Pin und GPIO24 geschaltet werden.

3.  **L293D Motortreiber**
    * Logik VCC (VCC1 oder Pin 16 am IC) → Pin 4 (Raspberry Pi 5V)
    * Motor VCC (VCC2 oder Pin 8 am IC) → **Externe 5V Stromversorgung** (Für den Motor. Die Stromversorgung über den Raspberry Pi kann den Pi beschädigen oder unzureichend sein.)
    * GND (Pins 4,5,12,13 am IC) → Raspberry Pi GND (z.B. Pin 14, 20, 25)
    * EN1 (Enable 1 - Pin 1 am IC, für Motor-Geschwindigkeitsregelung) → Pin 12 (GPIO18 - PWM-fähiger Pin)
    * IN1 (Input 1 - Pin 2 am IC, für Motor-Drehrichtung) → Pin 13 (GPIO27)
    * IN2 (Input 2 - Pin 7 am IC, für Motor-Drehrichtung) → Pin 15 (GPIO22)
    * OUT1 / OUT2 (Output 1/2 - Pins 3 & 6 am IC) → DC-Motoranschlüsse

## Einrichtung und Ausführung

1.  **Repository:**
    ```bash
    git clone https://github.com/Keray535/Raspberry-Pi-Based-Smart-Sensor-and-Motor-Control-System.git
    ```

2.  **Erforderliche Systempakete Installieren (Falls noch nicht installiert):**
    ```bash
    sudo apt update
    sudo apt install python3-pip python3-rpi.gpio python3-psutil
    ```

3.  **Python Virtuelle Umgebung Erstellen und Aktivieren (Empfohlen):**
    ```bash
    python3 -m venv .venv
    source venv/bin/activate
    ```
    *(Um die virtuelle Umgebung zu verlassen, verwenden Sie den Befehl `deactivate`.)*

4.  **Erforderliche Python-Bibliotheken Installieren:**
    ```bash
    pip install --upgrade pip setuptools wheel
    pip install adafruit-blinka adafruit-circuitpython-dht psutil RPi.GPIO
    ```
    *(Wenn eine `requirements.txt`-Datei erstellt wird, können alle Abhängigkeiten auf einmal mit `pip install -r requirements.txt` installiert werden.)*

5.  **Hauptprogramm Ausführen:**
    `sudo` ist für den Zugriff auf GPIO-Pins erforderlich.
    ```bash
    sudo python3 main.py
    ```

## Konfigurationsparameter

Die folgenden grundlegenden Parameter können einfach am Anfang der Datei `main.py` bearbeitet werden:

* `DIST_THRESH`: Maximaler Entfernungsschwellenwert (cm), bei dem der Motor arbeitet.
* `TEMP_THRESH`: Minimaler Temperaturschwellenwert (°C), bei dem der Motor arbeitet.
* `STOP_TOLERANCE`: Anzahl der aufeinanderfolgenden Toleranzzyklen, bevor der Motor gestoppt wird, wenn die Bedingungen nicht erfüllt sind.
* `BASE_DELAY`: Grundverzögerungszeit (Sekunden) für die Hauptsteuerschleife. Kann dynamisch basierend auf der Systemlast angepasst werden.
* `DIST_SIZE` / `TEMP_SIZE`: Fenstergrößen (Anzahl der zu nehmenden Abtastwerte) für den gleitenden Durchschnittsfilter für Entfernungs- und Temperaturmessungen.

## Mitwirken

Beiträge sind willkommen! Wenn Sie einen Fehler finden, eine Funktion verbessern möchten oder Vorschläge haben, bitte:
1.  Forken Sie das Projekt.
2.  Erstellen Sie einen neuen Feature-Branch (`git checkout -b feature/TollesFeature`).
3.  Committen Sie Ihre Änderungen (`git commit -m 'Füge TollesFeature hinzu'`).
4.  Pushen Sie Ihren Branch (`git push origin feature/TollesFeature`).
5.  Öffnen Sie einen Pull Request (PR).


## Authors

* Bedirhan Kalkan
* Kadir Eray Güven
* Bilal Kutluca
