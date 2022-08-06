import random
from randm import block_index_rand, rand_lst
from PIL import Image
import numpy as np
import lsb
from highlight import block_detect, cropd_img
import myDCT


def extrct(img, mykey):

    
    wtr_mat = np.array(img)

    res_mat = np.array(img)
    #np.zeros((len(wtr_mat),len(wtr_mat[0])), int)

    # géneration d'une liste d'index par division de l'image sur 4 regions 
    regions = lsb.index_regions(wtr_mat)
    # géneration d'une liste d'index du blocs restant aprés la division par region
    lst_blcs_rst = lsb.rows_lst(wtr_mat)

    mykeys = rand_lst(mykey,4)

    for i in range(0,4,2):
        reg1_it = iter(block_index_rand(wtr_mat,regions[i][0],regions[i][1],regions[i][2],regions[i][3],mykeys[i]))
        reg2_it = iter(block_index_rand(wtr_mat,regions[i+1][0],regions[i+1][1],regions[i+1][2],regions[i+1][3],mykeys[i+1]))
        src = next(reg1_it,None)
        while src != None:
            dst = next(reg2_it,None)
            lsb.block_extract(wtr_mat, res_mat, src[0], src[1], dst[0], dst[1])
            src = next(reg1_it,None)


    fin = len(lst_blcs_rst)
    if len(lst_blcs_rst) % 2 == 1:
        lst_blcs_rst.pop(fin-1)

    random.seed(mykey)
    random.shuffle(lst_blcs_rst)

    fin = len(lst_blcs_rst)
    for i  in range(0,fin,2):
        lsb.block_extract(wtr_mat, res_mat, lst_blcs_rst[i][0],lst_blcs_rst[i][1],lst_blcs_rst[i+1][0],lst_blcs_rst[i+1][1])

    return res_mat


def rgb_extract(img_path,key):

     # Lecture de l'image en version grayscale
    img_wtr = Image.open(img_path).convert('RGB')
    if img_wtr.size[0] % 8 != 0 or img_wtr.size[1] % 8 != 0:
            img_wtr = cropd_img(img_wtr)

    r_mat, g_mat, b_mat = img_wtr.split()
    
    r = extrct(r_mat,key)
    g = extrct(g_mat,key)
    b = extrct(b_mat,key)
    final = []
    for i in range(len(r)):
        final.append([])
        for j in range(len(r[0])):
            final[i].append([r[i][j],g[i][j],b[i][j]])
    
    
    output = open("img_resultats/res.png", "wb")
    fin = Image.fromarray(np.array(final))
    fin.save(output)

def dtct(img,mykey,coef):
    
    

    wtr_mat = np.array(img)
    lsb.LSB_to_zero(wtr_mat)

    wtr2_mat = np.array(img)
    

    dtct_mat = np.array(img)

    # géneration d'une liste d'index par division de l'image sur 4 regions 
    regions = lsb.index_regions(wtr_mat)
    # géneration d'une liste d'index du blocs restant aprés la division par region
    lst_blcs_rst = lsb.rows_lst(wtr_mat)

    mykeys = rand_lst(mykey,4)


    for i in range(0,4,2):
        reg1_it = iter(block_index_rand(wtr_mat,regions[i][0],regions[i][1],regions[i][2],regions[i][3],mykeys[i]))
        reg2_it = iter(block_index_rand(wtr_mat,regions[i+1][0],regions[i+1][1],regions[i+1][2],regions[i+1][3],mykeys[i+1]))
        src = next(reg1_it,None)
        while src != None:
            dst = next(reg2_it,None)
            block_detect(wtr_mat, wtr2_mat, dtct_mat, src[0], src[1], dst[0], dst[1],coef)
            src = next(reg1_it,None)


    fin = len(lst_blcs_rst)
    if len(lst_blcs_rst) % 2 == 1:
        lst_blcs_rst.pop(fin-1)

    random.seed(mykey)
    random.shuffle(lst_blcs_rst)

    fin = len(lst_blcs_rst)
    for i  in range(0,fin,2):
        block_detect(wtr_mat, wtr2_mat, dtct_mat, lst_blcs_rst[i][0],lst_blcs_rst[i][1],lst_blcs_rst[i+1][0],lst_blcs_rst[i+1][1],coef)

    return dtct_mat

def rgb_dctct(img_path, key):

    img_wtr = Image.open(img_path).convert('RGB')
    if img_wtr.size[0] % 8 != 0 or img_wtr.size[1] % 8 != 0:
            img_wtr = cropd_img(img_wtr)

    r_mat, g_mat, b_mat = img_wtr.split()
    
    r = dtct(r_mat,key,100)
    g = dtct(g_mat,key,200)
    b = dtct(b_mat,key,80)
    final = []
    for i in range(len(r)):
        final.append([])
        for j in range(len(r[0])):
            final[i].append([r[i][j],g[i][j],b[i][j]])
    
    
    output = open("img_resultats/highlighted.png", "wb")
    fin = Image.fromarray(np.array(final))
    fin.save(output)