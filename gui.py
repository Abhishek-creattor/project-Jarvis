from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
import sys
import numpy as np
from features.voice import speak, listen
from features.ai import ask_ai

class VoiceThread(QThread):
    command_received = pyqtSignal(str)
    listening_status = pyqtSignal(bool)
    
    def run(self):
        self.listening_status.emit(True)
        command = listen()
        self.command_received.emit(command)
        self.listening_status.emit(False)

class WaveformWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.points = []
        self.active = False
        
        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateWaveform)
        self.timer.start(50)  # 20 FPS
        
    def setActive(self, active):
        self.active = active
        if not active:
            self.points = []
            self.update()
    
    def updateWaveform(self):
        if self.active:
            # Generate smooth waveform points
            num_points = 100
            x = np.linspace(0, 2*np.pi, num_points)
            amplitude = 0.3 if self.active else 0
            y = amplitude * np.sin(x + self.timer.interval() / 50) * np.random.uniform(0.5, 1.5, num_points)
            self.points = list(zip(x, y))
            self.update()
    
    def paintEvent(self, event):
        if not self.points:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Set up the coordinate system
        painter.translate(self.width()/2, self.height()/2)
        painter.scale(self.width()/(2*np.pi), self.height()/2)
        
        # Draw waveform
        pen = QPen(QColor(0, 255, 255) if self.active else QColor(100, 100, 100))
        pen.setWidth(0)
        painter.setPen(pen)
        
        path_points = [(x, y) for x, y in self.points]
        for i in range(len(path_points)-1):
            painter.drawLine(
                path_points[i][0], path_points[i][1],
                path_points[i+1][0], path_points[i+1][1]
            )

class JarvisGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.voice_thread = None
        
    def initUI(self):
        self.setWindowTitle('Jarvis AI Assistant')
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e1e; }
            QLabel { color: #ffffff; font-size: 14px; }
            QPushButton {
                background-color: #0d47a1;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #1565c0; }
            QPushButton:pressed { background-color: #0a3d91; }
            QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
        """)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel('Jarvis AI Assistant')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet('font-size: 24px; font-weight: bold; color: #ffffff; margin-bottom: 20px;')
        layout.addWidget(title)
        
        # Waveform visualization
        self.waveform = WaveformWidget()
        self.waveform.setMinimumHeight(100)
        layout.addWidget(self.waveform)
        
        # Status label
        self.status_label = QLabel('Ready')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Response display
        self.response_display = QTextEdit()
        self.response_display.setReadOnly(True)
        self.response_display.setMinimumHeight(200)
        layout.addWidget(self.response_display)
        
        # Listen button
        self.listen_button = QPushButton('Start Listening')
        self.listen_button.clicked.connect(self.toggleListening)
        layout.addWidget(self.listen_button)
        
        # Set window size
        self.setMinimumSize(500, 600)
        
    def toggleListening(self):
        if self.voice_thread is None or not self.voice_thread.isRunning():
            self.startListening()
        
    def startListening(self):
        self.voice_thread = VoiceThread()
        self.voice_thread.command_received.connect(self.handleCommand)
        self.voice_thread.listening_status.connect(self.updateListeningStatus)
        self.voice_thread.start()
        
    def handleCommand(self, command):
        if command:
            self.response_display.append(f'You: {command}')
            if 'stop' in command.lower():
                response = 'Goodbye!'
                self.response_display.append(f'Jarvis: {response}')
                speak(response)
                QTimer.singleShot(2000, self.close)
            else:
                response = ask_ai(command)
                self.response_display.append(f'Jarvis: {response}')
                speak(response)
        
    def updateListeningStatus(self, is_listening):
        self.waveform.setActive(is_listening)
        if is_listening:
            self.status_label.setText('Listening...')
            self.listen_button.setEnabled(False)
        else:
            self.status_label.setText('Ready')
            self.listen_button.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for better dark theme support
    
    window = JarvisGUI()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()