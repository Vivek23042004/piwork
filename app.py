<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Medication Adherence System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);"

            "min-height: 100vh;"
            color: #333;
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .main-header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .main-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #4CAF50, #2196F3, #FF9800, #E91E63);
        }

        .main-header h1 {
            color: #2c3e50;
            font-size: 2.5rem;
            margin-bottom: 15px;
            font-weight: 700;
        }

        .main-header .subtitle {
            color: #7f8c8d;
            font-size: 1.1rem;
            margin-bottom: 20px;
        }

        .system-status {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px;
            flex-wrap: wrap;
        }

        .status-card {
            background: rgba(255, 255, 255, 0.9);
            padding: 15px 25px;
            border-radius: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }

        .status-card:hover {
            transform: translateY(-2px);
        }

        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            position: relative;
        }

        .status-indicator.pulse {
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.2); }
            100% { transform: scale(1); }
        }

        .status-on {
            background: linear-gradient(45deg, #4CAF50, #8BC34A);
        }

        .status-off {
            background: linear-gradient(45deg, #f44336, #FF5722);
        }

        .status-warning {
            background: linear-gradient(45deg, #FF9800, #FFC107);
        }

        .tabs {
            display: flex;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 5px;
            margin-bottom: 30px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
            overflow-x: auto;
        }

        .tab {
            flex: 1;
            padding: 15px 20px;
            cursor: pointer;
            border-radius: 10px;
            text-align: center;
            font-weight: 600;
            transition: all 0.3s ease;
            white-space: nowrap;
            min-width: 120px;
        }

        .tab:hover {
            background: rgba(103, 126, 234, 0.1);
        }

        .tab.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
            animation: fadeIn 0.5s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .card h2 {
            color: #2c3e50;
            margin-bottom: 25px;
            font-size: 1.8rem;
            font-weight: 600;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
        }

        .compartment {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.7) 100%);
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 15px;
            padding: 25px;
            position: relative;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .compartment:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
        }

        .compartment::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #4CAF50, #2196F3);
        }

        .compartment-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .compartment-header h3 {
            color: #2c3e50;
            font-size: 1.3rem;
            font-weight: 600;
        }

        .compartment-status {
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            color: white;
        }

        .status-open {
            background: linear-gradient(45deg, #4CAF50, #8BC34A);
        }

        .status-closed {
            background: linear-gradient(45deg, #f44336, #FF5722);
        }

        .medication-info {
            background: rgba(255, 255, 255, 0.7);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
        }

        .medication-info p {
            margin-bottom: 8px;
            font-weight: 500;
        }

        .medication-times {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .time-slot {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9rem;
        }

        .adherence-indicator {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-top: 10px;
        }

        .adherence-bar {
            flex: 1;
            height: 8px;
            background: rgba(0, 0, 0, 0.1);
            border-radius: 4px;
            overflow: hidden;
        }

        .adherence-fill {
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #8BC34A);
            border-radius: 4px;
            transition: width 0.5s ease;
        }

        .button-group {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        button {
            padding: 12px 24px;
            border: none;
            border-radius: 25px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.9rem;
            flex: 1;
            min-width: 120px;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }

        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .btn-success {
            background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
            color: white;
        }

        .btn-danger {
            background: linear-gradient(135deg, #f44336 0%, #FF5722 100%);
            color: white;
        }

        .btn-warning {
            background: linear-gradient(135deg, #FF9800 0%, #FFC107 100%);
            color: white;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #2c3e50;
        }

        .form-row {
            display: flex;
            gap: 15px;
        }

        input, select {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            font-size: 1rem;
            transition: border-color 0.3s ease;
            background: rgba(255, 255, 255, 0.9);
        }

        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .notification-settings {
            background: rgba(255, 255, 255, 0.8);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
        }

        .notification-settings h4 {
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.2rem;
        }

        .notification-option {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        }

        .notification-option:last-child {
            border-bottom: none;
        }

        .toggle-switch {
            position: relative;
            width: 50px;
            height: 25px;
            background: #ccc;
            border-radius: 25px;
            cursor: pointer;
            transition: background 0.3s ease;
        }

        .toggle-switch.active {
            background: linear-gradient(135deg, #4CAF50, #8BC34A);
        }

        .toggle-switch::before {
            content: '';
            position: absolute;
            top: 2px;
            left: 2px;
            width: 21px;
            height: 21px;
            background: white;
            border-radius: 50%;
            transition: transform 0.3s ease;
        }

        .toggle-switch.active::before {
            transform: translateX(25px);
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }

        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }

        .stat-label {
            color: #7f8c8d;
            font-size: 0.9rem;
        }

        .log-container {
            height: 400px;
            overflow-y: auto;
            background: rgba(0, 0, 0, 0.05);
            border-radius: 15px;
            padding: 20px;
            font-family: 'Courier New', monospace;
        }

        .log-entry {
            margin-bottom: 10px;
            padding: 10px;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }

        .log-timestamp {
            color: #7f8c8d;
            font-size: 0.9rem;
            font-weight: bold;
        }

        .alert-banner {
            background: linear-gradient(135deg, #FF6B6B, #FF8E8E);
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: none;
            align-items: center;
            gap: 10px;
        }

        .alert-banner.show {
            display: flex;
        }

        .alert-icon {
            font-size: 1.5rem;
        }

        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .main-header {
                padding: 20px;
            }
            
            .main-header h1 {
                font-size: 2rem;
            }
            
            .grid {
                grid-template-columns: 1fr;
            }
            
            .tabs {
                flex-direction: column;
                gap: 5px;
            }
            
            .tab {
                width: 100%;
            }
            
            .system-status {
                flex-direction: column;
            }
            
            .button-group {
                flex-direction: column;
            }
            
            .form-row {
                flex-direction: column;
            }
            
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        @media (max-width: 480px) {
            .stats-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Alert Banner -->
        <div class="alert-banner" id="alert-banner">
            <span class="alert-icon">⚠️</span>
            <span id="alert-message">Medication reminder: Time to take your pills!</span>
        </div>

        <!-- Main Header -->
        <div class="main-header">
            <h1>Smart Medication Adherence System</h1>
            <p class="subtitle">Automated Pill Dispenser with Smart Notifications</p>
            
            <div class="system-status">
                <div class="status-card">
                    <span class="status-indicator pulse" id="system-status-indicator"></span>
                    <span id="system-status-text">Loading...</span>
                </div>
                <div class="status-card">
                    <span>🕐</span>
                    <span id="current-time">Loading...</span>
                </div>
                <div class="status-card">
                    <span>📱</span>
                    <span id="notification-status">Notifications Active</span>
                </div>
            </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="tabs">
            <div class="tab active" data-tab="dashboard">📊 Dashboard</div>
            <div class="tab" data-tab="medication">💊 Medication</div>
            <div class="tab" data-tab="notifications">🔔 Notifications</div>
            <div class="tab" data-tab="system">⚙️ System</div>
            <div class="tab" data-tab="logs">📋 Logs</div>
        </div>

        <!-- Dashboard Tab -->
        <div class="tab-content active" id="dashboard">
            <!-- Statistics -->
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number" id="adherence-rate">95%</div>
                    <div class="stat-label">Adherence Rate</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="doses-taken">28</div>
                    <div class="stat-label">Doses Taken</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="missed-doses">2</div>
                    <div class="stat-label">Missed Doses</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="streak-days">7</div>
                    <div class="stat-label">Current Streak</div>
                </div>
            </div>

            <!-- Compartments Overview -->
<div class="card">
    <h2>Pill Compartments Status</h2>
    <div class="grid">

        <!-- Compartment 1 -->
        <div class="compartment">
            <div class="compartment-header">
                <h3>Compartment 1</h3>
               
            </div>
            <div class="medication-info">
                <p><strong>Medication:</strong> <span id="compartment1-medication">Morning Pills</span></p>
                <p><strong>Dosage:</strong> <span id="compartment1-dosage">2 tablets</span></p>
                <p><strong>Scheduled Times:</strong> <span id="compartment1-times">Unknown</span></p>
                <p><strong>Status:</strong> <span id="compartment1-taken">Waiting for Medication</span></p>
                <div class="adherence-indicator">
                    
                   
                </div>
            </div>
            <div class="button-group">
                <button onclick="openCompartment(1)" class="btn-success">Open</button>
                <button onclick="closeCompartment(1)" class="btn-danger">Close</button>
            </div>
        </div>

        <!-- Compartment 2 -->
        <div class="compartment">
            <div class="compartment-header">
                <h3>Compartment 2</h3>
                
            </div>
            <div class="medication-info">
                <p><strong>Medication:</strong> <span id="compartment2-medication">Evening Pills</span></p>
                <p><strong>Dosage:</strong> <span id="compartment2-dosage">1 tablet</span></p>
                <p><strong>Scheduled Times:</strong> <span id="compartment2-times">Unknown</span></p>
                <p><strong>Status:</strong> <span id="compartment2-taken">Waiting for Medication</span></p>
                <div class="adherence-indicator">
                
                </div>
            </div>
            <div class="button-group">
                <button onclick="openCompartment(2)" class="btn-success">Open</button>
                <button onclick="closeCompartment(2)" class="btn-danger">Close</button>
            </div>
        </div>

    </div>


                
                <div class="button-group" style="margin-top: 30px;">
                    <button id="system-toggle-btn" onclick="toggleSystem()" class="btn-primary">Start System</button>
                    <button onclick="testBuzzer()" class="btn-warning">Test Buzzer</button>
                    <button onclick="testNotification()" class="btn-primary">Test Notification</button>
                </div>
            </div>
        </div>

        <!-- Medication Settings Tab -->
        <div class="tab-content" id="medication">
            <div class="card">
                <h2>Medication Schedule Configuration</h2>
                <div class="grid">
                    <div class="compartment">
                        <h3>Compartment 1 Settings</h3>
                        <div class="form-group">
                            <label>Medication Name</label>
                            <input type="text" id="comp1-medication" placeholder="e.g., Aspirin">
                        </div>
                        <div class="form-group">
                            <label>Dosage</label>
                            <input type="text" id="comp1-dosage" placeholder="e.g., 2 tablets">
                        </div>
                        <div class="form-group">
                            <label>Time Slot 1</label>
                            <div class="form-row">
                                <input type="number" id="comp1-slot1-hour" min="0" max="23" placeholder="Hour">
                                <input type="number" id="comp1-slot1-minute" min="0" max="59" placeholder="Minute">
                            </div>
                        </div>
                        <div class="form-group">
                            <label>Time Slot 2</label>
                            <div class="form-row">
                                <input type="number" id="comp1-slot2-hour" min="0" max="23" placeholder="Hour">
                                <input type="number" id="comp1-slot2-minute" min="0" max="59" placeholder="Minute">
                            </div>
                        </div>
                        <div class="button-group">
                            <button onclick="setMedicationTime(1, 1)" class="btn-primary">Set Slot 1</button>
                            <button onclick="setMedicationTime(1, 2)" class="btn-primary">Set Slot 2</button>
                        </div>
                    </div>
                    
                    <div class="compartment">
                        <h3>Compartment 2 Settings</h3>
                        <div class="form-group">
                            <label>Medication Name</label>
                            <input type="text" id="comp2-medication" placeholder="e.g., Vitamin D">
                        </div>
                        <div class="form-group">
                            <label>Dosage</label>
                            <input type="text" id="comp2-dosage" placeholder="e.g., 1 tablet">
                        </div>
                        <div class="form-group">
                            <label>Time Slot 1</label>
                            <div class="form-row">
                                <input type="number" id="comp2-slot1-hour" min="0" max="23" placeholder="Hour">
                                <input type="number" id="comp2-slot1-minute" min="0" max="59" placeholder="Minute">
                            </div>
                        </div>
                        <div class="form-group">
                            <label>Time Slot 2</label>
                            <div class="form-row">
                                <input type="number" id="comp2-slot2-hour" min="0" max="23" placeholder="Hour">
                                <input type="number" id="comp2-slot2-minute" min="0" max="59" placeholder="Minute">
                            </div>
                        </div>
                        <div class="button-group">
                            <button onclick="setMedicationTime(2, 1)" class="btn-primary">Set Slot 1</button>
                            <button onclick="setMedicationTime(2, 2)" class="btn-primary">Set Slot 2</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Notifications Tab -->
        <div class="tab-content" id="notifications">
            <div class="card">
                <h2>Notification Settings</h2>
                <div class="notification-settings">
                    <h4>Alert Preferences</h4>
                    
                    <div class="notification-option">
                        <span>Audio Buzzer Alerts</span>
                        <div class="toggle-switch active" id="buzzer-toggle"></div>
                    </div>
                    
                    <div class="notification-option">
                        <span>Visual Notifications</span>
                        <div class="toggle-switch active" id="visual-toggle"></div>
                    </div>
                    
                    <div class="notification-option">
                        <span>SMS Notifications</span>
                        <div class="toggle-switch" id="sms-toggle"></div>
                    </div>
                    
                    <div class="notification-option">
                        <span>Email Alerts</span>
                        <div class="toggle-switch" id="email-toggle"></div>
                    </div>
                    
                    <div class="notification-option">
                        <span>Missed Dose Reminders</span>
                        <div class="toggle-switch active" id="missed-toggle"></div>
                    </div>
                </div>
                
                <div class="form-group">
                    <label>Reminder Frequency (minutes after missed dose)</label>
                    <select id="reminder-frequency">
                        <option value="5">5 minutes</option>
                        <option value="10" selected>10 minutes</option>
                        <option value="15">15 minutes</option>
                        <option value="30">30 minutes</option>
                        <option value="60">1 hour</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Emergency Contact Phone</label>
                    <input type="tel" id="emergency-contact" placeholder="+1 234 567 8900">
                </div>
                
                <div class="form-group">
                    <label>Emergency Contact Email</label>
                    <input type="email" id="emergency-email" placeholder="caregiver@example.com">
                </div>
                
                <button onclick="saveNotificationSettings()" class="btn-success">Save Settings</button>
            </div>
        </div>

        <!-- System Settings Tab -->
        <div class="tab-content" id="system">
            <div class="card">
                <h2>System Configuration</h2>
                
                <div class="form-group">
                    <label>System Date</label>
                    <input type="date" id="rtc-date">
                </div>
                
                <div class="form-group">
                    <label>System Time</label>
                    <input type="time" id="rtc-time" step="1">
                </div>
                
                <button onclick="setRTCTime()" class="btn-primary">Update System Time</button>
                
                <div class="notification-settings" style="margin-top: 30px;">
                    <h4>Device Settings</h4>
                    
                    <div class="form-group">
                        <label>Buzzer Volume</label>
                        <input type="range" id="buzzer-volume" min="0" max="100" value="75">
                        <span id="volume-display">75%</span>
                    </div>
                    
                    <div class="form-group">
                        <label>LED Brightness</label>
                        <input type="range" id="led-brightness" min="0" max="100" value="80">
                        <span id="brightness-display">80%</span>
                    </div>
                    
                    <div class="form-group">
                        <label>Auto-Close Compartment (seconds)</label>
                        <select id="auto-close-time">
                            <option value="30">30 seconds</option>
                            <option value="60" selected>1 minute</option>
                            <option value="120">2 minutes</option>
                            <option value="300">5 minutes</option>
                            <option value="0">Never</option>
                        </select>
                    </div>
                    
                    <button onclick="saveSystemSettings()" class="btn-success">Save Settings</button>
                </div>
            </div>
        </div>

        <!-- Logs Tab -->
        <div class="tab-content" id="logs">
            <div class="card">
                <h2>System Activity Logs</h2>
                <div class="button-group" style="margin-bottom: 20px;">
                    <button onclick="refreshLogs()" class="btn-primary">Refresh</button>
                    <button onclick="exportLogs()" class="btn-warning">Export</button>
                    <button onclick="clearLogs()" class="btn-danger">Clear Logs</button>
                </div>
                <div class="log-container" id="system-logs">
                    <div class="log-entry">
                        <div class="log-timestamp">2024-06-10 14:30:15</div>
                        <div>System initialized successfully</div>
                    </div>
                    <div class="log-entry">
                        <div class="log-timestamp">2024-06-10 14:25:03</div>
                        <div>Compartment 1 opened for scheduled medication</div>
                    </div>
                    <div class="log-entry">
                        <div class="log-timestamp">2024-06-10 14:25:45</div>
                        <div>Medication taken from Compartment 1</div>
                    </div>
                    <div class="log-entry">
                        <div class="log-timestamp">2024-06-10 14:26:00</div>
                        <div>Compartment 1 closed automatically</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Your existing JavaScript code will go here
        // I'm preserving the original structure and just adding minimal JS for UI interactions
        
        // Tab switching functionality
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                
                tab.classList.add('active');
                const tabId = tab.getAttribute('data-tab');
                document.getElementById(tabId).classList.add('active');
            });
        });

        // Toggle switches for notifications
        document.querySelectorAll('.toggle-switch').forEach(toggle => {
            toggle.addEventListener('click', () => {
                toggle.classList.toggle('active');
            });
        });

        // Volume and brightness sliders
        document.getElementById('buzzer-volume').addEventListener('input', (e) => {
            document.getElementById('volume-display').textContent = e.target.value + '%';
        });

        document.getElementById('led-brightness').addEventListener('input', (e) => {
            document.getElementById('brightness-display').textContent = e.target.value + '%';
        });

        // Initialize date and time inputs with current values
        function initializeDateTimeInputs() {
            const now = new Date();
            const dateStr = now.toISOString().split('T')[0];
            const timeStr = now.toTimeString().split(' ')[0];
            
            document.getElementById('rtc-date').value = dateStr;
            document.getElementById('rtc-time').value = timeStr;
        }

        // Alert banner functions
        function showAlert(message, type = 'warning') {
            const banner = document.getElementById('alert-banner');
            const messageEl = document.getElementById('alert-message');
            messageEl.textContent = message;
            banner.classList.add('show');
            
            // Auto-hide after 5 seconds
            setTimeout(() => {
                banner.classList.remove('show');
            }, 5000);
        }

        function hideAlert() {
            document.getElementById('alert-banner').classList.remove('show');
        }

        // Placeholder functions for new features (you can connect these to your existing API)
        function testNotification() {
            showAlert('Test notification sent successfully!');
        }

        function saveNotificationSettings() {
            showAlert('Notification settings saved successfully!');
        }

        function saveSystemSettings() {
            showAlert('System settings saved successfully!');
        }

        function refreshLogs() {
            // Your existing fetchStatus() function can be called here
            showAlert('Logs refreshed successfully!');
        }

        function exportLogs() {
            showAlert('Logs exported successfully!');
        }

        function clearLogs() {
            if (confirm('Are you sure you want to clear all logs?')) {
                document.getElementById('system-logs').innerHTML = '<div class="log-entry"><div class="log-timestamp">Logs cleared</div></div>';
                showAlert('Logs cleared successfully!');
            }
        }

        // Initialize the page
        document.addEventListener('DOMContentLoaded', () => {
            initializeDateTimeInputs();
            
            // You can call your existing init() function here
            // init();
        });

        // Click handler for alert banner close
        document.getElementById('alert-banner').addEventListener('click', hideAlert);
                // Authentication credentials
        const username = 'admin';
        const password = 'password';

        // Global variables
        let systemRunning = false;
        let updateInterval;
        let authHeader = 'Basic ' + btoa(username + ':' + password);

        // Tab switching
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                
                tab.classList.add('active');
                const tabId = tab.getAttribute('data-tab');
                document.getElementById(tabId).classList.add('active');
            });
        });

        // Fetch system status
        async function fetchStatus() {
            try {
                const response = await fetch('/api/status');
                if (!response.ok) {
                    throw new Error('Failed to fetch status');
                }
                const data = await response.json();
                updateUI(data);
            } catch (error) {
                console.error('Error fetching status:', error);
            }
        }

        // Update UI with status data
        function updateUI(data) {
            // Update system status
            systemRunning = data.system_running;
            const statusIndicator = document.getElementById('system-status-indicator');
            const statusText = document.getElementById('system-status-text');
            const systemToggleBtn = document.getElementById('system-toggle-btn');
            
            if (systemRunning) {
                statusIndicator.className = 'status-indicator status-on';
                statusText.textContent = 'System Running';
                systemToggleBtn.textContent = 'Stop System';
                systemToggleBtn.className = 'danger';
            } else {
                statusIndicator.className = 'status-indicator status-off';
                statusText.textContent = 'System Stopped';
                systemToggleBtn.textContent = 'Start System';
                systemToggleBtn.className = 'success';
            }
            
            // Update current time
            document.getElementById('current-time').textContent = data.rtc_time;
            
            // Update compartment 1 info
            document.getElementById('compartment1-times').textContent = 
                `${data.medication_times[0][0][0].toString().padStart(2, '0')}:${data.medication_times[0][0][1].toString().padStart(2, '0')} & ${data.medication_times[0][1][0].toString().padStart(2, '0')}:${data.medication_times[0][1][1].toString().padStart(2, '0')}`;
            document.getElementById('compartment1-taken').textContent = data.medication_taken[0] ? 'Medication Taken' : 'Waiting for Medication';
            document.getElementById('compartment1-status').textContent = data.compartment_open[0] ? 'Open' : 'Closed';
            
            // Update compartment 2 info
            document.getElementById('compartment2-times').textContent = 
                `${data.medication_times[1][0][0].toString().padStart(2, '0')}:${data.medication_times[1][0][1].toString().padStart(2, '0')} & ${data.medication_times[1][1][0].toString().padStart(2, '0')}:${data.medication_times[1][1][1].toString().padStart(2, '0')}`;
            document.getElementById('compartment2-taken').textContent = data.medication_taken[1] ? 'Medication Taken' : 'Waiting for Medication';
            document.getElementById('compartment2-status').textContent = data.compartment_open[1] ? 'Open' : 'Closed';
            
            // Update logs
            const logsContainer = document.getElementById('system-logs');
            logsContainer.innerHTML = '';
            data.system_messages.forEach(msg => {
                const logEntry = document.createElement('div');
                logEntry.className = 'log-entry';
                logEntry.innerHTML = `<span class="log-timestamp">${msg.timestamp}</span> ${msg.message}`;
                logsContainer.appendChild(logEntry);
            });
            
            // Auto-scroll logs to bottom
            logsContainer.scrollTop = logsContainer.scrollHeight;
        }

        // Toggle system (start/stop)
        async function toggleSystem() {
            try {
                const endpoint = systemRunning ? '/api/stop_system' : '/api/start_system';
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': authHeader
                    }
                });
                
                if (!response.ok) {
                    throw new Error('Failed to toggle system');
                }
                
                fetchStatus();
            } catch (error) {
                console.error('Error toggling system:', error);
                alert('Error: ' + error.message);
            }
        }

        // Open compartment
        async function openCompartment(compartment) {
            try {
                const response = await fetch('/api/open_compartment', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': authHeader
                    },
                    body: JSON.stringify({ compartment })
                });
                
                if (!response.ok) {
                    throw new Error('Failed to open compartment');
                }
                
                setTimeout(fetchStatus, 1000);
            } catch (error) {
                console.error('Error opening compartment:', error);
                alert('Error: ' + error.message);
            }
        }

        // Close compartment
        async function closeCompartment(compartment) {
            try {
                const response = await fetch('/api/close_compartment', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': authHeader
                    },
                    body: JSON.stringify({ compartment })
                });
                
                if (!response.ok) {
                    throw new Error('Failed to close compartment');
                }
                
                setTimeout(fetchStatus, 1000);
            } catch (error) {
                console.error('Error closing compartment:', error);
                alert('Error: ' + error.message);
            }
        }

        // Test buzzer
        async function testBuzzer() {
            try {
                const response = await fetch('/api/test_buzzer', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': authHeader
                    }
                });
                
                if (!response.ok) {
                    throw new Error('Failed to test buzzer');
                }
            } catch (error) {
                console.error('Error testing buzzer:', error);
                alert('Error: ' + error.message);
            }
        }

        // Set medication time
        async function setMedicationTime(compartment, slot) {
            try {
                const hourInput = document.getElementById(`comp${compartment}-slot${slot}-hour`);
                const minuteInput = document.getElementById(`comp${compartment}-slot${slot}-minute`);
                
                const hour = parseInt(hourInput.value);
                const minute = parseInt(minuteInput.value);
                
                if (isNaN(hour) || isNaN(minute) || hour < 0 || hour > 23 || minute < 0 || minute > 59) {
                    alert('Please enter valid hour (0-23) and minute (0-59)');
                    return;
                }
                
                const response = await fetch('/api/set_medication_time', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': authHeader
                    },
                    body: JSON.stringify({ compartment, slot, hour, minute })
                });
                
                if (!response.ok) {
                    throw new Error('Failed to set medication time');
                }
                
                const result = await response.json();
                if (result.success) {
                    alert(result.message);
                    fetchStatus();
                } else {
                    alert('Error: ' + result.message);
                }
            } catch (error) {
                console.error('Error setting medication time:', error);
                alert('Error: ' + error.message);
            }
        }

        // Set RTC time
        async function setRTCTime() {
            try {
                const dateInput = document.getElementById('rtc-date');
                const timeInput = document.getElementById('rtc-time');
                
                if (!dateInput.value || !timeInput.value) {
                    alert('Please enter both date and time');
                    return;
                }
                
                const dateObj = new Date(dateInput.value + 'T' + timeInput.value);
                
                if (isNaN(dateObj.getTime())) {
                    alert('Please enter valid date and time');
                    return;
                }
                
                const year = dateObj.getFullYear();
                const month = dateObj.getMonth() + 1;
                const day = dateObj.getDate();
                const hour = dateObj.getHours();
                const minute = dateObj.getMinutes();
                const second = dateObj.getSeconds();
                
                const response = await fetch('/api/set_rtc_time', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': authHeader
                    },
                    body: JSON.stringify({ year, month, day, hour, minute, second })
                });
                
                if (!response.ok) {
                    throw new Error('Failed to set RTC time');
                }
                
                const result = await response.json();
                if (result.success) {
                    alert(result.message);
                    fetchStatus();
                } else {
                    alert('Error: ' + result.message);
                }
            } catch (error) {
                console.error('Error setting RTC time:', error);
                alert('Error: ' + error.message);
            }
        }

        // Initialize the page
        function init() {
            // Set current date and time in the RTC form
            const now = new Date();
            const dateStr = now.toISOString().split('T')[0];
            const timeStr = now.toTimeString().split(' ')[0];
            
            document.getElementById('rtc-date').value = dateStr;
            document.getElementById('rtc-time').value = timeStr;
            
            // Fetch initial status
            fetchStatus();
            
            // Set up periodic status updates
            updateInterval = setInterval(fetchStatus, 5000);
        }

        // Call init when the page loads
        window.addEventListener('load', init);
        
        // Clean up when the page unloads
        window.addEventListener('beforeunload', () => {
            clearInterval(updateInterval);
        });
    </script>
</body>
</html>
