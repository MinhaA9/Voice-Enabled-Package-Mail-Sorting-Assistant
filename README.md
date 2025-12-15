Voice-Enabled Package & Mail Sorting Assistant
==============================================

Description:
------------
This project is a voice-enabled system for managing package and mail sorting. 
It supports both manual and voice modes, reduces human errors, and automatically 
logs data to provide real-time statistics and insights.

Project Structure:
------------------

databases/
    - employee.csv         # Employee information
    - mail_data.csv        # Mail-related data
    - mail_department.csv  # Department information for mail
    - package_data.csv     # Package-related data

images/
    - dashboard_icon.png
    - home_icon.png
    - mic_icon.png

Backend Files:
--------------
- backend_dashboard.py           : Creates bar graphs for visualization
- backend_datalayer.py           : Reads CSV files and creates dictionaries for faster access
- backend_mail_package.py        : Contains classes:
      * Lookup_Employee_Info
      * Mail_Process
      * Package_Process
- backend_package_pickup_email.py: Handles sending emails to employees for package pickup (email sending currently disabled for security)
- backend_voicemode.py           : Handles voice input/output using Whisper and Vosk models
- container_manager.py           : Enables/disables app container

Frontend Files:
---------------
- frontend_body.py               : Contains three frames: title, navigation, and main
- frontend_dashboard.py          : Displays graphs and statistics
- frontend_lookup_employee.py    : Interactive lookup for employee information
- frontend_mail.py               : Processes mail workflow, shows actions, employee, and department info
- frontend_navigation_items.py   : Left-side navigation bar with buttons for different purposes
- frontend_package.py            : Worker input for package processing, autofills employee info, and handles pickup notifications
- frontend_startpage.py          : Loads databases when starting the app
- frontend_voicemode.py          : Displays voice input and text output in the app

Main File:
----------
- main.py                        : Entry point to run the entire application

Libraries / Dependencies:
-------------------------
- pandas
- matplotlib
- calendar
- time
- datetime
- threading
- smtplib
- email.message
- pyaudio
- wave
- os
- vosk
- json
- pyttsx3
- whisper
- customtkinter
- matplotlib.backends.backend_tkagg
- PIL (Pillow)
- rapidfuzz

How to Run:
-----------
1. Ensure all required libraries are installed (use pip to install missing packages).
2. Run the application by executing:

   python main.py

This will load the start page, initialize the databases, and launch the full app with 
both manual and voice-enabled modes.

Notes:
------
- Email sending functionality is currently disabled for security reasons.
- Voice mode requires a functioning microphone and appropriate Vosk/Whisper models.
- The application automatically logs activities and generates visual statistics.

Author:
-------
Your Name / Your Contact Info
