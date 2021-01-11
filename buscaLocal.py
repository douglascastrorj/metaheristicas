import random 
import copy
import numpy as np
import math
from utils import filterBy, _filter, ordenaCirurgias, getPenalizacao, mapToList, getHorasPorCirurgiao

from fitness import viavel, FOCirurgiaIsolada

# sobreposicao de horario cirurgiao
# maximo horario cirurgiao
# sobreposicao de horario cirurgia
# manter especialidade da sala (a menos q sala so tenha uma cirurgia)
# periodo de higienizacao

def primeiraMelhoria(funcaoBusca, params):
    pass


def trocaCirurgiasMesmoDia(params):
    solucaoAnterior = copy.deepcopy(params['solucao'])
    solucao = copy.deepcopy(params['solucao'])

    D = params['D']
    d = random.randint(0, D)

    cirurgiasD = filterBy(solucaoAnterior, 'dia', d)
    # #print(list(cirurgiasD.keys()))
    if len(list(cirurgiasD.keys())) < 2:
        return solucaoAnterior
    
    c1 = random.choice(list(cirurgiasD.keys()))
    c2 = random.choice(list(cirurgiasD.keys()))

    solucao[c1]['horaInicio'] = solucaoAnterior[c2]['horaInicio']
    solucao[c1]['horaFim'] = solucaoAnterior[c2]['horaInicio'] + solucaoAnterior[c1]['duracao']
    solucao[c1]['sala'] = solucaoAnterior[c2]['sala']

    solucao[c2]['horaInicio'] = solucaoAnterior[c1]['horaInicio']
    solucao[c2]['horaFim'] = solucaoAnterior[c1]['horaInicio'] + solucaoAnterior[c2]['duracao']
    solucao[c2]['sala'] = solucaoAnterior[c1]['sala']

    return solucao

   

def trocaCirurgiasDiasDiferente(params):
    solucaoAnterior = copy.deepcopy(params['solucao'])
    solucao = copy.deepcopy(params['solucao'])

    D = params['D']

    cirurgiasD = {}
    for d in range(0, D):
        cd = filterBy(solucao, 'dia', d)
        if len(cd.keys()) > 0:
            cirurgiasD[d] = cd

    if len(cirurgiasD.keys()) < 2:
        # #print('nao existem cirurgias em dias diferentes')
        return solucao
    
    d1 = random.choice(list(cirurgiasD.keys()))
    d2 = random.choice( [d for d in list(cirurgiasD.keys()) if not d == d1] )


    c1 = random.choice(list(cirurgiasD[d1].keys()))
    c2 = random.choice(list(cirurgiasD[d2].keys()))

    solucao[c1]['horaInicio'] = solucaoAnterior[c2]['horaInicio']
    solucao[c1]['horaFim'] = solucaoAnterior[c2]['horaInicio'] + solucaoAnterior[c1]['duracao']
    solucao[c1]['dia'] = solucaoAnterior[c2]['dia']
    solucao[c1]['sala'] = solucaoAnterior[c2]['sala']

    solucao[c2]['horaInicio'] = solucaoAnterior[c1]['horaInicio']
    solucao[c2]['horaFim'] = solucaoAnterior[c1]['horaInicio'] + solucaoAnterior[c2]['duracao']
    solucao[c2]['dia'] = solucaoAnterior[c1]['dia']
    solucao[c2]['sala'] = solucaoAnterior[c1]['sala']

    # #print(f'\n\n c1 {c1} c2 {c2}\n\n')
    # #print(solucaoAnterior)
    # #print('\n- --------- -\n')
    # #print(solucao)

    return solucao

