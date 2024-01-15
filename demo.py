#Importing libraries used in this project
import python_speech_features
import numpy as np
import librosa as lr
import soundfile as sf
import pickle
import os 
import aanityslib as y
import endvoiceline as end

#Load in the trained machine learning model
file = open('mlmodel', 'rb')
mlmodeldemo = pickle.load(file)
file.close()


dir = "testikansio"
#os.mkdir(dir) NOTE folder should already exist. If it doesn't, uncomment this row.
# Äänitysten pituus sekunneissa
len = float(input("How long recordings: (s) "))
# Yksittäisten numeroiden kansioden nimet
nums = ["testinumero"]
# Monta äänitystä kustakin numerosta
n = 1

# Lisää kohina flag
add_noise = False
# Kohinan taso
scale_noise = 0.01

# Poista kohina flag
rmv_noise = False

# Leikkaus flag
cut = False
# Leikkausten pituus
cut_len = 1

#Ask user if they want to add noise and if so, how much
flg_addNoise = input("Do you want to add noise? (y/n) ")
if flg_addNoise.lower() == 'y':
    scale = float(input("Please input the scale of the noise: (range of about 0.01-0.1) "))
    add_noise = True

#Ask user if they want to remove noise
flg_rmvNoise = input("Do you want to remove noise? (y/n) ")
if flg_rmvNoise.lower() == 'y':
    rmv_noise = True

#Length of cut down recording in seconds
cut_len = 1
cut = True

for i in nums:
    num = i
    path = dir + '/' + num
    #os.mkdir(path) NOTE file should already exist. If it doesn't, uncomment this row.
    for j in range(1,n+1):
        file = num + ".wav"
        filepath = path + '/' + file
        print(f"Starting recording: {j} of num: {num.upper()}\n")
        y.aanita(filepath, len)
        
        # Äänitteen muokkaus
        if add_noise: # Kohinan lisäys
            y.lisaa_kohina(filepath, scale_noise)
        if rmv_noise: # Kohinan poisto
            y.poista_kohina(filepath)
        if cut: # Äänitteen leikkaus
            y.leikkaa(filepath, cut_len)
        
        # Äänitteen tarkastelu
        play = input("Play back recording? (y/n) ") # Kuuntele näyte
        if play.lower() == 'y':
            y.soita(filepath, cut_len)
        
        val = input("Redo recording? (y/n) ") # Uusi näyte NOTE THIS HAS A BUG!! RE-RECORDING NEEDS TO BE CUT DOWN TO 1S
        while val == 'y':
            print(f"Starting re-recording: {j} of num: {num.upper()}\n")
            y.aanita(filepath, len)

            if add_noise: # Kohinan lisäys
                y.lisaa_kohina(filepath, scale_noise)
            if rmv_noise: # Kohinan poisto
                y.poista_kohina(filepath)
            if cut: # Äänitteen leikkaus
                y.leikkaa(filepath, cut_len)

            play = input("Play back recording? (y/n) ") # Kuuntele näyte
            if play.lower() == 'y':
                y.soita(filepath, cut_len)

            val = input("Redo recording? (y/n) ")

#Read the recorded test signal, one at full quality, one downsampled to 6k Hz
testsignalfullqual, realfsfullqual = sf.read('testikansio/testinumero/testinumero.wav', dtype='float32')
testsignal, realfs = lr.load('testikansio/testinumero/testinumero.wav', sr=6000) ## downsample to 6k Hz
testsignal = np.concatenate((testsignal, [0]*3436))

#Apply mfcc
mfccdatatemp = python_speech_features.mfcc(testsignal, realfs)
#Flattening the matrix from mfcc function into a vector
mfccdata = mfccdatatemp.flatten()
mfccdata = np.reshape(mfccdata, (-1, 2028))

#Use trained ml model to predict the said number
predicted_num = mlmodeldemo.predict(mfccdata)

#Print out and announce the result of the prediction
print(f"We predict you said the number {predicted_num}")
end.end_voice_line(predicted_num, testsignalfullqual, realfsfullqual)
