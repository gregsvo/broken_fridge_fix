import time, machine, onewire, ds18x20
from machine import Pin, Signal, Timer


CONFIG = {
    "THERMO_SENSOR_PIN": 3,
    "RELAY_PIN": 12,
    "LOW": 34,
    "HIGH": 40,
    "LED_PIN": 13
}

relay_pin = CONFIG.get("RELAY_PIN")
relay = Signal(Pin(relay_pin, Pin.OUT), invert=False)
led = Signal(Pin(CONFIG.get('LED_PIN'), Pin.Out), invert=False)

def main():
    while True:
        time.sleep_ms(8000)
        thermo()

# create the ds18x20/onewire object
def setup_DS():
    roms_list = []
    while len(roms_list) == 0:
        ds_object = ds18x20.DS18X20(
            onewire.OneWire(
                machine.Pin(
                    CONFIG.get('THERMO_SENSOR_PIN')
                    )
                )
            )
        roms_list = ds_object.scan()
    print('found devices: ', roms_list)
    return ds_object, roms_list


def fetch_ds_data(ds_object, roms_list):
    ds_object.convert_temp()
    time.sleep_ms(2000)
    for rom in roms_list:
        temp = ds_object.read_temp(rom)
    return temp


def should_turn_on_relay(air_temp):
    low_temp = CONFIG.get('LOW')
    high_temp = CONFIG.get('HIGH')
    print("Current fridge temp: ", air_temp)
    if air_temp >= high_temp:
        print("Fridge should turn ON.")
        return True
    if air_temp <= low_temp:
        print("Fridge should turn OFF.")
        return False

def thermo():
    ds_object, roms_list = setup_DS()
    if ds_object and roms_list:
        air_temp = fetch_ds_data(ds_object, roms_list)
        refridge_too_warm = should_turn_on_relay(air_temp)
        relay.on() if refridge_too_warm else relay.off()
        led.on() if refridge_too_warm else led.off()