#inserindo apenas uma por enquanto
#sortear cirurgia a ser inserida de forma gulosa com base em um alpha (0 = totalmente aleatorio, 1 = totalmente guloso)
def insercaoDeUmaOuMaisCirurgiasDaListaEspera(params):
    solucao = copy.deepcopy(params['solucao'])

    idsCirurgiasNaoAlocadas = [c for c in solucao.keys() if solucao[c]['alocada'] == False]

    if len(idsCirurgiasNaoAlocadas) == 0:
        return solucao
    
    cirurgias_ = mapToList(params['solucao'])
    cirurgias_ = [ c for c in cirurgias_ if c['alocada'] == False ]

    #print(cirurgias_)
    
    compareF = lambda cirurgia : float(cirurgia['prioridade']) / ((cirurgia['diasEspera'] * getPenalizacao(cirurgia['prioridade'])) + 0.1)
    cirurgias_ = ordenaCirurgias(cirurgias_, compareF)

    # print(cirurgias_)
    # random.shuffle(cirurgias_)
    maxPos = max( int(len(cirurgias_) * (1 - params['alpha'])),  1)
    # #print(maxPos)
    cirurgias_ = cirurgias_[: maxPos]
    
    # #print(cirurgias_, idsCirurgiasNaoAlocadas)
  
    cirurgiaEscolhida = random.choice(cirurgias_)
    # print('cirurgiaEscolhida ', cirurgiaEscolhida)

    for d in range(0, params['D']):
        for s in range(0, params['S']):
            # print('d - s :', d , s)
            filterF = lambda cirurgia : cirurgia['dia'] == d and cirurgia['sala'] == s
            cirurgiasDiaSala = _filter(solucao, filterF)
            cirurgiasDiaSala = mapToList(cirurgiasDiaSala)
            getValor = lambda cirurgia : cirurgia['horaFim']
            cirurgiasDiaSala = ordenaCirurgias(cirurgiasDiaSala, getValor)
            
            inicio = 0
            fim =  cirurgiaEscolhida['duracao'] - 1
            if len(cirurgiasDiaSala) > 0:
                ultimaDoDiaSala = cirurgiasDiaSala[len(cirurgiasDiaSala) - 1]
                inicio = ultimaDoDiaSala['horaFim'] + 3
                fim = ultimaDoDiaSala['horaFim'] + 3 + cirurgiaEscolhida['duracao'] - 1

            cirurgia = {
                            "id": cirurgiaEscolhida['id'],
                            "sala": s,
                            "horaInicio": inicio,
                            "horaFim": fim,
                            "dia": d,
                            "duracao": cirurgiaEscolhida['duracao'],
                            "cirurgiao": cirurgiaEscolhida['cirurgiao'],
                            "diasEspera": cirurgiaEscolhida['diasEspera'],
                            "prioridade": cirurgiaEscolhida['prioridade'],
                            "especialidade": cirurgiaEscolhida['especialidade'],
                            "alocada": True
                        }
            
            solucao[cirurgia['id']] = cirurgia

            # print('inicio fim ', inicio, fim)
            if viavel(solucao, params['S'], params['T'], params['D']) == False:
                solucao = params['solucao']
                continue

            # #print('busca local ', cirurgia)
            return solucao
            #se puder adicionar cirurgia adiciona e retorna


    return params['solucao']



def insercaoDeUmaOuMaisCirurgiasDaListaEspera2(params):
    solucao = copy.deepcopy(params['solucao'])
    
    naoAlocadas = filterBy(solucao, 'alocada', False)

    if len(naoAlocadas) == 0:
        return solucao
    
    c = random.choice(list(naoAlocadas.keys()))

    diaInicial = 0
    if solucao[c]['prioridade'] > 1:
        diaInicial = 1

    for s in range(0, params['S']):
        for d in range(diaInicial, params['D']):
            # nao tentar alocar p1 em outros dias
            if solucao[c]['prioridade'] == 1 and d > 0:
                return solucao

            for t in range(0, params['T']):
                alocarCirurgia(solucao, c, s, t, d)
                if viavel(solucao, params['S'], params['T'], params['D']) == False:
                    desalocarCirurgia(solucao, c)
                else:
                    # print(f'INSERCAO CIRURGIA {c}- SALA {s} SLOT {t} DIA {d}')
                    return solucao


    return solucao

def insereEmSalaDiaOcioso(params):
    solucao = copy.deepcopy(params['solucao'])
    
    naoAlocadas = filterBy(solucao, 'alocada', False)

    if len(naoAlocadas) == 0:
        return solucao
    
    c = random.choice(list(naoAlocadas.keys()))
    tempoSalas = np.zeros((params['S'], params['D']))

    for s in range(0, params['S']):
        for d in range(0, params['D']):
            filterAlocadasDiaSala = lambda cirurgia : cirurgia['alocada'] == True and  cirurgia['dia'] == d  and cirurgia['sala'] == s
            alocadasDiaSala = _filter(solucao, filterAlocadasDiaSala)
            for c in alocadasDiaSala:
                tempoSalas[s][d] += alocadasDiaSala[c]['duracao']

    lista = []     
    for s in range(0, params['S']):
        for d in range(0, params['D']):
            lista.append({'sala': s, 'dia': d, 'slotsOcupados': tempoSalas[s][d] })
    
    listaOrdenada = sorted(lista, key=lambda item: item['slotsOcupados'])
    sliceIndex = math.ceil(len(listaOrdenada) / 2) 

    listaCortada = listaOrdenada[:sliceIndex]
    
    item = random.choice(listaCortada)

    d = item['dia']
    s = item['sala']

    for t in range(0, params['T'] - solucao[c]['duracao'] ):
        alocarCirurgia(solucao, c, s, t, d)
        if viavel(solucao, params['S'], params['T'], params['D']) == False:
            desalocarCirurgia(solucao, c)
        else:
            # print(f'INSERCAO CIRURGIA {c}- SALA {s} SLOT {t} DIA {d}')
            return solucao

    return solucao

