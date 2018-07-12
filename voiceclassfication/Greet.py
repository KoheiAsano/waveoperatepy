import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication

from audiofunc import RecordToWav,Play
#from PyQt5.QtCore import QCoreApplication
from keras.models import load_model
model = load_model('my_model.h5')

import pyaudio
import wave
import librosa

class Greet(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.model = load_model('my_model.h5')

    def initUI(self, CHUNK = 1024,FORMAT = pyaudio.paInt16 ,CHANNELS = 2,RATE = 44100,RECORD_SECONDS = 5,WAVE_OUTPUT_FILENAME = "output.wav"):
        self.chunk = CHUNK
        self.format = FORMAT
        self.channels = CHANNELS
        self.rate = RATE
        self.record_seconds = RECORD_SECONDS
        self.wave_output_filename = WAVE_OUTPUT_FILENAME
        # QPushButtonの第一引数はラベル
        # QPushButtonの第二引数は親ウィジェット(QWidgetに継承されたExampleウィジェット)
        qbtn = QPushButton('Greet!!!', self)
        #qbtn = QtWidgts.QPushButton('Recording', self)
        qbtn.clicked.connect(self.RecordAndGreet)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 50)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Recorder')    
        self.show()
        
        
    def RecordAndGreet(self):
        self.wave = RecordToWav()
        self.n_mfcc = 20
        #Play(self.wave)
        y, sr = librosa.load(self.wave)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=self.n_mfcc)
        test = mfcc.reshape(1,20, 216, 1)
        Greet = model.predict(test).argmax()
        print(model.predict(test))
        if Greet==0:#ohayo
            Play("g_ohayo.wav")
        elif Greet==1:#oyasumi
            Play("g_oyasumi.wav")
        else:
            Play("g_ganbatte.wav")
        
if __name__ == '__main__':

    app = QApplication(sys.argv)
    Greet = Greet()
    sys.exit(app.exec_())