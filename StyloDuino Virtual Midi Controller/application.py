from uilib.window import Window
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSize, QVariantAnimation
from PyQt5.QtGui import QIcon, QColor


class TwoWaysButtonInputForm(QtWidgets.QWidget):
    def __init__(self, p, form_name):
        super().__init__(p)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.button_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.button_layout)
        
        self.up_button = QtWidgets.QPushButton(self)
        self.up_button.setFixedSize(48, 48)
        self.up_button.setIcon(QIcon(":/icons/up.svg"))
        self.up_button.setIconSize(QSize(48, 48))
        self.down_button = QtWidgets.QPushButton(self)
        self.down_button.setFixedSize(48, 48)
        self.down_button.setIcon(QIcon(":/icons/down.svg"))
        self.down_button.setIconSize(QSize(48, 48))

        self.button_layout.addWidget(self.up_button)
        self.button_layout.addWidget(self.down_button)

        self.form_label = QtWidgets.QLabel(form_name, self)
        self.main_layout.addWidget(self.form_label, alignment=Qt.AlignCenter)


class AnimatedButton(QtWidgets.QPushButton):
    def __init__(self, p=None):
        super().__init__(p)

        self.shadowAnim = QVariantAnimation(self)
        self.shadowAnim.setDuration(100)

        self.offsetAnim = QVariantAnimation(self)
        self.offsetAnim.setDuration(100)

        self.dropShadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.dropShadow.setColor(QColor(0, 0, 0, 45))
        self.dropShadow.setOffset(0, 20)
        self.dropShadow.setBlurRadius(64)
        self.setGraphicsEffect(self.dropShadow)

    def mousePressEvent(self, e) -> None:
        self.shadowAnim.stop()
        self.shadowAnim.setStartValue(64)
        self.shadowAnim.setEndValue(0)
        self.shadowAnim.valueChanged.connect(self.dropShadow.setBlurRadius)
        self.shadowAnim.start()

        self.offsetAnim.stop()
        self.offsetAnim.setStartValue(20)
        self.offsetAnim.setEndValue(1)
        self.offsetAnim.valueChanged.connect(self.dropShadow.setYOffset)
        self.offsetAnim.start()
        QtWidgets.QPushButton.mousePressEvent(self, e)

    def mouseReleaseEvent(self, e) -> None:
        self.shadowAnim.stop()
        self.shadowAnim.setStartValue(1)
        self.shadowAnim.setEndValue(64)
        self.shadowAnim.valueChanged.connect(self.dropShadow.setBlurRadius)
        self.shadowAnim.start()

        self.offsetAnim.stop()
        self.offsetAnim.setStartValue(0)
        self.offsetAnim.setEndValue(20)
        self.offsetAnim.valueChanged.connect(self.dropShadow.setYOffset)
        self.offsetAnim.start()
        QtWidgets.QPushButton.mouseReleaseEvent(self, e)


class MainWindow(Window):
    def __init__(self, p, width: int = 640, height: int = 480):
        super().__init__(p, width, height)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.header_layout = QtWidgets.QHBoxLayout()
        self.content_layout = QtWidgets.QVBoxLayout()
        self.controls_layout = QtWidgets.QHBoxLayout()
        self.footer_layout = QtWidgets.QHBoxLayout()
        
        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addLayout(self.content_layout)
        self.main_layout.addSpacing(45)
        self.main_layout.addLayout(self.footer_layout)

        self.main_layout.setContentsMargins(18, 8, 18, 16)
        self.header_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.header_layout.setSpacing(2)
        self.content_layout.setAlignment(Qt.AlignCenter)
        self.controls_layout.setAlignment(Qt.AlignCenter)
        self.footer_layout.setAlignment(Qt.AlignBottom)

        # header

        self.brand_label = QtWidgets.QLabel("StyloDuino", self)
        self.brand_label.setObjectName("brand_label")
        self.descr_label = QtWidgets.QLabel("Virtual Midi Controller", self)
        self.descr_label.setObjectName("descr_label")

        self.header_layout.addWidget(self.brand_label)
        self.header_layout.addWidget(self.descr_label)

        # content

        self.status_label = QtWidgets.QLabel("Disconnected", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setObjectName("status_label")

        self.content_layout.addWidget(self.status_label, alignment=Qt.AlignVCenter, stretch=5)
        self.content_layout.addSpacing(-100)
        self.content_layout.addLayout(self.controls_layout)

        # controls

        self.toggle_button = AnimatedButton(self)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(True)
        self.toggle_button.setObjectName("toggle_button")
        self.toggle_button.setFixedSize(100, 100)
        self.toggle_button.setIcon(QIcon(":/icons/power.svg"))
        self.toggle_button.setIconSize(QSize(64, 64))
        self.toggle_button.setToolTip("Toggle on/off midi controller")

        self.velocity_form = TwoWaysButtonInputForm(self, "velocity")
        self.octave_form = TwoWaysButtonInputForm(self, "octave")

        self.controls_layout.addWidget(self.velocity_form)
        self.controls_layout.addSpacing(80)
        self.controls_layout.addWidget(self.toggle_button)
        self.controls_layout.addSpacing(80)
        self.controls_layout.addWidget(self.octave_form)

        # footer

        self.detail_label = QtWidgets.QLabel(self)
        self.copyright_label = QtWidgets.QLabel("© 2023 Kevin Putra Satrianto", self)
        
        self.footer_layout.addWidget(self.detail_label, alignment=Qt.AlignLeft)
        self.footer_layout.addWidget(self.copyright_label, alignment=Qt.AlignRight)
        
        self.raiseBaseWidget()
