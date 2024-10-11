# setup.py
EMAIL = ""  # Your email address for iClicker login
PASSWORD = ""  # Your password for iClicker login

# Class schedule: {'class_name': ('class_url', [days_of_week], time_of_day)}
# Days of the week: 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
# Time of day format: 'HH:MM' in 24-hour time format
CLASS_SCHEDULES = {
    # Example Class Entry
    'Class Name Here': (
        'https://example.com/course-link',  # Replace with the actual class URL
        ['Monday', 'Wednesday', 'Friday'],  # List days of the week the class is held
        ('09:00', '10:00')  # Replace with the class start and end time
    ),
    # Add more classes below as needed
}

POLL_RATE = 5  # Poll rate in seconds (how often to check for polls)
WAIT_JOIN = 5  # Time to wait for the "Join" button in seconds

