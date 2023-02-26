from PyQt5.QtCore import pyqtSignal, QRunnable, QObject
from threading import Event
import serial
import rtmidi
import time


class Signals(QObject):
    CurrentKey = pyqtSignal(str)
    Log = pyqtSignal(str)
    Connected = pyqtSignal()
    Disconnected = pyqtSignal()


class StyloduinoMidiBridge(QRunnable):
    def __init__(self) -> None:
        super().__init__()
        self.signals = Signals()

        self.try_com = 2  # start trying to connect from COM2
        self.try_com_max = 20  # look for COM for x many times before giving up
        self.com_connected = False
        self.ser = None
        self.keys_clear = True
        self.key_hit = None  # only hit key once, until you lift the pen up
        self.running = True
        self.sleeping = False
        self.speaker_enabled = True

        self.midi = rtmidi.MidiOut()
        self.octave = 4
        self.velocity = 112

        # defined midi keys corresponding to styloduino's note range
        self.keys = [
            57, 58, 59, 60,
            61, 62, 63, 64,
            65, 66, 67, 68,
            69, 70, 71, 72,
            73, 74, 75, 76
        ]

        self.key_names = None
        self.update_keynames()

        self.init_midi()

    def update_keynames(self):
        self.key_names = [
            f"A{self.octave}", f"A#{self.octave}/Bb{self.octave}", f"B{self.octave}", f"C{self.octave+1}",
            f"C#{self.octave+1}/Db{self.octave+1}", f"D{self.octave+1}", f"D#{self.octave+1}/Eb{self.octave+1}", f"E{self.octave+1}",
            f"F{self.octave+1}", f"F#{self.octave+1}/Gb{self.octave+1}", f"G{self.octave+1}", f"G#4/Ab{self.octave+1}",
            f"A{self.octave+1}", f"A#{self.octave+1}/Bb{self.octave+1}", f"B{self.octave+1}", f"C{self.octave+2}",
            f"C#{self.octave+2}/Db{self.octave+2}", f"D{self.octave+2}", f"D#{self.octave+2}/Eb{self.octave+2}", f"E{self.octave+2}"
        ]

    def stop(self):
        self.running = False

    def set_sleeping(self, sleeping):
        self.sleeping = sleeping

    def toggle_onboard_speaker(self, on):
        if self.com_connected:
            if on:
                self.signals.Log.emit("Enabling on-board speaker...")
                for _ in range(3):
                    self.ser.write(str.encode('1'))
                    time.sleep(1)
                self.speaker_enabled = True
            else:
                self.signals.Log.emit("Disabling on-board speaker...")
                for _ in range(3):
                    self.ser.write(str.encode('0'))
                    time.sleep(1)
                self.signals.Log.emit(f"Connected to COM{self.try_com}")
                self.speaker_enabled = False

    def run(self):
        while self.running:
            if not self.sleeping:
                if self.com_connected:
                    self.signals.Log.emit(f"Connected to COM{self.try_com}")
                    try:
                        self.toggle_onboard_speaker(on=False)
                        self.init_communication()
                    except serial.SerialException:
                        self.signals.CurrentKey.emit("Disconnected")
                        self.signals.Disconnected.emit()
                        self.com_connected = False
                else:
                    self.init_serial()
                    time.sleep(2)
            else:
                if not self.speaker_enabled:
                    self.toggle_onboard_speaker(on=True)
                self.signals.Log.emit("Sleeping")
                time.sleep(2)

    def init_serial(self):
        while not self.com_connected and self.try_com < self.try_com_max:
            try:
                self.signals.Log.emit(f"Trying COM {self.try_com}.")
                self.ser = serial.Serial(f"COM{self.try_com}", 38400)
                self.com_connected = True
                self.signals.Log.emit(f"Connected to COM{self.try_com}")
                self.signals.Connected.emit()
                self.signals.CurrentKey.emit("Standby")
            except serial.SerialException:
                self.signals.Log.emit(f"Cannot connect to COM{self.try_com}.")
                self.try_com += 1
        if not self.com_connected:
            self.signals.Log.emit("No COM ports found. Retrying...")
            self.try_com = 2

    def init_midi(self):
        for idx, port in enumerate(self.midi.get_ports()):
            if "styloduino" in port:
                self.midi.open_port(idx)
                return
        self.signals.Log.emit("No midi port with name 'styloduino' found.")

    def init_communication(self):
        while not self.sleeping:
            data = int.from_bytes(self.ser.read(), "big")
            if data < 20:
                key = self.keys[data]
                if not self.key_hit == key:
                    if self.key_hit is not None:
                        self.midi.send_message([0x80, self.key_hit, 0])
                    self.keys_clear = False
                    self.midi.send_message([0x90, key, self.velocity])
                    self.signals.CurrentKey.emit(str(self.key_names[data]))
                    self.key_hit = key
            else:
                if not self.keys_clear:
                    for i in range(20):
                        self.midi.send_message([0x80, self.keys[i], 0])
                    self.keys_clear = True
                    self.key_hit = None
                    self.signals.CurrentKey.emit("Standby")