#sortear cirurgia a ser inserida de forma gulosa com base em um alpha (0 = totalmente aleatorio, 1 = totalmente guloso)
def removeCirurgias(params):
    solucao = copy.deepcopy(params['solucao'])

    alocadas = filterBy(solucao, 'alocada', True)

    if len(alocadas) == 0:
        return solucao

    cirurgias_ = mapToList(alocadas)
    compareF = lambda cirurgia : float(cirurgia['prioridade']) / ((cirurgia['diasEspera'] * getPenalizacao(cirurgia['prioridade'])) + 0.1)
    cirurgias_ = ordenaCirurgias(cirurgias_, compareF)
    cirurgias_.reverse()

    maxPos = max( int(len(cirurgias_) * (1 - params['alpha'])),  1)
    cirurgias_ = cirurgias_[: maxPos]
    
    # #print(cirurgias_, idsCirurgiasNaoAlocadas)
  
    cirurgiaEscolhida = random.choice(cirurgias_)
    cirurgiaAlocada = cirurgiaEscolhida['id']

    # print(f'cirurgia {cirurgiaAlocada} removida')

    solucao[cirurgiaAlocada]['dia'] = None
    solucao[cirurgiaAlocada]['sala'] = None
    solucao[cirurgiaAlocada]['horaInicio'] = None
    solucao[cirurgiaAlocada]['horaFim'] = None
    solucao[cirurgiaAlocada]['alocada'] = False

    return solucao 

def trocaCirurgiaMarcadaPorCirurgiaListaEspera(params):
    solucao = copy.deepcopy(params['solucao'])

    alocadas = filterBy(solucao, 'alocada', True)
    naoAlocadas = filterBy(solucao, 'alocada', False)

    if len(alocadas) == 0 or len(naoAlocadas) == 0:
        return solucao

    cirurgiaAlocada = random.choice(list(alocadas.keys()))
    cirurgiaNaoAlocada = random.choice(list(naoAlocadas.keys()))

    solucao[cirurgiaNaoAlocada]['dia'] = solucao[cirurgiaAlocada]['dia']
    solucao[cirurgiaNaoAlocada]['sala'] = solucao[cirurgiaAlocada]['sala']
    solucao[cirurgiaNaoAlocada]['horaInicio'] = solucao[cirurgiaAlocada]['horaInicio']
    solucao[cirurgiaNaoAlocada]['horaFim'] = solucao[cirurgiaAlocada]['horaInicio'] + solucao[cirurgiaNaoAlocada]['duracao'] - 1
    solucao[cirurgiaNaoAlocada]['alocada'] = True

    solucao[cirurgiaAlocada]['dia'] = None
    solucao[cirurgiaAlocada]['sala'] = None
    solucao[cirurgiaAlocada]['horaInicio'] = None
    solucao[cirurgiaAlocada]['horaFim'] = None
    solucao[cirurgiaAlocada]['alocada'] = False


    return solucao

def realocarHorario(params):
    solucao = copy.deepcopy(params['solucao'])

    alocadas = filterBy(solucao, 'alocada', True)
    if len(alocadas) == 0:
        return solucao

    cirurgiaEscolhida = random.choice(list(alocadas.keys()))
    deslocamento = random.randint(1, 10)
    direcao = random.choice([1, -1])

    solucao[cirurgiaEscolhida]['horaInicio'] += deslocamento * direcao
    solucao[cirurgiaEscolhida]['horaFim'] += deslocamento * direcao  

    return solucao

def realocarDia(params):
    solucao = copy.deepcopy(params['solucao'])

    alocadas = filterBy(solucao, 'alocada', True)
    if len(alocadas) == 0:
        return solucao

    cirurgiaEscolhida = random.choice(list(alocadas.keys()))
    deslocamento = random.randint(1, 25)
    direcao = random.choice([1, -1])

    solucao[cirurgiaEscolhida]['dia'] += (deslocamento * direcao) % params['D']

    return solucao


