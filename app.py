import RPi.GPIO as GPIO
import time
import datetime
import board
import busio
import adafruit_ds3231
import threading
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for
import logging
from logging.handlers import RotatingFileHandler
import os
from functools import wraps

# Setup logging
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'medication_system.log')

logger = logging.getLogger('medication_system')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

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

# System status
system_running = False
system_messages = []
MAX_MESSAGES = 100  # Maximum number of messages to keep in memory

# Function to add a message to the system messages list
def add_system_message(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    system_messages.append({"timestamp": timestamp, "message": message})
    logger.info(message)
    # Keep only the last MAX_MESSAGES messages
    if len(system_messages) > MAX_MESSAGES:
        system_messages.pop(0)

# Function to control servo position
def set_servo_angle(servo, angle):
    duty = angle / 18 + 2
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)  # Stop pulse to prevent jitter

def open_compartment(compartment_number):
    message = f"Opening compartment {compartment_number+1}"
    add_system_message(message)
    if compartment_number == 0:
        set_servo_angle(servo1, 90)
    else:
        set_servo_angle(servo2, 90)
    compartment_open[compartment_number] = True
    add_system_message(f"Box {compartment_number+1} opened")
    GPIO.output(LED_PIN_1 if compartment_number == 0 else LED_PIN_2, GPIO.HIGH)
    timer_thread = threading.Thread(target=compartment_timer, args=(compartment_number,))
    timer_thread.daemon = True
    timer_thread.start()
    return True

# Function to close compartment
def close_compartment(compartment_number):
    message = f"Closing compartment {compartment_number+1}"
    add_system_message(message)
    if compartment_number == 0:
        set_servo_angle(servo1, 0)
    else:
        set_servo_angle(servo2, 0)
    compartment_open[compartment_number] = False
    GPIO.output(LED_PIN_1 if compartment_number == 0 else LED_PIN_2, GPIO.LOW)
    return True

# Function to sound buzzer
def sound_buzzer(times=3, duration=0.2, pause=0.2):
    add_system_message(f"Sounding buzzer: {times} times")
    for _ in range(times):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        time.sleep(pause)
    return True

# Function to alert user if pill not taken
def alert_pill_not_taken(compartment_number):
    if not medication_taken[compartment_number] and compartment_open[compartment_number]:
        add_system_message(f"ALERT: Pill from compartment {compartment_number+1} not taken!")
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
                add_system_message(f"Pill from compartment {compartment+1} is taken")
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
            add_system_message(f"Medication time for compartment {compartment+1}, slot {slot+1} set to {hour:02d}:{minute:02d}")
            return True
    return False

# Function to set RTC time
def set_rtc_time(year, month, day, hour, minute, second):
    rtc.datetime = time.struct_time((year, month, day, hour, minute, second, 0, -1, -1))
    add_system_message(f"RTC time set to: {year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}")
    return True

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
            add_system_message(f"Medication status for compartment {compartment+1} reset for new day")

# Function to check magnetic switches
def check_magnetic_switches():
    for compartment in range(2):
        magnetic_pin = MAGNETIC_SWITCH_1 if compartment == 0 else MAGNETIC_SWITCH_2
        if GPIO.input(magnetic_pin) == GPIO.HIGH:
            add_system_message(f"WARNING: Compartment {compartment+1} may have been tampered with!")

# Main monitoring function
def monitoring_thread():
    global system_running
    add_system_message("Medication Reminder System Started")
    add_system_message(f"Current RTC Time: {get_rtc_time()}")
    add_system_message("Medication times:")
    for compartment in range(2):
        for slot, time_slot in enumerate(medication_times[compartment]):
            add_system_message(f"Compartment {compartment+1}, Slot {slot+1}: {time_slot[0]:02d}:{time_slot[1]:02d}")
    
    try:
        close_compartment(0)
        close_compartment(1)
        while system_running:
            check_medication_time()
            check_pill_taken()
            check_magnetic_switches()
            reset_medication_status()
            time.sleep(1)
    except Exception as e:
        add_system_message(f"Error in monitoring thread: {str(e)}")
    finally:
        add_system_message("Monitoring thread stopped")

# Initialize Flask app
app = Flask(__name__)

# Simple authentication (for demonstration purposes)
# In a production environment, use a more secure authentication method
USERNAME = 'admin'
PASSWORD = 'password'

