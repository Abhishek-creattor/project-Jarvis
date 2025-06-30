import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui import JarvisGUI

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion') # Use 'Fusion' style for better dark theme support

    # Set application icon (optional)
    # if os.path.exists('path/to/your/icon.png'):
    #     app.setWindowIcon(QIcon('path/to/your/icon.png'))

    jarvis_gui = JarvisGUI()
    jarvis_gui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()