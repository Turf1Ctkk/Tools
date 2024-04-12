import time
import subprocess
import threading
import locale
import codecs
import os
import sys
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.Qt import QWidget
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QLabel
from PyQt5.Qt import QApplication



def get_cuda_status():
    cmd = "nvidia-smi"
    ps = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    res = ''
    while True:
        data = ps.stdout.readline()
        data = str(data)
        if data == "b''":
            break
        if data.startswith('b\''):
            data = data[2:]
        if data.endswith('\\r\\n\''):
            data = data[:len(data)-5]
        data = data.replace('\\\\', '\\')
        res += data + '\n'
    return res


def get_gpu_name():
    cmd = "nvidia-smi -L"
    ps = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    res = ''
    while True:
        data = ps.stdout.readline()
        data = str(data)
        if data == "b''":
            break
        if data.startswith('b\''):
            data = data[2:]
        if data.endswith('\\r\\n\''):
            data = data[:len(data)-5]
        data = data.replace('\\\\', '\\')
        res += data + '&'
    return res


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'Cuda Supervisor @{get_gpu_name()}')
        self.resize(1040, 1040)
        self.setStyleSheet('background-color: #2A2A2A; color: white')
        self.geometry().center()


        self.ts_status = QLabel(self)
        self.ts_status.setText("None")
        self.ts_status.setStyleSheet('font-size: 22px; color: white')
        self.ts_status.adjustSize()
        self.ts_status.move(10, 10)

        self.cuda_status_thread = True
        self.th = threading.Thread(target=self.refresh_info, args=())
        self.th.start()


    def closeEvent(self, event):
        self.cuda_status_thread = False


    def refresh_info(self):
        while self.cuda_status_thread:
            self.ts_status.setText(get_cuda_status())
            self.ts_status.adjustSize()
            time.sleep(0.1)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())
