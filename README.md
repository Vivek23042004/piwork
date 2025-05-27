# Medication Reminder System

A web-based interface for a Raspberry Pi 3 medication reminder system with compartment control, scheduling, and monitoring.

## Features

- Web-based UI accessible from any device on the same network
- Set medication times for two compartments (two slots each)
- Control compartment doors (open/close)
- Test buzzer functionality
- Set system time
- Monitor system status and logs
- Automatic medication dispensing based on schedule

## Hardware Requirements

- Raspberry Pi 3
- DS3231 RTC module
- 2 Servo motors
- 2 IR sensors
- 2 Magnetic switches
- 1 Buzzer
- 2 LEDs

## Installation

1. Clone this repository to your Raspberry Pi 3:

```bash
git clone <repository-url>
cd medication-reminder-system
```

2. Install the required dependencies:

```bash
pip3 install -r requirements.txt
```

3. Run the application:

```bash
python3 app.py
```

4. Access the web interface by navigating to `http://<raspberry-pi-ip>:5000` in your web browser.

## Default Login

- Username: admin
- Password: password

**Note:** For security reasons, you should change these credentials in the `app.py` file before deploying in a production environment.

## Usage

1. **Dashboard**: View system status, compartment status, and control compartments
2. **Medication Settings**: Set medication times for each compartment
3. **System Settings**: Set the system time
4. **System Logs**: View system activity logs

## Running at Startup

To make the application start automatically when the Raspberry Pi boots:

1. Create a systemd service file:

```bash
sudo nano /etc/systemd/system/medication-reminder.service
```

2. Add the following content (adjust paths as needed):

```
[Unit]
Description=Medication Reminder System
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/medication-reminder-system/app.py
WorkingDirectory=/home/pi/medication-reminder-system
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

3. Enable and start the service:

```bash
sudo systemctl enable medication-reminder.service
sudo systemctl start medication-reminder.service
```

## Troubleshooting

- Check logs in the `logs` directory for error messages
- Ensure all hardware connections are correct
- Verify that the Raspberry Pi has the correct permissions to access GPIO pins

## License

This project is licensed under the MIT License - see the LICENSE file for details.