def trocaP1PorD0(params):
    solucao = copy.deepcopy(params['solucao'])

    filterP1NaoAlocadas = lambda cirurgia : cirurgia['prioridade'] == 1 and cirurgia['alocada'] == False
    naoAlocadasP1 = _filter(solucao, filterP1NaoAlocadas)

    if len(naoAlocadasP1) == 0:
        return solucao

    filterAlocadasD0 = lambda cirurgia : cirurgia['dia'] == 0 and cirurgia['alocada'] == True and cirurgia['prioridade'] != 1
    alocadasD0 = _filter(solucao, filterAlocadasD0)

    if len(alocadasD0) == 0:
        return solucao

    cP1 = random.choice(list(naoAlocadasP1.keys()))
    c2 = random.choice(list(alocadasD0.keys()))

    solucao[cP1]['dia'] = solucao[c2]['dia']
    solucao[cP1]['sala'] = solucao[c2]['sala']
    solucao[cP1]['horaInicio'] = solucao[c2]['horaInicio']
    solucao[cP1]['horaFim'] = solucao[c2]['horaInicio'] + solucao[cP1]['duracao'] - 1
    solucao[cP1]['alocada'] = True

    solucao[c2]['dia'] = None
    solucao[c2]['sala'] = None
    solucao[c2]['horaInicio'] = None
    solucao[c2]['horaFim'] = None
    solucao[c2]['alocada'] = False

    return solucao


def desalocaNaoP1D0(params):
    solucao = copy.deepcopy(params['solucao'])

    filterNaoP1D0 = lambda cirurgia : cirurgia['alocada'] == True and cirurgia['dia'] == 0  and cirurgia['prioridade'] != 1
    naoP1D0 = _filter(solucao, filterNaoP1D0)

    if len(naoP1D0) == 0:
        return solucao

    c = random.choice(list(naoP1D0.keys()))

    solucao[c]['dia'] = None
    solucao[c]['sala'] = None
    solucao[c]['horaInicio'] = None
    solucao[c]['horaFim'] = None
    solucao[c]['alocada'] = False

    return solucao 


def trocaCirurgiaMarcadaPorDuasCirurgiasListaEspera(params):
    solucao = copy.deepcopy(params['solucao'])
    return solucao

def trocaDuasCirurgiasMarcadasPorUmaCirurgiaListaEspera(params):
    solucao = copy.deepcopy(params['solucao'])
    return solucao

def trocaDuasCirurgiasMarcadasPorDuasCirurgiasListaEspera(params):
    solucao = copy.deepcopy(params['solucao'])
    return solucao

def trocaDuasFimSemanaPorUmaInicioSemana(params):
    solucao = copy.deepcopy(params['solucao'])
    return solucao


def removeOciosidadeCirurgiao(params):
    solucaoCpy = copy.deepcopy(params['solucao'])

    horasCirurgioesSolucaoElite = getHorasPorCirurgiao(solucaoCpy)
    filterF = lambda cirurgiao : cirurgiao['horasSemana'] < 80
    horasCirurgioesSolucaoElite = _filter(horasCirurgioesSolucaoElite, filterF)
    # print(horasCirurgioesSolucaoElite)

    cirurgiao = random.choice(list(horasCirurgioesSolucaoElite.keys()))

    filterF = lambda cirurgia : cirurgia['alocada'] == False and cirurgia['cirurgiao'] == cirurgiao
    cirurgiasDoCirurgiao = _filter(solucaoCpy, filterF)

    if len(cirurgiasDoCirurgiao) == 0:
        return solucaoCpy

    c = random.choice(list(cirurgiasDoCirurgiao.keys()))

    if solucaoCpy[c]['cirurgiao'] == cirurgiao:
        for d in range(0, params['D']):
            for s in range(0, params['S']):
                for t in range(0, params['T'] - solucaoCpy[c]['duracao']):
                    if solucaoCpy[c]['alocada'] == True:
                        continue
                    alocarCirurgia(solucaoCpy, c, s, t, d)
                    if viavel(solucaoCpy, params['S'], params['T'], params['D'] ) == False:
                        desalocarCirurgia(solucaoCpy, c)
                    else:
                        # print('BUSCA LOCAL conseguiu alocar cirurgia de cirurgiao ocioso')
                        # print(f'Cirurgia {c} Cirurgiao {cirurgiao}')
                        return solucaoCpy
                        

    return solucaoCpy

