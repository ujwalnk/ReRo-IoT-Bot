from machine import Pin
from time import sleep

from common import DataSentinel

import network
import server

# Singleton class instance
# ds = DataSentinel()

def run_user_code():
    """
    Function to import the user code & run

    import the user.py & run the main function, delete the user.py file on completion or exception
    """

    # Running the user code inside try-catch block to catch exception & not crash the MCU
    # Only the first thrown exception is caught & communicated to the server
    # The first exception will stop the execution of the user code
    try:

        import user
        user.main()

    except Exception as e:
        # TODO: Stop code flow & return the exception to server over web socket
        print(f"Error: {e}")

    # User code file is removed, at every instance only one user.py file can be available on the bot
    finally:
        # TODO: Remove the user.py file
        pass

# Comment not added into the function to keep the function ISR short
# ISR function to counting pulses
def encoder_interrupt(pin):
    ds.increment_encoder_count()

def setup():
    """ Function to setup the environment """

    # TODO: Setup the server

    # WiFi Setup
    ssid = "ReRo Lab"
    password = ""
    station = network.WLAN(network.STA_IF)

    station.active(True)

    if not station.isconnected():

        station.connect(ssid, password)

        while station.isconnected() == False:
            pass

    print('Connection successful')
    print(station.ifconfig())

    # Configure & get server started
    server.start()

    # Interrupts configuration



# Run the setup code & then the user code
setup()
run_user_code()