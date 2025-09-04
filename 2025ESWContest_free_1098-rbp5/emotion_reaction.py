import time
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas

# Initialize the SPI interface and the MAX7219 device
# Make sure port and device are correct for your setup.
serial = spi(port=0, device=0, gpio=noop())

# Create the device. Adjust rotate or block_orientation if your
# matrix is upside down or sideways.
# For a single 8x8 matrix, cascaded=1.
device = max7219(serial, cascaded=1, rotate=1)

def emotion_reaction(index):
    
    sleep_time_1 = 0.5
    sleep_time_2 = 0.5
    
    if index == 0: # no emotion
        sleep_time_1 = 0.5
        sleep_time_2 = 0.5
    if index == 1: # anger
        sleep_time_1 = 2.0
        sleep_time_2 = 2.0
    if index == 2: # disgust
        sleep_time_1 = 1.8
        sleep_time_2 = 1.8
    if index == 3: # fear
        sleep_time_1 = 1.5
        sleep_time_2 = 1.5
    if index == 4: # happiness
        sleep_time_1 = 0.3
        sleep_time_2 = 0.3
    if index == 5: # sadness
        sleep_time_1 = 1.0
        sleep_time_2 = 1.0
    if index == 6: # surprise
        sleep_time_1 = 2.5
        sleep_time_2 = 2.5
        
    try:
        while True:
            with canvas(device) as draw:
                draw.rectangle(device.bounding_box, outline="white", fill="white")
            time.sleep(sleep_time_1)
            device.clear()
            time.sleep(sleep_time_2)
    except KeyboardInterrupt:
        print("\nProgram stopped.")
        device.clear()