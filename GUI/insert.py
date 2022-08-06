from highlight import cropd_img
import random
import randm
from PIL import Image
import numpy as np
import lsb




def insrt(wtr_mat,mykey):

    wtr_mat  = np.array(wtr_mat)

    # mise a jour de tous les LSB de pixels a zero
    lsb.LSB_to_zero(wtr_mat)


    # géneration d'une liste d'index par division de l'image sur 4 regions 
    regions = lsb.index_regions(wtr_mat)
    # géneration d'une liste d'index du blocs restant aprés la division par region
    lst_blcs_rst = lsb.rows_lst(wtr_mat)


    mykeys = randm.rand_lst(mykey,4)

    for i in range(0,4,2):
        reg1_it = iter(randm.block_index_rand(wtr_mat,regions[i][0],regions[i][1],regions[i][2],regions[i][3],mykeys[i]))
        reg2_it = iter(randm.block_index_rand(wtr_mat,regions[i+1][0],regions[i+1][1],regions[i+1][2],regions[i+1][3],mykeys[i+1]))
        src = next(reg1_it,None)
        while src != None:
            dst = next(reg2_it,None)
            lsb.block_insert(wtr_mat,src[0],src[1],dst[0],dst[1])
            src = next(reg1_it,None)


    fin = len(lst_blcs_rst)
    if len(lst_blcs_rst) % 2 == 1:
        lst_blcs_rst.pop(fin-1)
    random.seed(mykey)
    random.shuffle(lst_blcs_rst)

    fin = len(lst_blcs_rst)
    for i  in range(0,fin,2):
        lsb.block_insert(wtr_mat,lst_blcs_rst[i][0],lst_blcs_rst[i][1],lst_blcs_rst[i+1][0],lst_blcs_rst[i+1][1])


    return wtr_mat
    

def rgb_insrt(img_path,key):
    # Lecture de l'image en version grayscale
    img_wtr = Image.open(img_path).convert('RGB')
    if img_wtr.size[0] % 8 != 0 or img_wtr.size[1] % 8 != 0:
            img_wtr = cropd_img(img_wtr)

            
    r_mat, g_mat, b_mat = img_wtr.split()
    
    r = insrt(r_mat,key)
    g = insrt(g_mat,key)
    b = insrt(b_mat,key)
    final = []
   
    for i in range(len(r)):
        final.append([])
        for j in range(len(r[0])):
            final[i].append([r[i][j],g[i][j],b[i][j]])
    
    
    output = open("img_watermarked/wtrmrkd.png", "wb")
    fin = Image.fromarray(np.array(final))
    fin.save(output)