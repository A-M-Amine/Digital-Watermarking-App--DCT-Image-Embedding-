from highlight import cropd_img
from lsb2 import block_extract
from randm import block_index_rand, rand_lst
from PIL import Image
import numpy as np


def extract_img_embd(img,key):

    img_mat = np.array(cropd_img(Image.open(img).convert("RGB")))

    logo_mat = np.array(cropd_img(Image.open(img).convert("L")))



    mykey = key
    mykeys = rand_lst(mykey,2)

    liste_pos = block_index_rand(img_mat, 0, 0, len(img_mat), len(img_mat[0]), mykeys[0])
    liste_pos_2 = block_index_rand(img_mat, 0, 0, len(img_mat), len(img_mat[0]), mykeys[1])

    it = iter(liste_pos)
    it2 = iter(liste_pos_2)
    pos = next(it,None)
    pos2 = next(it,None)
    while pos != None:
        block_extract(img_mat,logo_mat,pos[0],pos[1],pos2[0],pos2[1])
        pos = next(it,None)
        pos2 = next(it2,None)

    
    output = open("img_resultats/extrctd_from_img.png", "wb")
    fin = Image.fromarray(logo_mat)
    fin.save(output)