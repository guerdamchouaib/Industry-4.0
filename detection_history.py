from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class DetectionHistory(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Detection History')
        self.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()

        self.info_label = QLabel('No detections recorded yet.', self)
        layout.addWidget(self.info_label)

        self.setLayout(layout)
