import time
import socketio
import platform
import time

conversion = 1/0.7204
CHANNEL = 0

try:
    if platform.system() == "Linux":
        import ADS1263
        import RPi.GPIO as GPIO

        REF = 5.08
        ADC = ADS1263.ADS1263()
        if (ADC.ADS1263_init_ADC1('ADS1263_7200SPS') == -1):
            ADC.ADS1263_Exit()
            print("Failed to initialize ADC1")
            exit()
        ADC.ADS1263_SetMode(1)
        ads1263_available = True
except ImportError:
    print("ADS1263 library not available, using simulated data")

sio = socketio.Client()
sio.connect('192.168.1.100:8090')

def read_adc():
    value = ADC.ADS1263_GetChannalValue(CHANNEL)
    if value >> 31 == 1:
        voltage = -(REF * 2 - value * REF / 0x80000000)
    else:
        voltage = value * REF / 0x7fffffff
    return voltage * conversion

while True:
    # Read your data from ADS1263 and Geophone
    # This is a placeholder value:
    data = read_adc()

    # Send data to server
    sio.emit('client_data', {'value': data})

    time.sleep(1)
