# 2021-01-02 Mouse trap sensor
# Shows last 5 PIR activations

# Still room for improvement
# e.g. date formatting, code efficiency


# Import Python header files
import RPi.GPIO as GPIO
import time
from datetime import datetime

# Set the GPIO naming convention
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set a variable to hold the GPIO Pin identity
pinpir = 17

print("PIR Module Test (CTRL-C to exit)")

# Set pin as input
GPIO.setup(pinpir, GPIO.IN)

# Variables to hold the current and last states
currentstate = 0
previousstate = 0

# Use Python array (list)
# alarm001[0] - Alarm start time
# alarm001[1] - Alarm end time
# alarm001[2] - Alarm duration

alarm001 = ["No Alarm", "No Alarm", "No Alarm"]
alarm002 = ["No Alarm", "No Alarm", "No Alarm"]
alarm003 = ["No Alarm", "No Alarm", "No Alarm"]
alarm004 = ["No Alarm", "No Alarm", "No Alarm"]
alarm005 = ["No Alarm", "No Alarm", "No Alarm"]


try:
    print("Waiting for PIR to settle ...")
    # Loop until PIR output is 0
    while GPIO.input(pinpir) == 1:
        currentstate = 0

    print("    Ready")
    # Loop until users quits with CTRL-C
    while True:
        # Read PIR state
        currentstate = GPIO.input(pinpir)

        # If the PIR is triggered
        if currentstate == 1 and previousstate == 0:

            # Move last alarm down list of lists
            # List slicing [:] required to prevent persistent list sync

            alarm005 = alarm004[:]
            alarm004 = alarm003[:]
            alarm003 = alarm002[:]
            alarm002 = alarm001[:]

            print("    Motion detected!")
            alarm001[0] = datetime.now()
            # print(alarm001[0])

            # Record previous state
            previousstate = 1
        # If the PIR has returned to ready state
        elif currentstate == 0 and previousstate == 1:
            print("    Ready")
            alarm001[1] = datetime.now()
            alarm001[2] = alarm001[1] - alarm001[0]

            # print(alarm001[1])
            # print(alarm001[2])
            previousstate = 0

            print(alarm005)
            print(alarm004)
            print(alarm003)
            print(alarm002)
            print(alarm001)

            print("Last alarm start")
            print(alarm001[0])

            print("Last alarm end")
            print(alarm001[1])

            print("Last alarm duration")
            print(alarm001[2])

        # Wait for 10 milliseconds
        time.sleep(0.01)

except KeyboardInterrupt:
    print("    Quit")

    # Reset GPIO settings
    GPIO.cleanup()
