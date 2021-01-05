import random

#!
# N: numero de cirurgias
# H: numero de cirurgioes
# E: Numero de especialidades
# !#
def gerarInstancia(N=10, H=1, E=1, percentP1=0.1 ):

    cirurgias = {}
    for _id in range(1, N + 1):

        p = 1
        if _id > N * percentP1:
            p = random.randint(2,4)
            
        w = random.randint(1, 10)
        e = random.randint(1, E)
        h = random.randint(1, H)
        tc = random.randint(5, 15)

        cirurgias[_id] = {
            "c": _id,
            "w": w,
            "e": e,
            "h": h,
            "tc": tc,
            "p": p
        }
    
    return cirurgias