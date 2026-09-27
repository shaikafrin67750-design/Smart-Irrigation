import RPi.GPIO as GPIO
import time

# GPIO pin configuration
SOIL_SENSOR_PIN = 17
RELAY_PIN = 27

# Change this depending on your relay module
# Many relay modules are active LOW
RELAY_ON = GPIO.LOW
RELAY_OFF = GPIO.HIGH

# Soil sensor setting
# Change this after testing your sensor
DRY_VALUE = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(SOIL_SENSOR_PIN, GPIO.IN)
GPIO.setup(RELAY_PIN, GPIO.OUT)

# Start with the pump turned off
GPIO.output(RELAY_PIN, RELAY_OFF)


def read_soil_sensor():
    """
    Read the soil moisture sensor.
    Returns True if the soil is dry.
    """
    sensor_value = GPIO.input(SOIL_SENSOR_PIN)

    if sensor_value == DRY_VALUE:
        return True
    else:
        return False


try:
    print("Smart irrigation system started.")

    while True:
        soil_is_dry = read_soil_sensor()

        if soil_is_dry:
            print("Soil is dry. Turning water pump ON.")
            GPIO.output(RELAY_PIN, RELAY_ON)

            # Water the plant for 5 seconds
            time.sleep(5)

            print("Turning water pump OFF.")
            GPIO.output(RELAY_PIN, RELAY_OFF)

            # Wait before checking again
            time.sleep(10)

        else:
            print("Soil moisture is sufficient. Pump is OFF.")
            GPIO.output(RELAY_PIN, RELAY_OFF)

            # Check again after 10 seconds
            time.sleep(10)

except KeyboardInterrupt:
    print("\nProgram stopped.")

finally:
    GPIO.output(RELAY_PIN, RELAY_OFF)
    GPIO.cleanup()
