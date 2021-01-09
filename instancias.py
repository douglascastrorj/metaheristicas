import sys
import random

#!
# N: numero de cirurgias
# H: numero de cirurgioes
# E: Numero de especialidades
# !#
def gerarInstancia(N=10, H=1, E=1, percentP1=0.15):

    cirurgias = {}
    for _id in range(1, N + 1):

        p = 1
        w = 0
        if _id > N * percentP1:
            p = random.randint(2,4)
            w = random.randint(0, 40)
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

def saveInstancia(cirurgias):
    path = 'output.csv'
    if len(sys.argv) > 1:
        path = sys.argv[1]
    f = open(path, 'w')

    f.write('c;p;w;e;h;tc\n')
    for c in cirurgias:
        cirurgia = cirurgias[c]
        f.write(f"{c};{cirurgia['p']};{cirurgia['w']};{cirurgia['e']};{cirurgia['h']};{cirurgia['tc']}\n")

    f.close()

if __name__ == "__main__":
    saveInstancia( gerarInstancia(N=200, H=40, E=8, percentP1=0.04) )