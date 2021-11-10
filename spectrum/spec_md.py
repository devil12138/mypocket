import spectral.io.envi as envi
from spectral import imshow,save_rgb
import matplotlib.pyplot as plt
import sys 
import os
import numpy as np
img = envi.open('./bluetooth/30_9_1.bil.hdr', './bluetooth/30_9_1.bil')

def hyper_show():
    view = imshow(img, (187,120,52))
    print(view)
    save_rgb('apple1.jpg', img, [187, 120, 52])

def spectrum_show():
    data_nparr = np.array(img.load())

    save_rgb('apple2.jpg', data_nparr, [187,120,52])

    apple_pixel_y = 75
    apple_pixel_x = 200
    apple_pixel = data_nparr[
            apple_pixel_y:apple_pixel_y+1,
            apple_pixel_x:apple_pixel_x+1,
            :
            ]
    apple_pixel_squeezed = np.squeeze(apple_pixel)
    plt.plot(bands, apple_pixel_squeezed)
    plt.title('apple spectral footprint\n(pixel {},{})'.format(apple_pixel_x, apple_pixel_y))
    plt.xlabel('wavelength')
    plt.ylabel('reflectance')
    plt.savefig('apple_spectrum.jpg')
    os.system('termux-open apple_spectrum.jpg')

def k_mean():
    img = envi.open('./bluetooth/30_9_1.bil.hdr', './bluetooth/30_9_1.bil').load()
    (m, c) = kmeans(img, 20, 30)
    plt.figure()
    for i in range(c.shape[0]):
        plt.plot(c[i])
    plt.grid()
    plt.savefig('kmean.jpg')
    os.system('termux-open kmean.jpg')

k_mean()
