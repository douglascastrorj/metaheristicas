import random 
import copy

from utils import filterBy

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

    # print(Xcstd)

    return Xcstd

def trocaCirurgiasDiasDiferente(_solucao, D):
    solucao = copy.deepcopy(_solucao)

    cirurgiasD = {}
    for d in range(0, D):
        cd = filterBy(solucao, 'dia', d)
        if len(cd.keys()) > 0:
            cirurgiasD[d] = cd

    if len(cirurgiasD.keys()) < 2:
        print('nao existem cirurgias em dias diferentes')
        return solucao
    
    d1 = random.choice(list(cirurgiasD.keys()))
    d2 = random.choice( [d for d in list(cirurgiasD.keys()) if not d == d1] )


    c1 = random.choice(list(cirurgiasD[d1].keys()))
    c2 = random.choice(list(cirurgiasD[d2].keys()))

    solucao[c1]['horaInicio'] = _solucao[c2]['horaInicio']
    solucao[c1]['horaFim'] = _solucao[c2]['horaInicio'] + _solucao[c1]['duracao']
    solucao[c1]['dia'] = _solucao[c2]['dia']
    solucao[c1]['sala'] = _solucao[c2]['sala']

    solucao[c2]['horaInicio'] = _solucao[c1]['horaInicio']
    solucao[c2]['horaFim'] = _solucao[c1]['horaInicio'] + _solucao[c2]['duracao']
    solucao[c2]['dia'] = _solucao[c1]['dia']
    solucao[c2]['sala'] = _solucao[c1]['sala']

    print(f'\n\n c1 {c1} c2 {c2}\n\n')
    print(_solucao)
    print('\n- --------- -\n')
    print(solucao)

    return solucao

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