import spectral.io.envi as envi
import matplotlib.pyplot as plt
import numpy as np
import os

def data_filter(targetdir):
    if os.path.exists(targetdir):
        bil_files = os.listdir(targetdir)
        bil_files = [x[:-4] for x in  bil_files if  x[-4:] == '.bil']
        if not  bil_files:
            raise Exception('the dir has no report file')
    else:
        raise Exception('sorry, the dir is not exist!')     
    return bil_files

def apple_mask(sample, band, dfra, ufra):
    data_ref = envi.open(sample+'.bil.hdr', sample+'.bil')
    sample_band = data_ref.read_band(band)
    dfra_band = np.percentile(sample_band, dfra)
    ufra_band = np.percentile(sample_band, ufra)
    sample_band[sample_band < dfra_band] = 0
    sample_band[sample_band > ufra_band] = 0
    fig, ax = plt.subplots()
    ax.imshow(sample_band*255, cmap='gray')
    ax.axis('off')
    #plt.show()
    fig.savefig('apple_%s_%s_d%s_u%s.png'%(sample,band,dfra,ufra))
    return 0

def extract_roi():
    data_ref = envi.open(sample+'.bil.hdr', sample+'.bil')
    sample_band = 

def hdr_band(sample, wavelength):
    data_hdr = envi.open(sample+".bil.hdr")
    bands = data_hdr.bands.centers
    for i in bands:
        if i>=wavelength:
            band = bands.index(i)
            break
    return band

def mask_main():
    targetdir = './'
    wavelength = 700
    bil_files = data_filter(targetdir)
    for bil in bil_files:
        band = hdr_band(bil, wavelength)
        for dfra in range(75, 95,5):
            for ufra in range(96,100,2):
                apple_mask(bil, band, dfra, ufra)

if __name__=="__main__":
    mask_main()

