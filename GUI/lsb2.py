from numpy.lib.function_base import insert
from PIL import Image
import numpy as np


def bin_to_int(rgb):
    """Conversion d'un tuple binaire (chaîne) en un tuple entier.
    :return:Renvoie un tuple entier.
    """
    r, g, b = rgb
    return (int(r, 2),
            int(g, 2),
            int(b, 2))


def block_insert(img, logo, l, q, x, y):


    if l == 8:
        startL = 0
    else:
        startL = l - 8
    if q == 8:
        startQ = 0
    else:
        startQ = q - 8
    
    if x == 8:
        startLx = 0
    else:
        startLx = x - 8
    if y == 8:
        startQy = 0
    else:
        startQy = y - 8
    


    i2 = startLx

    for i in range(startL, l):
        j2 = startQy
        for j in range(startQ, q):
        
            lg_pixel = '{0:08b}'.format(logo[i][j])

            r, g, b = img[i2][j2]

            r = '{0:08b}'.format(r)
            g = '{0:08b}'.format(g)
            b = '{0:08b}'.format(b)
            
            rgb = (r[:6] + lg_pixel[:2], g[:6] + lg_pixel[2:4], b[:6] + lg_pixel[4:6])
            img[i2][j2] = bin_to_int(rgb)

            j2 = j2 + 1

        i2 = i2 + 1


def block_extract(img, logo, l, q, x, y):

    if l == 8:
        startL = 0
    else:
        startL = l - 8
    if q == 8:
        startQ = 0
    else:
        startQ = q - 8
    
    if x == 8:
        startLx = 0
    else:
        startLx = x - 8
    if y == 8:
        startQy = 0
    else:
        startQy = y - 8
    


    i2 = startLx

    for i in range(startL, l):
        j2 = startQy
        for j in range(startQ, q):
        
            

            r, g, b = img[i2][j2]

            r = '{0:08b}'.format(r)
            g = '{0:08b}'.format(g)
            b = '{0:08b}'.format(b)

            logo_pixel = r[6:8] + g[6:8] + b[6:8] + "00"
            
            pix = int(logo_pixel, 2)

            logo[i][j] = int(logo_pixel, 2)
            


            j2 = j2 + 1

        i2 = i2 + 1










