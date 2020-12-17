from utils import filterNotBy, getPenalizacao

def fitnessFunction( cirurgias, S, T, D, Xcstd, z):

    cirurgiasNaoP1 = filterNotBy(cirurgias, 'p', 1)

    fo = 0

    for c in cirurgias:
        cirurgia = cirurgias[c]
        wc = cirurgia['w']
        for s in range(0, S):
            for t in range(0,T):
                xcst1 = Xcstd[c][s][t][0]
                fo += (wc + 3)*xcst1 * cirurgia['tc']

                # print(fo)

    for c in cirurgiasNaoP1:
        cirurgia = cirurgiasNaoP1[c]
        wc = cirurgia['w']
        for s in range(0, S):
            for t in range(0, T):
                for d in range(0, D):
                    xcstd = Xcstd[c][s][t][d]
                    fo += (wc + 2 + (d + 1))*xcstd * cirurgia['tc'] # nosso d vai de 0 a 4
        pc = cirurgia['p']
        Epc = getPenalizacao(pc)
        fo += pc * Epc * z[c]

    return fo

def fitnessFunction2( cirurgias, S, T, D, Xcstd, z):

    cirurgiasNaoP1 = filterNotBy(cirurgias, 'p', 1)

    fo = 0

    for c in cirurgias:
        cirurgia = cirurgias[c]
        wc = cirurgia['w']
        for s in range(0, S):
            for t in range(0,T):
                xcst1 = Xcstd[c][s][t][0]
                fo += (wc + 3)*xcst1

        pc = cirurgia['p']
        Epc = getPenalizacao(pc)
        fo += pc * Epc * z[c]

    for c in cirurgiasNaoP1:
        cirurgia = cirurgiasNaoP1[c]
        wc = cirurgia['w']
        for s in range(0, S):
            for t in range(0, T):
                for d in range(0, D):
                    xcstd = Xcstd[c][s][t][d]
                    fo += (wc + 2 + (d + 1))*xcstd # nosso d vai de 0 a 4
        

    return fo