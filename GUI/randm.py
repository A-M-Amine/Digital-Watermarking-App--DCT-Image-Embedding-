import random

def my_rand_8():
    return 8 * random.random()


def rand_lst(key,limit):
    lst = []
    random.seed(key)
    for i in range(limit):
        val = int(999 * random.random())
        lst.append(val)

    return lst


def seed_gen(key):

    random.seed(key)
    liste = []

    while len(liste) < 64:
        elt = [int(my_rand_8()), int(my_rand_8())]
        if elt not in liste:
            liste.append(elt)

    return liste


# liste aleatoire des index du blocs 8x8 
def block_index_rand(img, sx, sy, height, width, key):

    index_lst = []
    for i in range(sx, height, 8):
        for j in range(sy, width, 8):
            index_lst.append([i + 8, j + 8])

    random.seed(key)
    random.shuffle(index_lst)
    return index_lst
