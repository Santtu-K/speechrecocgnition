import pyaudio
import wave
import os.path
import soundfile as sf
import noisereduce as nr
import sounddevice as sd
import numpy as np
import maf
import matplotlib.pyplot as plt
import time

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second

def aanita(savepath, t):
    seconds = t
    #save_path = "testi"
    #filename = filename
    completeName = savepath #os.path.join(save_path, filename)
    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    val = input("Press enter to start recording\n")
    print("Recording\n")
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(completeName, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

# Kohinan lisäys
def lisaa_kohina(filename, scale):
    x, fs = sf.read(filename)
    max_val = max(abs(x))
    size = len(x)
    res = [0]*size
    kohina = np.random.normal(0, max_val * scale, size)
    for i, v in enumerate(x):
        res[i] = v + kohina[i]
    sf.write(filename, res, fs)

# Kohinan poisto
def poista_kohina(filename):
    x, fs = sf.read(filename)
    res = nr.reduce_noise(x,fs)
    sf.write(filename, res, fs)
    return res

# Audion leikkaus
def leikkaa(filename, t):
    x, fs = sf.read(filename)
    wnd = 10000
    n_sample = fs * t
    mean = maf.MA_filter(x, wnd)
    max_val = max(mean) # Skaalausfactor (skaalaa arvot välille [0,1])
    start = -1
    end = -1
    i = 0
    v = mean[i]/max_val # Skaalaus
    while v <= 0.3:
        i = i + 1
        v = mean[i]/max_val
    start = int(i + wnd/2) # Alku
    while v >= 0.3:
        i = i + 1
        v = mean[i]/max_val
    end = int(i + wnd/2) # Loppu
    trim = x[start:end]
    pituus = len(trim)
    ero = n_sample - pituus
    if ero > 0:
        trim = np.concatenate((trim, [0]*round(ero))) # 0 päddäys
    elif ero < 0:
        trim = trim[0:pituus-abs(ero)] # puheen leikkaus
    sf.write(filename, trim, fs)

# Plottaus
def plottaa(filename, save_full):
    x, fs = sf.read(filename)
    plt.figure(1); plt.clf()
    Y_LIMS = [-1, 1]    # y-axis limits
    plt.plot(abs(x))
    plt.xlabel('Time (samples)') # Beautify
    plt.ylabel('Amplitude (1)')
    plt.ylim(Y_LIMS)
    plt.title('Input')
    plt.savefig(save_full)

# Äänen soittaminen
def soita(filename, t):
    x, fs = sf.read(filename)
    sd.play(x, fs)
    time.sleep(t)
