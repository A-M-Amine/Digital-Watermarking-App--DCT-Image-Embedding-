from binary_encd import bin_to_int_2, int_to_bin_2
from scipy.fftpack import dct, idct
import numpy as np


# implementation de 2D DCT
def dct2(a):
    return dct(dct(a.T, norm='ortho').T, norm='ortho')


# implementation de l'inverse 2D DCT
def idct2(a):
    return idct(idct(a.T, norm='ortho').T, norm='ortho')


# Encodage sur 64 bit de bloc 8x8 aprés l'implementation du DCT avec quantification 50% (11 permeirs valeurs)   
def block_gen(blc,l,q):

    if l == 8:
            startL = 0
    else:
        startL = l - 8
    if q == 8:
        startQ = 0
    else:
        startQ = q - 8
    
    code = ""
    dct_blc = np.array(blc[startL:l, startQ:q])
    dct_blc = dct2(dct_blc)
    zigzag_quant(dct_blc)
    dct_it = iter(zigzag(dct_blc))
    encd_it = iter(mat_encd_64b())

    for i in range(11):
        number = int(next(dct_it))
        bits = next(encd_it)
        code  = code + int_to_bin_2(number,bits)
    

    return code





# matrice de quantification jpeg avec une qualité de 50 %
def matrice_quantification():
    
    mat_quant = [
        [16,11,	10,	16,	24,	40,	51,	61],
        [12,12,	14,	19,	26,	58,	60,	55],
        [14,13,	16,	24,	40,	57,	69,	56],
        [14,17,	22,	29,	51,	87,	80,	62],
        [18,22,	37,	56,	68,	109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
    ]

    return mat_quant


# matrice d'encodage 64 bit
def mat_encd_64b():

    L=[7, 7, 7, 6, 6, 7, 5, 5, 5, 5, 4]

    return L


def decode_64b(code):
    vect = []
    encd_it = iter(mat_encd_64b())
    strt = 0
    tmp = next(encd_it,None)
    end = tmp
    while tmp != None:
        number = code[strt:end]
        strt = end
        
        vect.append(bin_to_int_2(number))
        tmp = next(encd_it,None)
        if tmp != None:
            end = end + tmp
    
    z =[0 for i in range(53)]
    vect.extend(z)
    blc = inverse_zigzag(vect,8,8)
    
    return blc




def quantification(mat):

    matQ = matrice_quantification()
    res = []
    for i in range(8):
        res.append([])
        for j in range(8):
            x = mat[i][j] / matQ[i][j]
            res[i].append(np.uint8(x))

    return res

def de_quantification(mat):

    matQ = matrice_quantification()
    res = []
    for i in range(8):
        res.append([])
        for j in range(8):
            x = mat[i][j] * matQ[i][j]
            res[i].append(x)

    return res

def quant_11(mat):

    matQ = matrice_quantification()
    res = []
    for i in range(8):
        res.append([])
        for j in range(8):
            x = mat[i][j] / matQ[i][j]
            res[i].append(np.uint8(x))

    return res

def check(mat):
    lst = zigzag(mat)
    for i in range(11):
        if lst[i] < 0 and i == 0:
            print("pos " + str(i)  +" : "+ str(int(lst[i])))


def center_mat(mat):
    for i in range(8):
        for j in range(8):
            mat[i, j] = mat[i, j] - 128



def reverse_center_mat(mat):
    for i in range(8):
        for j in range(8):
            mat[i, j] = mat[i, j] + 128



def zigzag(M):
    i = 0
    j = 0
    maxI = 7
    maxJ = 7
    croiss = 0
    Lzig=[]
    while (i <= maxI) and (j <= maxJ):

        Lzig.append(M[i][j])
        if (i == 0 or i == maxI) :
            if j==maxJ:
                j-=1
                i+=1
            j+=1
            Lzig.append(M[i][j])
        elif (j==0) or (j==maxJ):
                if i==maxI:
                  i-=1
                  j+=1
                i+=1
                Lzig.append(M[i][j])
        if(i==0) or (j==maxJ): croiss=0
        if(j==0) or (i==maxI): croiss=1
        if croiss==1:
            i=i-1
            j=j+1
        else :
            i=i+1
            j=j-1 
    return Lzig


def inverse_zigzag(input, vmax, hmax):
	
	
	h = 0
	v = 0

	vmin = 0
	hmin = 0

	output = np.zeros((vmax, hmax))

	i = 0
	while ((v < vmax) and (h < hmax)): 
		if ((h + v) % 2) == 0:                 
			if (v == vmin):
				output[v, h] = input[i]        

				if (h == hmax):
					v = v + 1
				else:
					h = h + 1                        

				i = i + 1

			elif ((h == hmax -1 ) and (v < vmax)):   
				
				output[v, h] = input[i] 
				v = v + 1
				i = i + 1

			elif ((v > vmin) and (h < hmax -1 )):    
				
				output[v, h] = input[i] 
				v = v - 1
				h = h + 1
				i = i + 1

		else:                                   

			if ((v == vmax -1) and (h <= hmax -1)):       
				#print(4)
				output[v, h] = input[i] 
				h = h + 1
				i = i + 1
        
			elif (h == hmin):                 
				output[v, h] = input[i] 
				if (v == vmax -1):
					h = h + 1
				else:
					v = v + 1
				i = i + 1
        		        		
			elif((v < vmax -1) and (h > hmin)):    
				output[v, h] = input[i] 
				v = v + 1
				h = h - 1
				i = i + 1

		if ((v == vmax-1) and (h == hmax-1)):               	
			output[v, h] = input[i] 
			break


	return output.astype(int)

def zigzag_quant(M):
    i = 0
    j = 0
    maxI = 7
    maxJ = 7
    croiss = 0
    cpt = 0 
    Q = matrice_quantification()
    while (i <= maxI) and (j <= maxJ):

        if cpt < 11:
            M[i][j] = int(M[i][j] / Q[i][j])
            cpt = cpt + 1
        else: break
        if (i == 0 or i == maxI) :
            if j==maxJ:
                j-=1
                i+=1
            j+=1
            if cpt < 11:
                M[i][j] = int(M[i][j] / Q[i][j])
                cpt = cpt + 1
            else: break
        elif (j==0) or (j==maxJ):
                if i==maxI:
                  i-=1
                  j+=1
                i+=1
                if cpt < 11:
                    M[i][j] = int(M[i][j] / Q[i][j])
                    cpt = cpt + 1
                else: break
        if(i==0) or (j==maxJ): croiss=0
        if(j==0) or (i==maxI): croiss=1
        if croiss==1:
            i=i-1
            j=j+1
        else :
            i=i+1
            j=j-1 


def reverse_zigzag_quant(M):
    i = 0
    j = 0
    maxI = 7
    maxJ = 7
    croiss = 0
    cpt = 0 
    Q = matrice_quantification()
    while (i <= maxI) and (j <= maxJ):

        if cpt < 11:
            M[i][j] = M[i][j] * Q[i][j]
            cpt = cpt + 1
        else: break
        if (i == 0 or i == maxI) :
            if j==maxJ:
                j-=1
                i+=1
            j+=1
            if cpt < 11:
                M[i][j] = M[i][j] * Q[i][j]
                cpt = cpt + 1
            else: break
        elif (j==0) or (j==maxJ):
                if i==maxI:
                  i-=1
                  j+=1
                i+=1
                if cpt < 11:
                    M[i][j] = M[i][j] * Q[i][j]
                    cpt = cpt + 1
                else: break
        if(i==0) or (j==maxJ): croiss=0
        if(j==0) or (i==maxI): croiss=1
        if croiss==1:
            i=i-1
            j=j+1
        else :
            i=i+1
            j=j-1 

