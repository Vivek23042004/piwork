import RPi.GPIO as GPIO
import time
import datetime
import board
import busio
import adafruit_ds3231
import threading

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pin Definitions
SERVO_PIN_1 = 18  # PWM pin for servo motor 1
SERVO_PIN_2 = 19  # PWM pin for servo motor 2
IR_SENSOR_1 = 17  # IR sensor for compartment 1
IR_SENSOR_2 = 27  # IR sensor for compartment 2
MAGNETIC_SWITCH_1 = 22  # Magnetic switch for compartment 1
MAGNETIC_SWITCH_2 = 23  # Magnetic switch for compartment 2
BUZZER_PIN = 24  # Buzzer pin
LED_PIN_1 = 25  # LED for compartment 1
LED_PIN_2 = 16  # LED for compartment 2

# Setup pins
GPIO.setup(SERVO_PIN_1, GPIO.OUT)
GPIO.setup(SERVO_PIN_2, GPIO.OUT)
GPIO.setup(IR_SENSOR_1, GPIO.IN)
GPIO.setup(IR_SENSOR_2, GPIO.IN)
GPIO.setup(MAGNETIC_SWITCH_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(MAGNETIC_SWITCH_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(LED_PIN_1, GPIO.OUT)
GPIO.setup(LED_PIN_2, GPIO.OUT)

# Initialize PWM for servo motors
servo1 = GPIO.PWM(SERVO_PIN_1, 50)  # 50Hz frequency
servo2 = GPIO.PWM(SERVO_PIN_2, 50)
servo1.start(0)
servo2.start(0)

# Initialize I2C for RTC DS3231
i2c = busio.I2C(board.SCL, board.SDA)
rtc = adafruit_ds3231.DS3231(i2c)

# Default medication times (24-hour format)
# Format: [[hour, minute], [hour, minute]] for each compartment
medication_times = [
    [[8, 0], [20, 0]],  # Compartment 1: 8:00 AM and 8:00 PM
    [[13, 0], [17, 0]]  # Compartment 2: 1:00 PM and 5:00 PM
]

# Flags for tracking medication status
medication_taken = [False, False]  # For two compartments
compartment_open = [False, False]  # For two compartments
alert_active = [False, False]  # For alert status

# Function to control servo position
def set_servo_angle(servo, angle):
    duty = angle / 18 + 2
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)  # Stop pulse to prevent jitter
def open_compartment(compartment_number):
    print(f"Opening compartment {compartment_number+1}")
    if compartment_number == 0:
        set_servo_angle(servo1, 90)
    else:
        set_servo_angle(servo2, 90)
    compartment_open[compartment_number] = True
    print(f"Box {compartment_number+1} opened")
    GPIO.output(LED_PIN_1 if compartment_number == 0 else LED_PIN_2, GPIO.HIGH)
    timer_thread = threading.Thread(target=compartment_timer, args=(compartment_number,))
    timer_thread.daemon = True
    timer_thread.start()

# Function to close compartment
def close_compartment(compartment_number):
    print(f"Closing compartment {compartment_number+1}")
    if compartment_number == 0:
        set_servo_angle(servo1, 0)
    else:
        set_servo_angle(servo2, 0)
    compartment_open[compartment_number] = False
    GPIO.output(LED_PIN_1 if compartment_number == 0 else LED_PIN_2, GPIO.LOW)

# Function to sound buzzer
def sound_buzzer(times=3, duration=0.2, pause=0.2):
    for _ in range(times):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        time.sleep(pause)

# Function to alert user if pill not taken
def alert_pill_not_taken(compartment_number):
    if not medication_taken[compartment_number] and compartment_open[compartment_number]:
        print(f"ALERT: Pill from compartment {compartment_number+1} not taken!")
        close_compartment(compartment_number)
        sound_buzzer(times=5, duration=0.5, pause=0.3)
        led_pin = LED_PIN_1 if compartment_number == 0 else LED_PIN_2
        alert_active[compartment_number] = True
        for _ in range(10):
            if not alert_active[compartment_number]:
                break
            GPIO.output(led_pin, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(led_pin, GPIO.LOW)
            time.sleep(0.2)
        alert_active[compartment_number] = False

# One-minute timer for taking medication
def compartment_timer(compartment_number):
    time.sleep(60)
    if compartment_open[compartment_number] and not medication_taken[compartment_number]:
        alert_pill_not_taken(compartment_number)
def check_pill_taken():
    for compartment in range(2):
        if compartment_open[compartment]:
            ir_pin = IR_SENSOR_1 if compartment == 0 else IR_SENSOR_2
            if GPIO.input(ir_pin) == GPIO.HIGH and not medication_taken[compartment]:
                print(f"Pill from compartment {compartment+1} is taken")
                medication_taken[compartment] = True
                alert_active[compartment] = False
                time.sleep(2)
                close_compartment(compartment)

# Function to check if it's time for medication
def check_medication_time():
    current_time = rtc.datetime
    current_hour = current_time.tm_hour
    current_minute = current_time.tm_min
    for compartment in range(2):
        for time_slot in medication_times[compartment]:
            if current_hour == time_slot[0] and current_minute == time_slot[1]:
                if not compartment_open[compartment] and not medication_taken[compartment]:
                    sound_buzzer()
                    open_compartment(compartment)
                    return

# Function to set medication time
def set_medication_time(compartment, slot, hour, minute):
    if 0 <= compartment <= 1 and 0 <= slot <= 1:
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            medication_times[compartment][slot] = [hour, minute]
            print(f"Medication time for compartment {compartment+1}, slot {slot+1} set to {hour:02d}:{minute:02d}")
            return True
    return False

# Function to set RTC time
def set_rtc_time(year, month, day, hour, minute, second):
    rtc.datetime = time.struct_time((year, month, day, hour, minute, second, 0, -1, -1))
    print(f"RTC time set to: {year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}")

# Function to get current RTC time
def get_rtc_time():
    dt = rtc.datetime
    return f"{dt.tm_year}-{dt.tm_mon:02d}-{dt.tm_mday:02d} {dt.tm_hour:02d}:{dt.tm_min:02d}:{dt.tm_sec:02d}"

# Reset medication status at midnight
def reset_medication_status():
    current_time = rtc.datetime
    if current_time.tm_hour == 0 and current_time.tm_min == 0:
        for compartment in range(2):
            medication_taken[compartment] = False
            print(f"Medication status for compartment {compartment+1} reset for new day")

# Function to check magnetic switches
def check_magnetic_switches():
    for compartment in range(2):
        magnetic_pin = MAGNETIC_SWITCH_1 if compartment == 0 else MAGNETIC_SWITCH_2
        if GPIO.input(magnetic_pin) == GPIO.HIGH:
            print(f"WARNING: Compartment {compartment+1} may have been tampered with!")

# Main function
def main():
    print("Medication Reminder System Started")
    print("Current RTC Time:", get_rtc_time())
    print("Medication times:")
    for compartment in range(2):
        for slot, time_slot in enumerate(medication_times[compartment]):
            print(f"Compartment {compartment+1}, Slot {slot+1}: {time_slot[0]:02d}:{time_slot[1]:02d}")
    try:
        close_compartment(0)
        close_compartment(1)
        while True:
            check_medication_time()
            check_pill_taken()
            check_magnetic_switches()
            reset_medication_status()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program stopped by user")
    finally:
        servo1.stop()
        servo2.stop()
        GPIO.cleanup()
        print("GPIO cleanup completed")

# Command Line Interface
def cli():
    while True:
        print("\nMedication Reminder System - CLI")
        print("1. Set medication time")
        print("2. Set RTC time")
        print("3. Display current RTC time")
        print("4. Test open compartment")
        print("5. Test close compartment")
        print("6. Test buzzer")
        print("7. Start main program")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            try:
                compartment = int(input("Enter compartment (1 or 2): ")) - 1
                slot = int(input("Enter slot (1 or 2): ")) - 1
                hour = int(input("Enter hour (0-23): "))
                minute = int(input("Enter minute (0-59): "))
                if set_medication_time(compartment, slot, hour, minute):
                    print("Medication time set successfully")
                else:
                    print("Invalid input for setting medication time")
            except ValueError:
                print("Please enter valid numbers")

        elif choice == '2':
            try:
                year = int(input("Enter year: "))
                month = int(input("Enter month (1-12): "))
                day = int(input("Enter day (1-31): "))
                hour = int(input("Enter hour (0-23): "))
                minute = int(input("Enter minute (0-59): "))
                second = int(input("Enter second (0-59): "))
                set_rtc_time(year, month, day, hour, minute, second)
            except ValueError:
                print("Please enter valid numbers")

        elif choice == '3':
            print("Current RTC time:", get_rtc_time())

        elif choice == '4':
            try:
                compartment = int(input("Enter compartment to open (1 or 2): ")) - 1
                if 0 <= compartment <= 1:
                    open_compartment(compartment)
                else:
                    print("Invalid compartment number")
            except ValueError:
                print("Please enter a valid number")

        elif choice == '5':
            try:
                compartment = int(input("Enter compartment to close (1 or 2): ")) - 1
                if 0 <= compartment <= 1:
                    close_compartment(compartment)
                else:
                    print("Invalid compartment number")
            except ValueError:
                print("Please enter a valid number")

        elif choice == '6':
            sound_buzzer()

        elif choice == '7':
            print("Starting main program. Press Ctrl+C to stop.")
            main()

        elif choice == '8':
            print("Exiting program")
            servo1.stop()
            servo2.stop()
            GPIO.cleanup()
            break

        else:
            print("Invalid choice. Please try again.")

# ? Correct entry point
if __name__ == "__main__":
    cli()



