from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QHBoxLayout, QVBoxLayout, QSlider, QLabel, QTextEdit
from PySide6.QtCore import QTimer, Signal, Qt
from PySide6.QtGui import QColor, QTextCursor
from joystick_widget import Joystick
from dpad_widget import DirectionalPad
from ws_server import WSServer
import sys

class ServerWindow(QMainWindow):
    def __init__(self, max_speed_pwm=50, msg_interval_ms=200):
        super().__init__()
        
        self.max_speed_pwm = max_speed_pwm
        self.msg_interval_ms = msg_interval_ms
        self.connected = False
        
        self.init_ui()
        self.init_ws_server()
        self.start_timer()
    
    def init_ui(self):
        self.setWindowTitle("owenBot")
        self.setGeometry(100, 100, 600, 500)
        
        # central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)
        
        # joystick and dpad
        controllers_layout = QHBoxLayout()
        self.joystick = Joystick()
        controllers_layout.addWidget(self.joystick)
        self.dpad = DirectionalPad()
        controllers_layout.addWidget(self.dpad)
        layout.addLayout(controllers_layout, 0, 0)
        
        # speed slider
        slider_layout = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.max_speed_pwm)
        self.slider.setValue(0)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(5)
        slider_layout.addWidget(self.slider)
        self.slider_label = QLabel("0")
        self.slider_label.setMinimumWidth(30)
        slider_layout.addWidget(self.slider_label)
        self.slider.valueChanged.connect(self.update_slider_label)
        layout.addLayout(slider_layout, 1, 0)
        
        # status area
        self.client_label = QLabel("Client: None")
        layout.addWidget(self.client_label, 2, 0)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #c2c2c2;
                border: 1px solid #e3e3e3;
                border-radius: 5px;
                padding: 5px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                color: #000000;
            }
        """)
        layout.addWidget(self.log_text, 3, 0)
    
    def init_ws_server(self):
        self.ws_server = WSServer(port=9876)
        self.ws_server.client_connected.connect(self.on_client_connected)
        self.ws_server.client_disconnected.connect(self.on_client_disconnected)
        self.ws_server.message_sent.connect(self.on_message_sent)
        self.ws_server.message_received.connect(self.on_message_received)
    
    def start_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.send_data)
        self.timer.start(self.msg_interval_ms)
    
    def get_speeds_from_pos(self, x, y):
        # tank controls - swap the x assignments
        left_ratio, right_ratio = y - x, y + x
        max_raw = max(abs(left_ratio), abs(right_ratio))
        if max_raw > 1:
            left_ratio /= max_raw
            right_ratio /= max_raw
    
        left_pwm = int(left_ratio * self.slider.value())
        right_pwm = int(right_ratio * self.slider.value())
    
        return left_pwm, right_pwm
    
    def send_data(self):
        if not self.connected:
            return
        x, y = self.joystick.joystickPos()
        if x == 0 and y == 0:
            x, y = self.dpad.dpadPos()
        left_pwm, right_pwm = self.get_speeds_from_pos(x, y)
        self.ws_server.send_message(f"{left_pwm} {right_pwm}")
    
    def update_slider_label(self, value):
        percent = value / self.max_speed_pwm * 100.0
        self.slider_label.setText(f"{percent:.1f}%")
    
    def on_client_connected(self):
        self.client_label.setText(f"Client: Connected!")
        self.connected = True
        self.log(f"Client connected!")
    
    def on_client_disconnected(self):
        self.client_label.setText("Client: None")
        self.connected = False
        self.log(f"Client disconnected!")
    
    def on_message_sent(self, msg):
        self.log(f"Message sent ({msg=})")
    
    def on_message_received(self, msg):
        self.log(f"Message received ({msg=})")
    
    def log(self, message):
        self.log_text.append(f"[{self.get_timestamp()}] {message}")
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.log_text.setTextCursor(cursor)
    
    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ServerWindow()
    window.show()
    app.exec()