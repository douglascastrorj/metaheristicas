import random 


# sobreposicao de horario cirurgiao
# maximo horario cirurgiao
# sobreposicao de horario cirurgia
# manter especialidade da sala (a menos q sala so tenha uma cirurgia)
# periodo de higienizacao

def primeiraMelhoria(funcaoBusca, params):
    pass


def trocaCirurgiasMesmoDia(Xcstd, cirurgias, d):
    cirurgiasDoDiaD = []
    print(f'Dia sorteado {d}')
    for c in Xcstd:
        for s in Xcstd[c]:
            for t in Xcstd[c][s]:
                if(Xcstd[c][s][t][d] == 1):
                    cirurgiaAgendada = {
                        'c': c,
                        'tc': t,
                        's': s
                    }
                    cirurgiasDoDiaD.append(cirurgiaAgendada)
    
    c1 = random.choice(cirurgiasDoDiaD)
    c2 = random.choice(cirurgiasDoDiaD)

    c1c = c1['c']
    c1s = c1['s']
    c1t = c1['tc']

    c2c = c2['c']
    c2s = c2['s']
    c2t = c2['tc']

    print(f'cirurgias Sorteadas {c1} - {c2}')

    Xcstd[c1c][c1s][c1t][d] = 0
    Xcstd[c2c][c2s][c2t][d] = 0

    Xcstd[c1c][c2s][c2t][d] = 1
    Xcstd[c2c][c1s][c1t][d] = 1




    print(Xcstd)

    return Xcstd

def trocaCirurgiasDiasDiferente(Xcstd):

    return Xcstd

def insercaoDeUmaOuMaisCirurgiasDaListaEspera(Xcstd, cirurgias):

    return Xcstd


def trocaCirurgiaMarcadaPorCirurgiaListaEspera(Xcstd, cirurgias):

    return Xcstd

def trocaCirurgiaMarcadaPorDuasCirurgiasListaEspera(Xcstd, cirurgias):

    return Xcstd

def trocaDuasCirurgiasMarcadasPorUmaCirurgiaListaEspera(Xcstd, cirurgias):

    return Xcstd

def trocaDuasCirurgiasMarcadasPorDuasCirurgiasListaEspera(Xcstd, cirurgias):

    return Xcstd

def trocaDuasFimSemanaPorUmaInicioSemana(Xcstd, cirurgias):

    return Xcstd