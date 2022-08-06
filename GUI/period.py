import random
from PIL import Image
from string import ascii_lowercase


def block_insert(blc,l, q, x, y):


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
    j2 = startQy
   
    for i in range(startL, l):
        j2 = 0
        for j in range(startQ, q):
            tmp = blc[i][j]
            blc[i][j] = blc[i2][j2]
            blc[i2][j2] = tmp
            j2 = j2 + 1
        i2 = i2 + 1


def position_list(x,y,height,width):
    pos_x = round (int(height * 0.3) / 2 ) * 2
    pos_y = round (int(width * 0.3) / 2 ) * 2

    
    if x + pos_x >= height:
        x_axis_pos = (x + pos_x) % height
    else:
        x_axis_pos = x + pos_x
    
    if y + pos_y >= width:
        y_axis_pos = (y + pos_y) % width
    else:
        y_axis_pos = y + pos_y

    if x - pos_x < 0:
        x_axis_neg = (x - 2 - pos_x) % height
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

    
    tmp = next(pos_it,None)
    while tmp != None:
        x, y = tmp
        if is_empty_blc(mat,x,y) == True:
            block_insert(mat,l,q,x,y)
            break
        tmp = next(pos_it,None)



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

    
 






it = iter(ascii_lowercase)
lost = []
i= 1
j= 0
while i < 4 :
    lost.append([])
    lost.append([])
    j = 0
    while j < 6:
        if j % 2 == 0:
            c = next(it)
        lost[i-1].append(c)
        lost[i].append(c)
        j = j + 1
    i = i + 2
        
for i in lost:
    print(i)
        


i = 2
j = 2
while i <= len(lost):
    j = 2
    while j <= len(lost[0]): 
        index_insertion(lost,i,j)
        j = j + 2
    i = i + 2

print("rslt")
for i in lost:
    print(i)
