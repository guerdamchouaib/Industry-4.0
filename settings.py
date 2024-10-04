from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class AppSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Settings')
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        self.info_label = QLabel('Settings Panel (You can add more configurations)', self)
        layout.addWidget(self.info_label)

        self.setLayout(layout)
