# Librosa on äänianalyysiin suunniteltu kirjasto
import librosa

# https://librosa.org/doc/main/generated/librosa.feature.mfcc.html#librosa.feature.mfcc

# mfcc-funktio: äänisignaalin Mel-frequency cepstral coefficients (MFCC) -ominaisuuksien erotteluun
# parametrit: äänitiedosto (file_path), MFCC-kertoimien määrä (num_mfcc), FFT-koko (n_fft) ja hypyn pituus (hop_size)
def mfcc(file_path, num_mfcc=???, n_fft=???, hop_size=???):
    # ladataan äänisignaali
    signal, sr = librosa.load(file_path)
    # käytetään librosa.feature.mfcc -funktiota äänisignaalin MFCC-kertoimien erotteluun
    # parametrit: äänisignaali (y), näytteenottotaajuus (sr), haluttu MFCC-kertoimien määrä (n_mfcc), FFT-koko (n_fft) ja hypyn pituus (hop_length)
    mfcc_coeff = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=num_mfcc, n_fft=n_fft, hop_length=hop_size)
    # palautetaan MFCC-kertoimet, joilla kuvataan äänisignaalin piirteitä koneoppimismallille äänen tunnistamiseen
    return mfcc_coeff

mfcc_coeff = mfcc('yksi1.wav')
print(mfcc_coeff)

'''
Output:

 [[-5.6762067e+02 -5.6865082e+02 -5.7696454e+02 ... -5.8061414e+02
  -5.7992084e+02 -5.7891809e+02]
 [ 2.2304710e+01  2.0406557e+01  9.4546938e+00 ...  4.5700512e+00
   5.4970942e+00  6.8725224e+00]
 [ 1.9639874e+01  1.7288832e+01  7.8681054e+00 ...  3.9708614e+00
   4.5546188e+00  5.8531761e+00]
 ...
 [ 9.7811234e-01  2.8938007e+00  2.2427900e+00 ...  3.0587694e-01
   1.0834292e+00  3.4148271e+00]
 [ 7.8183472e-01  2.4931226e+00  2.2439809e+00 ...  5.9006709e-01
   4.6463549e-01  2.4607437e+00]
 [ 4.4579056e-01  1.8718731e+00  2.2202139e+00 ...  1.1112915e+00
   3.8472426e-01  2.1167397e+00]]
'''

