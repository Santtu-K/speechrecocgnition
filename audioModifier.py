import os
import maf
import numpy as np
import librosa as lr ## pip install librosa
import soundfile as sf ## pip install soundfile
from audiostretchy.stretch import stretch_audio ## pip install audiostretchy[all]

def cut(readPath, writePath, t):
    x, fs = sf.read(readPath)
    wnd = 10000
    n_sample = fs * t
    mean = maf.MA_filter(x, wnd)
    max_val = max(mean) # Skaalausfactor (skaalaa arvot välille [0,1])
    start = -1
    end = -1
    i = 0
    v = mean[i]/max_val # Skaalaus
    while v <= 0.1:
        i = i + 1
        v = mean[i]/max_val
    start = int(i + wnd/2) # Alku
    while v >= 0.1:
        i = i + 1
        v = mean[i]/max_val
    end = int(i + wnd/2) # Loppu
    trim = x[start:end]
    pituus = len(trim)
    ero = n_sample - pituus
    if ero > 0:
        trim = np.concatenate((trim, [0]*ero)) # 0 päddäys
    elif ero < 0:
        trim = trim[0:pituus-abs(ero)] # puheen leikkaus
    sf.write(writePath, trim, fs)

def main():
    for number in ['', '2', '3', '4']: ## for each person
        for directory in sorted(os.listdir(f"./Numeroäänitteet{number}")): ## for each number folder
            if directory != ".gitkeep":
                for file in sorted(os.listdir(f"./Numeroäänitteet{number}/{directory}")): ## for each file
                    if file != ".gitkeep":
                        fileN = file.replace(".wav", "")
                        readpath = f"./Numeroäänitteet{number}/{directory}/{file}"
                        cut(readpath, f"./trimmed/{fileN}{number}.wav", 1) ## trim every file and save
                        readpath2 = f"./trimmed/{fileN}{number}.wav"
                        ## slowed down audios
                        stretch_audio(readpath2, f"./spedUp1.3x/{fileN}{number}sped.wav", ratio=1.3)
                        stretch_audio(readpath2, f"./spedUp1.225x/{fileN}{number}sped.wav", ratio=1.225)
                        stretch_audio(readpath2, f"./spedUp1.15x/{fileN}{number}sped.wav", ratio=1.15)
                        stretch_audio(readpath2, f"./spedUp1.075x/{fileN}{number}sped.wav", ratio=1.075)
                        ## sped up audios
                        stretch_audio(readpath2, f"./slowedDown0.9x/{fileN}{number}slowed.wav", ratio=0.9)
                        stretch_audio(readpath2, f"./slowedDown0.8x/{fileN}{number}slowed.wav", ratio=0.8)
                        ## extract the audio
                        audio, fs = lr.load(readpath2)
                        ## pitched up audios
                        audioMod = lr.effects.pitch_shift(audio, sr=fs, n_steps=1)
                        audioMod2 = lr.effects.pitch_shift(audio, sr=fs, n_steps=2)
                        sf.write(f"./pitchUp1/{fileN}{number}.wav", audioMod, fs)
                        sf.write(f"./pitchUp2/{fileN}{number}.wav", audioMod2, fs)
                        ## pitched down audios
                        audioMod3 = lr.effects.pitch_shift(audio, sr=fs, n_steps=-1)
                        audioMod4 = lr.effects.pitch_shift(audio, sr=fs, n_steps=-2)
                        sf.write(f"./pitchDown1/{fileN}{number}.wav", audioMod3, fs)
                        sf.write(f"./pitchDown2/{fileN}{number}.wav", audioMod4, fs)

main()