def antecipaPrioridadeMaisBaixa(params):

    # print('antecipa cirurgia mais baixa')
    solucao = copy.deepcopy(params['solucao'])
    solucaoAnterior = copy.deepcopy(params['solucao'])

    filterAlocadasNaoP1 = lambda cirurgia : cirurgia['alocada'] == True and cirurgia['prioridade'] != 1
    alocadasNaoP1 = _filter(solucao, filterAlocadasNaoP1)

    if len(alocadasNaoP1) == 0:
        return solucao

    c1 = random.choice(list(alocadasNaoP1.keys()))

    filterPrioridadeMaissBaixa = lambda cirurgia : cirurgia['alocada'] == True and cirurgia['prioridade'] != 1 and cirurgia['prioridade'] >= solucao[c1]['prioridade'] and cirurgia['especialidade'] == solucao[c1]['especialidade'] and cirurgia['dia'] < solucao[c1]['dia']
    prioridadesMaisBaixa = _filter(solucao, filterPrioridadeMaissBaixa)

    if len(prioridadesMaisBaixa) == 0:
        return solucao

    c2 = random.choice(list(prioridadesMaisBaixa.keys()))

    solucao[c1]['horaInicio'] = solucaoAnterior[c2]['horaInicio']
    solucao[c1]['horaFim'] = solucaoAnterior[c2]['horaInicio'] + solucaoAnterior[c1]['duracao']
    solucao[c1]['dia'] = solucaoAnterior[c2]['dia']
    solucao[c1]['sala'] = solucaoAnterior[c2]['sala']

    solucao[c2]['horaInicio'] = solucaoAnterior[c1]['horaInicio']
    solucao[c2]['horaFim'] = solucaoAnterior[c1]['horaInicio'] + solucaoAnterior[c2]['duracao']
    solucao[c2]['dia'] = solucaoAnterior[c1]['dia']
    solucao[c2]['sala'] = solucaoAnterior[c1]['sala']

    if viavel(solucao, params['S'], params['T'], params['D'] ) == False:
        return solucaoAnterior

    return solucao

def antecipaFOMaisBaixa(params):

    # print('antecipa cirurgia mais baixa')
    solucao = copy.deepcopy(params['solucao'])
    solucaoAnterior = copy.deepcopy(params['solucao'])

    filterAlocadasNaoP1 = lambda cirurgia : cirurgia['alocada'] == True and cirurgia['prioridade'] != 1
    alocadasNaoP1 = _filter(solucao, filterAlocadasNaoP1)

    if len(alocadasNaoP1) == 0:
        return solucao

    c1 = random.choice(list(alocadasNaoP1.keys()))

    foc1 = FOCirurgiaIsolada(solucao[c1])
    filterPrioridadeMaissBaixa = lambda cirurgia : cirurgia['alocada'] == True and cirurgia['prioridade'] != 1 and cirurgia['especialidade'] == solucao[c1]['especialidade'] and cirurgia['dia'] < solucao[c1]['dia'] and FOCirurgiaIsolada(cirurgia) < foc1
    prioridadesMaisBaixa = _filter(solucao, filterPrioridadeMaissBaixa)

    if len(prioridadesMaisBaixa) == 0:
        return solucao

    c2 = random.choice(list(prioridadesMaisBaixa.keys()))

    solucao[c1]['horaInicio'] = solucaoAnterior[c2]['horaInicio']
    solucao[c1]['horaFim'] = solucaoAnterior[c2]['horaInicio'] + solucaoAnterior[c1]['duracao']
    solucao[c1]['dia'] = solucaoAnterior[c2]['dia']
    solucao[c1]['sala'] = solucaoAnterior[c2]['sala']

    solucao[c2]['horaInicio'] = solucaoAnterior[c1]['horaInicio']
    solucao[c2]['horaFim'] = solucaoAnterior[c1]['horaInicio'] + solucaoAnterior[c2]['duracao']
    solucao[c2]['dia'] = solucaoAnterior[c1]['dia']
    solucao[c2]['sala'] = solucaoAnterior[c1]['sala']

    if viavel(solucao, params['S'], params['T'], params['D'] ) == False:
        return solucaoAnterior

    return solucao

# funcoes auxiliares

def alocarCirurgia(solucao, idCirurgia, s, t, d):
    solucao[idCirurgia]['dia'] = d
    solucao[idCirurgia]['sala'] = s
    solucao[idCirurgia]['horaInicio'] = t
    solucao[idCirurgia]['horaFim'] = t + solucao[idCirurgia]['duracao']
    solucao[idCirurgia]['alocada'] = True


def desalocarCirurgia(solucao, idCirurgia):
    solucao[idCirurgia]['dia'] = None
    solucao[idCirurgia]['sala'] = None
    solucao[idCirurgia]['horaInicio'] = None
    solucao[idCirurgia]['horaFim'] = None
    solucao[idCirurgia]['alocada'] = False