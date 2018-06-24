import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
#from PyQt5.QtCore import QCoreApplication


import pyaudio
import wave

class Wavesaver(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self, CHUNK = 1024,FORMAT = pyaudio.paInt16 ,CHANNELS = 2,RATE = 44100,RECORD_SECONDS = 5,WAVE_OUTPUT_FILENAME = "output.wav"):
        self.chunk = CHUNK
        self.format = FORMAT
        self.channels = CHANNELS
        self.rate = RATE
        self.record_seconds = RECORD_SECONDS
        self.wave_output_filename = WAVE_OUTPUT_FILENAME
        # QPushButtonの第一引数はラベル
        # QPushButtonの第二引数は親ウィジェット(QWidgetに継承されたExampleウィジェット)
        qbtn = QPushButton('Recording', self)
        #qbtn = QtWidgts.QPushButton('Recording', self)
        qbtn.clicked.connect(self.Record)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 50)

        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('Recorder')    
        self.show()
        
        
    def Record(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk)
        print("* recording")
        frames = []

        for i in range(0, int(self.rate / self.chunk * self.record_seconds)):
            data = stream.read(self.chunk)
        frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(self.wave_output_filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        
if __name__ == '__main__':

    app = QApplication(sys.argv)
    wavesaver = Wavesaver()
    sys.exit(app.exec_())