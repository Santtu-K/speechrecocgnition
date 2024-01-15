import os
import librosa as lr ## pip install librosa
import pandas as pd ## pip install pandas

def stringToNumber(name):
    if "yksi" in name:
        return 1
    elif "kaksi" in name:
        return 2
    elif "kolme" in name:
        return 3
    elif "neljä" in name:
        return 4
    elif "viisi" in name:
        return 5
    elif "kuusi" in name:
        return 6
    elif "seitsemän" in name:
        return 7
    elif "kahdeksan" in name:
        return 8
    elif "yhdeksän" in name:
        return 9

def main():
    audios = []
    labels = []
    for directory in ["trimmed", "pitchDown1", "pitchDown2", "pitchUp1", "pitchUp2", "slowedDown0.8x", "slowedDown0.9x", "spedUp1.075x", "spedUp1.15x", "spedUp1.225x", "spedUp1.3x"]:
        for file in sorted(os.listdir(f"./{directory}")):
            fileN = file.replace(".wav", "")
            y, fs = lr.load(f"./{directory}/{file}", sr=6000) ## downsample to 6k Hz
            audios.append(y)
            labels.append(stringToNumber(fileN))
    merged = pd.DataFrame(audios)
    merged.to_csv("all.csv", index=False)
    merged2 = pd.DataFrame(labels)
    merged2.to_csv("allLabels.csv", index=False)

main()