from numpy.lib.function_base import insert
import myDCT
from PIL import Image
import randm
import random
import numpy as np


def int_to_bin(rgb):
    """Conversion d'un tuple entier en tuple binaire (chaîne).
    :return: Un tuple de chaîne"""
    r, g, b = rgb
    return ('{0:08b}'.format(r), '{0:08b}'.format(g), '{0:08b}'.format(b))


def bin_to_int(rgb):
    """Conversion d'un tuple binaire (chaîne) en un tuple entier.
    :return:Renvoie un tuple entier.
    """
    r, g, b = rgb
    return (int(r, 2),
            int(g, 2),
            int(b, 2))



def block_insert(blc,l,q, x, y):

    
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

    
    

    cpt = 0
    for i in range(startL, l):
        j2 = startQy
        for j in range(startQ, q):
        
            nb = '{0:08b}'.format(blc[i][j])
            nb = nb[0:-1] + code2[cpt]
            blc[i][j] = int(nb, 2)

            nb = '{0:08b}'.format(blc[i2][j2])
            nb = nb[0:-1] + code1[cpt]
            blc[i2][j2] = int(nb, 2)

            cpt = cpt + 1

            j2 = j2 + 1
        i2 = i2 + 1    

    


def block_extract(blc,res,l,q, x, y):
    
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
    
    
    code1 = ""
    code2 = ""


    for i in range(startL, l):
        j2 = startQy
        for j in range(startQ, q):
        
            nb = '{0:08b}'.format(blc[i][j])
            code2 = code2 + nb[-1]

            nb = '{0:08b}'.format(blc[i2][j2])
            code1 = code1 + nb[-1]

            j2 = j2 + 1

        i2 = i2 + 1

    
    blc1 = myDCT.decode_64b(code1)
    myDCT.reverse_zigzag_quant(blc1)
    blc1 = myDCT.idct2(blc1)
    blc2 = myDCT.decode_64b(code2)
    myDCT.reverse_zigzag_quant(blc2)
    blc2 = myDCT.idct2(blc2)

    res[startL:l, startQ:q] = blc1
    res[startLx:x, startQy:y] = blc2



def position_list(x,y,height,width):
    pos_x = round (int(height * 0.3) / 8 ) * 8
    pos_y = round (int(width * 0.3) / 8 ) * 8

    
    if x + pos_x >= height:
        x_axis_pos = (x + pos_x) % height
    else:
        x_axis_pos = x + pos_x
    
    if y + pos_y >= width:
        y_axis_pos = (y + pos_y) % width
    else:
        y_axis_pos = y + pos_y

    if x - pos_x < 0:
        x_axis_neg = (x - pos_x) % height
    else:
        if x - pos_x == 0:
            x_axis_neg = height
        else:
            x_axis_neg  = x - pos_x
    
    
    if y - pos_y < 0:
        y_axis_neg = (y - pos_y) % width
    else:
        if y - pos_y == 0:
            y_axis_neg = width
        else:
            y_axis_neg = y - pos_y

    pos = [[x_axis_pos,y_axis_pos],[x_axis_pos,0],[0,y_axis_pos],
            [x_axis_pos,y_axis_neg],[x_axis_neg,y_axis_pos],[x_axis_neg,y_axis_neg],
            [x_axis_neg,0],[0,y_axis_neg]]
    
    return pos
    

def index_insertion(mat,l,q,key):


    pos = position_list(l,q,len(mat),len(mat[0]))
    random.seed(key)
    random.shuffle(pos)
    pos_it = iter(pos)

    #yessir = False
    tmp = next(pos_it,None)
    while tmp != None:
        x, y = tmp
        if x == 0:
            x = l
        if y == 0:
            y = q
        #print(" pos " + str(x) +"  "+ str(y))
        if is_empty_blc(mat,x,y) == True:
            yessir = True
            block_insert(mat,l,q,x,y)
            break
        tmp = next(pos_it,None)

    '''
    if yessir == False:
        insert_from_last(mat,l,q)'''
        
    



def is_empty_blc(mat,l,q):

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
            nb = '{0:08b}'.format(mat[i][j])
            if nb[-1] != "0":
                return False
    
    return True




def block_iter(mat, l, q):
    tab = []
    if l == 8:
        startL = 0
    else:
        startL = l - 8
    if q == 8:
        startQ = 0
    else:
        startQ = q - 8
    cpt = 0

    for i in range(startL, l):
        tab.append([])
        for j in range(startQ, q):
            tab[cpt].append(mat[i][j])
        cpt = cpt + 1

    return tab




def closest_div8(x):
    y = x / 8
    return int(y) * 8


def fill(res, inserted, l, q):
    if l == 8:
        startL = 0
    else:
        startL = l - 8
    if q == 8:
        startQ = 0
    else:
        startQ = q - 8
    in_it = iter(inserted.flatten())
    for i in range(startL, l):
        for j in range(startQ, q):
            res[i, j] = next(in_it)


def LSB_to_zero(mat):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            bin = '{0:08b}'.format(mat[i,j])
            bin = bin[:-1] + "0"
            mat[i,j] = int(bin,2)




def index_regions(img):

    x = closest_div8(len(img)/ 2)
    y = closest_div8(len(img[0])/ 2)



    region_1 = [0, 0, x, y ]
    region_2 = [x, y, x*2, y*2 ]
    region_3 = [0, y, x, y*2 ]
    region_4 = [x, 0, x*2, y ]
    regions = [ region_1, region_2, region_3, region_4 ]

    return regions


def rows_lst(img):

    x = closest_div8(len(img)/ 2)
    y = closest_div8(len(img[0])/ 2)

    xbl = False
    ybl = False
    if x*2 != len(img):
        xbl = True
    if y*2 != len(img[0]):
        ybl = True



    liste = []
    

    if xbl and ybl:
        i = 8
        while i <= len(img):
            if i != len(img):
                j = len(img[0])
            else: j = 8

            while j <= len(img[0]):
                liste.append([i,j])
                j = j + 8
            i = i + 8
    else:
        if xbl:
            i = len(img)
            j = 8
            while j <= len(img[0]):
                liste.append([i,j])
                j = j + 8
        else:
            if ybl:
                i = 8
                j = len(img[0])
                while i <= len(img):
                    liste.append([i,j])
                    i = i + 8
        

    return liste

# unused
'''
def index_regions(img):
    x = closest_div8(img.size[0]/ 2)
    y = closest_div8(img.size[1]/ 2)
    region_1 = [0, 0, x, y ]
    region_2 = [0, y, x, img.size[1] ]
    region_3 = [x, 0, img.size[0], y ]
    region_4 = [x, img.size[1]/ 2, img.size[0], img.size[1] ]
    regions = [ region_1, region_2, region_3, region_4 ]

    return regions
    
    
    
    
    
def corner_insertion(mat,fx,fy):
    #print(fx)
    #print(fy)
    wtr_corner_mat = np.array(mat[fx:len(mat), fy:len(mat[0])])

    limit = int(len(wtr_corner_mat) / 8) * int(len(wtr_corner_mat[0]) / 8)
    rnd_it = iter(randm.rand_lst(245,limit))

    i = 8
    j = 8
    while i < len(wtr_corner_mat):
        j = 8
        while j < len(wtr_corner_mat[0]):
            key = next(rnd_it)  
            index_insertion(wtr_corner_mat,i,j,key)
            j = j + 8
        i = i + 8

    mat[fx:,fy:] = wtr_corner_mat'''
