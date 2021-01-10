from flask import Flask,render_template,redirect,request
from wave import open as open_wave
import numpy as np
import glob
import pandas as pd
import sklearn
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import pickle as pkl

def catOrDog(fileName):
    print('Cat Dog')
    if 'FalseKW' in fileName:
        return 'False Killer Whale'
    elif 'SouthRW' in fileName:
        return 'Southen Right Whale'
    elif 'Killer' in fileName:
        return 'Killer Whale'
    else:
        return 'Northen Right Whale'

def writeOSPtoFile(start, file, test_wave):
    for s in range(start, 14700 + start, 100):
        file.write(str(test_wave.ys[s]))
        file.write(',')

def searchInArray(last, freq, data):
    curr = last
    #print('Looking for %d' % freq)
    for s in range(last, data.size):
        if freq < int(data[s]):
            if s > 0:
                curr = s
                break
    return curr


def writeSpectogramToFile(file, spectrum):
    pos = 0
    print('In writeSpectoramToFile')
    for freq in range(10, 8000, 53):
        pos = searchInArray(pos, freq, spectrum.fs)
        file.write(str(spectrum.hs[pos].real))
        file.write(',')
    file.write('\n')
    #print('Last Postion found at %d' % pos)

def runOSP(spectrumFile, fileName):
    test_wave = read_wave(fileName)
    spectrum = test_wave.make_spectrum()
    spectrumFile.write(catOrDog(fileName))
    spectrumFile.write(',')
    writeSpectogramToFile(spectrumFile, spectrum)

def read_wave(filename='sound.wav'):
    """Reads a wave file.

    filename: string

    returns: Wave
    """

    fp = open_wave(filename, 'r')

    nchannels = fp.getnchannels()
    nframes = fp.getnframes()
    sampwidth = fp.getsampwidth()
    framerate = fp.getframerate()

    # Adding this hard coded min as large audio files were blowing away
    # the readframes processing.
    z_str = fp.readframes(min([50000, nframes]))

    fp.close()

    dtype_map = {1:np.int8, 2:np.int16, 3:'special', 4:np.int32}
    if sampwidth not in dtype_map:
        raise ValueError('sampwidth %d unknown' % sampwidth)

    if sampwidth == 3:
        xs = np.fromstring(z_str, dtype=np.int8).astype(np.int32)
        ys = (xs[2::3] * 256 + xs[1::3]) * 256 + xs[0::3]
    else:
        ys = np.fromstring(z_str, dtype=dtype_map[sampwidth])

    # if it's in stereo, just pull out the first channel
    if nchannels == 2:
        ys = ys[::2]


    #ts = np.arange(len(ys)) / framerate
    wave = Wave(ys, framerate=framerate)
    wave.normalize()

    return wave

def normalize(ys, amp=1.0):
    """Normalizes a wave array so the maximum amplitude is +amp or -amp.

    ys: wave array
    amp: max amplitude (pos or neg) in result

    returns: wave array
    """
    high, low = abs(max(ys)), abs(min(ys))
    return amp * ys / max(high, low)

class Wave:
    """Represents a discrete-time waveform.

    """
    def __init__(self, ys, ts=None, framerate=None):
        """Initializes the wave.

        ys: wave array
        ts: array of times
        framerate: samples per second
        """
        self.ys = np.asanyarray(ys)
        self.framerate = framerate if framerate is not None else 11025

        if ts is None:
            self.ts = np.arange(len(ys)) / self.framerate
        else:
            self.ts = np.asanyarray(ts)

    def normalize(self, amp=1.0):
        """Normalizes the signal to the given amplitude.

        amp: float amplitude
        """
        self.ys = normalize(self.ys, amp=amp)

    def make_spectrum(self, full=False):
        """Computes the spectrum using FFT.
        Fourier Transforms
        returns: Spectrum
        """
        n = len(self.ys)
        d = 1.0 / self.framerate

        #print('framerate is %f , d is %f' % (n, d))

        if full:
            hs = np.fft.fft(self.ys)
            fs = np.fft.fftfreq(n, d)
        else:
            hs = np.fft.rfft(self.ys)
            fs = np.fft.rfftfreq(n, d)

        return Spectrum(hs, fs, self.framerate, full)


class Spectrum():
    """Represents the spectrum of a signal."""

    def __init__(self, hs, fs, framerate, full=False):
        """Initializes a spectrum.
        hs: array of amplitudes (real or complex)
        fs: array of frequencies
        framerate: frames per second
        full: boolean to indicate full or real FFT
        """
        self.hs = np.asanyarray(hs)
        self.fs = np.asanyarray(fs)
        self.framerate = framerate
        self.full = full


def prediction(file):
    spectrumFile = open('pp.csv', 'w')
    runOSP(spectrumFile, file)
    spectrumFile.close()
    reader=open("model.pkl","rb")
    model=pkl.load(reader)
    df=pd.read_csv("pp.csv",header=None)
    predict_whale=model.predict(df.iloc[:,1:152].values)
    result=""
    if(predict_whale==0):
        result="False Killer Whale"
    elif(predict_whale==1):
        result = "Killer Whale"
    else:
        result = "Northen Right Whale"
    return result
app=Flask(__name__,static_folder='static/')
@app.route('/')
def hello():
	return render_template("whales.html")
@app.route('/result',methods=['POST'])
def submit():
    if request.method=='POST':
        # try: 
        f=request.files['fileUpload'] 
        path = "{}".format(f.filename)
        print(f)
        f.save('static/'+path)
        animal=prediction('static/'+path)
        return render_template("resultEven.html",your_result=animal,filename=animal+'.jpg')
		# except:
		# 	return render_template("resultEven.html",your_result="NO IMAGE FOUND",filename="sign.png")
if __name__=='__main__':
	app.run(debug = True )
