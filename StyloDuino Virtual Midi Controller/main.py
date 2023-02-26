from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThreadPool
from PyQt5.QtGui import QFontDatabase
from uilib.window import WindowContainer
from uilib.util import open_qt_resource
from application import MainWindow
from bridge import StyloduinoMidiBridge
from res import *
import sys


class Application(MainWindow):
    def __init__(self, p, width: int = 640, height: int = 480):
        super().__init__(p, width, height)
        self.bridge = StyloduinoMidiBridge()
        self.bridge.signals.Log.connect(self.detail_label.setText)
        self.bridge.signals.CurrentKey.connect(self.status_label.setText)
        self.bridge.signals.Connected.connect(lambda: self.toggle_button.setChecked(True))
        self.bridge.signals.Disconnected.connect(lambda: self.toggle_button.setChecked(False))

        self.thread_pool = QThreadPool(self)
        self.thread_pool.start(self.bridge)

        self.toggle_button.clicked.connect(lambda toggled: self.bridge.set_sleeping(False) if toggled else \
                                           self.bridge.set_sleeping(True))
        self.cleanupQueue.append(self.bridge.stop)

        self.octave_form.up_button.clicked.connect(self.octave_up)
        self.octave_form.down_button.clicked.connect(self.octave_down)
        self.velocity_form.up_button.clicked.connect(self.velocity_up)
        self.velocity_form.down_button.clicked.connect(self.velocity_down)
        
    def octave_up(self):
        if (self.bridge.octave + 1) < 10:
            for i in range(20):
                self.bridge.keys[i] = self.bridge.keys[i] + 12
            self.bridge.octave += 1
            self.bridge.update_keynames()
            print(self.bridge.octave)

    def octave_down(self):
        if (self.bridge.octave - 1 ) > -1:
            for i in range(20):
                self.bridge.keys[i] = self.bridge.keys[i] - 12
            self.bridge.octave -= 1
            self.bridge.update_keynames()
            print(self.bridge.octave)

    def velocity_up(self):
        if self.bridge.velocity + 1 < 128:
            self.bridge.velocity += 1

    def velocity_down(self):
        if self.bridge.velocity - 1 > 0:
            self.bridge.velocity -= 1


if __name__ == "__main__":
    app = QApplication(sys.argv)

    fontret = QFontDatabase.addApplicationFont(":/font/comfortaa.ttf")
    if fontret < 0:
        print("failed to load default font")

    wcon = WindowContainer(Application, width=900, height=550)
    wcon.setWindowTitle("StyloDuino-VMC")
    wcon.setStyleSheet(open_qt_resource(":/style/style.css"))
    wcon.show()
    sys.exit(app.exec_())