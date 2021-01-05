import sys
import random

#!
# N: numero de cirurgias
# H: numero de cirurgioes
# E: Numero de especialidades
# !#
def gerarInstancia(N=10, H=1, E=1, percentP1=0.1):

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
    saveInstancia( gerarInstancia(N=50, H=10, E=4) )