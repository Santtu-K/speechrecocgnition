import soundfile as sf
import sounddevice as sd

def end_voice_line(predicted_num, recsig, fs):
    #Checking, which number the ml model predicted and deciding the voice file based on that
    #Text-to-speech voice lines generated using Narakeet: https://www.narakeet.com/
    modelstart, fsm = sf.read('lopputulosaudiofiles/veikkaanettakunsanoit.wav', dtype='float32')
    modelstart = modelstart[0:90000]
    if predicted_num == 0:
        model, fsm = sf.read('lopputulosaudiofiles/sanoit numeron nolla.wav', dtype='float32')
    elif predicted_num == 1:
        model, fsm = sf.read('lopputulosaudiofiles/sanoit numeron yksi .wav', dtype='float32')
    elif predicted_num == 2:
        model, fsm = sf.read('lopputulosaudiofiles/sanoit numeron kaksi.wav', dtype='float32')
    elif predicted_num == 3:
        model, fsm = sf.read('lopputulosaudiofiles/sanoit numeron kolme.wav', dtype='float32')
    elif predicted_num == 4:
        model, fsm = sf.read('lopputulosaudiofiles/sanoit numeron neljä.wav', dtype='float32')
    elif predicted_num == 5:
        model, fsm = sf.read('lopputulosaudiofiles/sanoit numeron viisi.wav', dtype='float32')
    elif predicted_num == 6:
        model, fsm = sf.read('lopputulosaudiofiles/sanoit numeron kuusi.wav', dtype='float32')
    elif predicted_num == 7:
        model, fsm = sf.read('lopputulosaudiofiles/sanoit numeron seits.wav', dtype='float32')
    elif predicted_num == 8:
        model, fsm = sf.read('lopputulosaudiofiles/sanoit numeron kahde.wav', dtype='float32')
    elif predicted_num == 9:
        model, fsm = sf.read('lopputulosaudiofiles/sanoit numeron yhdek.wav', dtype='float32')

    #Playing the ending voice line
    sd.play(modelstart, fsm)
    status = sd.wait() #Wait until file is done playing
    sd.play(recsig, fs)
    status = sd.wait() #Wait until file is done playing
    sd.play(model, fsm)
    status = sd.wait() #Wait until file is done playing
    return