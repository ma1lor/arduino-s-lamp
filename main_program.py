import sys
import serial
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton
from speech_recognition_code import recognition


class SerialPortExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.serial_port = None

    def initUI(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)

        self.input_line = QLineEdit(self)
        self.layout.addWidget(self.input_line)

        
        self.open_button = QPushButton('Открыть порт', self)
        self.open_button.clicked.connect(self.openSerialPort)
        self.layout.addWidget(self.open_button)

        self.close_button = QPushButton('Закрыть порт', self)
        self.close_button.clicked.connect(self.closeSerialPort)
        self.layout.addWidget(self.close_button)

        self.send_button = QPushButton('Отправить', self)
        self.send_button.clicked.connect(self.sendData)
        self.layout.addWidget(self.send_button)

        self.voice_button = QPushButton('Голосовой ввод', self)
        self.voice_button.clicked.connect(self.voiceButton)
        self.layout.addWidget(self.voice_button)    


        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Лампочка')
        self.show()

    def openSerialPort(self):
        port_name = 'COM4' 
        baud_rate = 9600  
        try:
            self.serial_port = serial.Serial(port_name, baud_rate)
            self.text_edit.append(f'Порт {port_name} открыт.')
        except Exception as e:
            self.text_edit.append(f'Ошибка открытия порта: {str(e)}')

    def closeSerialPort(self):
        if self.serial_port:
            self.serial_port.close()
            self.text_edit.append('Порт закрыт.')

    def sendData(self):
        if self.serial_port and self.serial_port.is_open:
            data = self.input_line.text()
            print(data)
            if data:
                self.serial_port.write(data.encode())
                self.text_edit.append(f'Отправлено: {data}')
                self.input_line.clear()

    def voiceButton(self):
        if self.serial_port and self.serial_port.is_open:
            self.text_edit.append(f'Працює')
            result = recognition()
            self.sendPositive(result)
        else:
            self.text_edit.append('Порт закрыт.')

             
    def sendPositive(self, positive):
        if positive == True:
            self.serial_port.write('True'.encode())
        elif positive == False:
            self.serial_port.write('False'.encode())



    def closeEvent(self, event):
        self.closeSerialPort()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SerialPortExample()
    sys.exit(app.exec_())
