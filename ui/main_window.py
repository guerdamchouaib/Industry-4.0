import cv2
from ultralytics import YOLO
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QDesktopWidget
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
from datetime import datetime
import os
from components.detection_history import DetectionHistory
from components.settings import AppSettings
from components.snapshot import SnapshotManager

# Load YOLOv8 model
model = YOLO(r'C:\Users\choua\Desktop\defectsdetection\defectsdetection\ui\best.pt')



class DefectDetectionApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize window properties
        self.setWindowTitle('Crimping Wires Defects Detection')
        self.setStyleSheet("background-color: #D3D3D3; color: #d3d3d3;")

        # Get screen size
        self.screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, self.screen.width(), self.screen.height())

        # Initialize settings, history, and snapshot manager
        self.settings = AppSettings()
        self.history = DetectionHistory()
        self.snapshot_manager = SnapshotManager()

        # Initialize UI and camera
        self.init_ui()
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Handle resize events
        self.installEventFilter(self)

    def init_ui(self):
        """Initialize the UI layout."""
        screen_width = self.screen.width()
        screen_height = self.screen.height()

        # Camera view setup
        self.camera_label = QLabel(self)
        self.camera_label.setFixedSize(int(screen_width * 0.75), int(screen_height * 0.7))
        self.camera_label.setStyleSheet("border: 2px solid #D3D3D3; border-radius: 10px; background-color: #C0C0C0;")
        self.camera_label.setAlignment(Qt.AlignCenter)

        # Result label
        self.result_label = QLabel('Result: N/A', self)
        self.result_label.setStyleSheet("color: #00cc99; font-size: 36px; font-weight: bold; background-color:  #708090; padding: 10px; border-radius: 10px;")
        self.result_label.setAlignment(Qt.AlignCenter)

        # Buttons
        self.btn_start = self.create_button('Start Detection', '#009688')
        self.btn_stop = self.create_button('Stop Detection', '#e74c3c')
        self.btn_snapshot = self.create_button('Capture Snapshot', '#f39c12')
        self.btn_record = self.create_button('Start Recording', '#2980b9')
        self.btn_settings = self.create_button('Settings', '#34495e')
        self.btn_history = self.create_button('Detection History', '#8e44ad')

        # Connect button actions
        self.btn_start.clicked.connect(self.start_detection)
        self.btn_stop.clicked.connect(self.stop_detection)
        self.btn_snapshot.clicked.connect(self.capture_snapshot)
        self.btn_record.clicked.connect(self.start_recording)
        self.btn_settings.clicked.connect(self.open_settings)
        self.btn_history.clicked.connect(self.open_history)

        # Layout configuration
        layout = QVBoxLayout()
        layout.addWidget(self.result_label)
        layout.addWidget(self.camera_label, alignment=Qt.AlignCenter)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_start)
        button_layout.addWidget(self.btn_stop)
        button_layout.addWidget(self.btn_snapshot)
        button_layout.addWidget(self.btn_record)
        button_layout.addWidget(self.btn_settings)
        button_layout.addWidget(self.btn_history)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def create_button(self, text, color):
        button = QPushButton(text, self)
        button.setStyleSheet(f"background-color: {color}; color: white; font-size: 20px; border-radius: 10px;")
        button.setFixedHeight(int(self.screen.height() * 0.08))
        button.setFixedWidth(int(self.screen.width() * 0.15))
        return button

    def start_detection(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(1)
            if not self.cap.isOpened():
                self.result_label.setText('Error: Cannot open camera')
                return
        self.timer.start(30)

    def stop_detection(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None
        self.camera_label.clear()
        self.result_label.setText('Result: N/A')

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            results = model.predict(source=frame)
            result = results[0]

            if result.boxes:
                for detection in result.boxes:
                    x1, y1, x2, y2 = map(int, detection.xyxy[0])
                    class_id = int(detection.cls[0])
                    label, color = ("NG", (255, 0, 0)) if class_id == 0 else ("OK", (0, 255, 0))
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                self.result_label.setText('Result: NG' if any(int(d.cls[0]) == 0 for d in result.boxes) else 'Result: OK')
            else:
                self.result_label.setText('Result: No Detection')

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            q_img = QImage(frame_rgb.data, w, h, ch * w, QImage.Format_RGB888)
            self.camera_label.setPixmap(QPixmap.fromImage(q_img))

    def capture_snapshot(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                self.snapshot_manager.save_snapshot(frame)
                self.result_label.setText('Snapshot Captured')

    def start_recording(self):
        if not self.snapshot_manager.recording:
            self.snapshot_manager.start_video_recording()
            self.result_label.setText('Recording Started')

    def open_settings(self):
        self.settings.show()

    def open_history(self):
        self.history.show()

    def closeEvent(self, event):
        if self.cap:
            self.cap.release()
        event.accept()




















