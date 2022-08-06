
def int_to_bin_2(num,bit):
    
    frm = '{0:0'+str(bit - 1)+'b}'
    frm1 = '{0:0'+str(bit)+'b}'
    cond = len(str(frm.format(num)))
    if num < 0: cond = cond - 1

    if cond > bit - 1:
        if num >= 0:
            res = "0" + "1" * (bit - 1)
        else:
            res = "1" + "1" * (bit - 1)
    else:
        if num >= 0:
            res = frm1.format(num)
        else:
            res = '1' + frm.format(-num)
    
    return res


def bin_to_int_2(num):

    if num[0] == '1':
        return -int(num[1:],2)
    return int(num,2)