def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated

# Routes
@app.route('/')
def index():
    return render_template('index.html', 
                          rtc_time=get_rtc_time(),
                          medication_times=medication_times,
                          medication_taken=medication_taken,
                          compartment_open=compartment_open,
                          system_running=system_running)

@app.route('/api/status')
def get_status():
    return jsonify({
        'rtc_time': get_rtc_time(),
        'medication_times': medication_times,
        'medication_taken': medication_taken,
        'compartment_open': compartment_open,
        'system_running': system_running,
        'system_messages': system_messages[-20:]  # Return last 20 messages
    })

@app.route('/api/set_medication_time', methods=['POST'])
@requires_auth
def api_set_medication_time():
    data = request.json
    try:
        compartment = int(data.get('compartment', 0)) - 1
        slot = int(data.get('slot', 0)) - 1
        hour = int(data.get('hour', 0))
        minute = int(data.get('minute', 0))
        
        if set_medication_time(compartment, slot, hour, minute):
            return jsonify({"success": True, "message": "Medication time set successfully"})
        else:
            return jsonify({"success": False, "message": "Invalid input for setting medication time"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})

@app.route('/api/set_rtc_time', methods=['POST'])
@requires_auth
def api_set_rtc_time():
    data = request.json
    try:
        year = int(data.get('year', 2023))
        month = int(data.get('month', 1))
        day = int(data.get('day', 1))
        hour = int(data.get('hour', 0))
        minute = int(data.get('minute', 0))
        second = int(data.get('second', 0))
        
        if set_rtc_time(year, month, day, hour, minute, second):
            return jsonify({"success": True, "message": "RTC time set successfully"})
        else:
            return jsonify({"success": False, "message": "Failed to set RTC time"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})

@app.route('/api/open_compartment', methods=['POST'])
@requires_auth
def api_open_compartment():
    data = request.json
    try:
        compartment = int(data.get('compartment', 0)) - 1
        if 0 <= compartment <= 1:
            if open_compartment(compartment):
                return jsonify({"success": True, "message": f"Compartment {compartment+1} opened"})
            else:
                return jsonify({"success": False, "message": "Failed to open compartment"})
        else:
            return jsonify({"success": False, "message": "Invalid compartment number"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})

@app.route('/api/close_compartment', methods=['POST'])
@requires_auth
def api_close_compartment():
    data = request.json
    try:
        compartment = int(data.get('compartment', 0)) - 1
        if 0 <= compartment <= 1:
            if close_compartment(compartment):
                return jsonify({"success": True, "message": f"Compartment {compartment+1} closed"})
            else:
                return jsonify({"success": False, "message": "Failed to close compartment"})
        else:
            return jsonify({"success": False, "message": "Invalid compartment number"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})

@app.route('/api/test_buzzer', methods=['POST'])
@requires_auth
def api_test_buzzer():
    try:
        if sound_buzzer():
            return jsonify({"success": True, "message": "Buzzer test completed"})
        else:
            return jsonify({"success": False, "message": "Failed to test buzzer"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})

@app.route('/api/start_system', methods=['POST'])
@requires_auth
def api_start_system():
    global system_running
    try:
        if not system_running:
            system_running = True
            thread = threading.Thread(target=monitoring_thread)
            thread.daemon = True
            thread.start()
            return jsonify({"success": True, "message": "System started"})
        else:
            return jsonify({"success": False, "message": "System is already running"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})

@app.route('/api/stop_system', methods=['POST'])
@requires_auth
def api_stop_system():
    global system_running
    try:
        if system_running:
            system_running = False
            time.sleep(2)  # Give time for the monitoring thread to stop
            return jsonify({"success": True, "message": "System stopped"})
        else:
            return jsonify({"success": False, "message": "System is not running"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})

# Cleanup function to be called when the application exits
def cleanup():
    global system_running
    system_running = False
    time.sleep(1)
    servo1.stop()
    servo2.stop()
    GPIO.cleanup()
    add_system_message("GPIO cleanup completed")

# Register the cleanup function to be called on exit
import atexit
atexit.register(cleanup)

if __name__ == '__main__':
    try:
        # Start the Flask app
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    except Exception as e:
        logger.error(f"Error starting application: {str(e)}")
    finally:
        cleanup()