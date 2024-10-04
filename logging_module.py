import os
from datetime import datetime

class Logger:
    def __init__(self):
        if not os.path.exists('./assets/log_files'):
            os.makedirs('./assets/log_files')

    def log_detection(self, detection_info):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(f"./assets/log_files/detections_log.txt", "a") as log_file:
            log_file.write(f"{timestamp} - {detection_info}\n")
