from lsb import closest_div8
from PIL import Image
import myDCT
from math import log10, sqrt
import cv2
import numpy as np




def highlight(mat, l, q,coef):

    if l == 8:
        startL = 0
    else:
        startL = l - 8
    if q == 8:
        startQ = 0
    else:
        startQ = q - 8
    

    for i in range(startL, l):
        for j in range(startQ, q):
            mat[i][j] = coef
            

def block_detect(blc,blc2,rgb_blc,l,q, x, y,coef):
    
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
    

    code1 = myDCT.block_gen(blc,l,q)
    code2 = myDCT.block_gen(blc,x,y)
    
    code1_lsb = ""
    code2_lsb = ""


    for i in range(startL, l):
        j2 = startQy
        for j in range(startQ, q):
        
            nb = '{0:08b}'.format(blc2[i][j])
            code2_lsb = code2_lsb + nb[-1]

            nb = '{0:08b}'.format(blc2[i2][j2])
            code1_lsb = code1_lsb + nb[-1]

            j2 = j2 + 1

        i2 = i2 + 1

    
    if code1 != code1_lsb:
        highlight(rgb_blc,x,y,coef)

    if code2 != code2_lsb:
        highlight(rgb_blc,l,q,coef)


   
def cropd_img(img):
    x, y = img.size
    
    if img.size[0] != 8:
        x = closest_div8(img.size[0])

    if img.size[1] != 8:
        y = closest_div8(img.size[1])

    return  img.crop((0,0,x,y))



def PSNR(org, scnd):
    original = cv2.imread(org)
    compressed = cv2.imread(scnd, 1)
    mse = np.mean((original - compressed) ** 2)
    if(mse == 0):  # MSE is zero means no noise is present in the signal .
                  # Therefore PSNR have no importance.
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr
  

