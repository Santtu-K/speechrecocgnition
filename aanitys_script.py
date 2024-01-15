import os 
import aanityslib as y

dir = input("Give a name for you directory: ") # Kansion nimi
os.mkdir(dir)
# Äänitysten pituus sekunneissa
len = float(input("How long recordings: (s) "))
# Yksittäisten numeroiden kansioden nimet
nums = ["nolla", "yksi", "kaksi", "kolme", "neljä", "viisi", "kuusi", "seitsemän", "kahdeksan", "yhdeksän"]
# Monta äänitystä kustakin numerosta
n = int(input("How many recordings of each number: "))

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

flg_addNoise = input("Do you want to add noise? (y/n) ")
if flg_addNoise.lower() == 'y':
    scale = float(input("Please input the scale of the noise: (range of about 0.01-0.1) "))
    add_noise = True

flg_rmvNoise = input("Do you want to remove noise? (y/n) ")
if flg_rmvNoise.lower() == 'y':
    rmv_noise = True

flg_cut = input("Do you want to cut the recording? (y/n) ")
if flg_cut.lower() == 'y':
    cut_len = float(input("How long do you want to cut it? (s) "))
    cut = True

for i in nums:
    num = i
    path = dir + '/' + num
    os.mkdir(path)
    for j in range(1,n+1):
        file = num + str(j) + ".wav"
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
            y.soita(filepath, len)
        plt = input("Do you want to plot the recording? (y/n) ") # Plottaa näyte
        if plt.lower() == 'y':
            name = input("Give a name for your plot: ")
            y.plottaa(filepath, name)
        
        val = input("Redo recording? (y/n) ") # Uusi näyte
        while val == 'y':
            print(f"Starting re-recording: {j} of num: {num.upper()}\n")
            y.aanita(filepath, len)
            val = input("Redo recording? (y/n) ")