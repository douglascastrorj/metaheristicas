import pandas as pd
import numpy as np

def readDataset(path):
    df = pd.read_csv(path, delimiter=';')
    return df
    

def createDecisionVar(C, S, T, D, E):
    x = []
    for i in range(0, C):
        x.append([])
        for j in range(0, S):
            x[i].append([])
            for k in range(0, T):
                x[i][j].append([])
                for l in range(0,D):
                    x[i][j][k].append(0)
    
    xcstd = np.array(x)
    z = np.zeros(C)
    
    yesd = []
    for i in range(0, E):
        yesd.append([])
        for j in range(0, S):
            yesd[i].append([])
            for k in range(0, D):
                yesd[i][j].append(0)
    yesd = np.array(yesd)

    return xcstd, yesd, z

def createDecisionDict(cirurgias, S, T, D, E):
    x = {}
    z = {}
    for i in cirurgias:
        x[i] = {}
        for j in range(0, S):
            x[i][j] = {}
            for k in range(0, T):
                x[i][j][k] = {}
                for l in range(0,D):
                    x[i][j][k][l] = 0
    
    
        z[i] = 0
    
    yesd = {}
    for i in E:
        yesd[i] = {}
        for j in range(0, S):
            yesd[i][j] = {}
            for k in range(0, D):
                yesd[i][j][k] = 0


    return x, yesd, z


def getSurgeryByPriority(dataset, p):
    surgeries = []
    idx = 0
    for row in dataset['p']:
        if(row == p):
            surgeries.append(idx)
        idx = idx + 1
    
    return surgeries

def getSurgeriesBySpecialty(dataset, e):
    surgeries = []
    idx = 0
    for row in dataset['e']:
        if(row == e):
            surgeries.append(idx)
        idx = idx + 1
    
    return surgeries


def getHorasPorCirurgiao(solucao):
    horasPorCirurgiao = {}
    for c in solucao:
        if solucao[c]['alocada'] == False:
            continue

        cirurgiao = solucao[c]['cirurgiao']
        if cirurgiao not in list(horasPorCirurgiao.keys()):
            # print(f'cirurgiao : {cirurgiao}')
            horasPorCirurgiao[cirurgiao] = {
                'dia': {
                    0: 0,
                    1: 0,
                    2: 0,
                    3: 0,
                    4: 0
                },
                'horasSemana': 0
            }

           
        d = solucao[c]['dia']
        horasPorCirurgiao[cirurgiao]['dia'][d] += solucao[c]['duracao']
        horasPorCirurgiao[cirurgiao]['horasSemana'] += solucao[c]['duracao']
    return horasPorCirurgiao
        


def getDistinctSpecialtyArr(dataset):
    especialidadesDistintas = []
    for e in dataset['e']:
        if not e in especialidadesDistintas:
            especialidadesDistintas.append(e)
    
    return especialidadesDistintas

def getDistinctSpecialtyArr2(cirurgias):
    especialidadesDistintas = []
    for key in cirurgias:
        e = cirurgias[key]['e']
        if not e in especialidadesDistintas:
            especialidadesDistintas.append(e)
    return especialidadesDistintas

    
def getDistinctSpecialty(dataset):    
    return len(getDistinctSpecialtyArr(dataset))


def getPenalizacao(prioridade):
    if prioridade == 1:
        return 90
    if prioridade == 2:
        return 20
    if prioridade == 3:
        return 5
    if prioridade == 4:
        return 1

def createMap(dataset):
    _map = {}
    for indice in range(0, len(dataset['c'])):
        idCirurgia = dataset['c'][indice]
        cirurgia = {
            "c": idCirurgia,
            "p": dataset['p'][indice],
            "w": dataset['w'][indice],
            "e": dataset['e'][indice],
            "h": dataset['h'][indice],
            "tc": dataset['tc'][indice]
        }
        _map[idCirurgia] = cirurgia
    return _map


def createMedicSlotMap(cirurgias):
    medicSlotMap = {}
    for cirurgiaId in cirurgias:
        cirurgia = cirurgias[cirurgiaId]
        
        medicSlotMap[cirurgia['h']] = {
            'slotsDia': {
                0: 0,
                1: 0,
                2: 0,
                3: 0,
                4: 0,
            },
            'slotsSemana': 0
        }

    return medicSlotMap


# filtrar cirurgias do cirurgiao 2 de sexta-feira
# filterF = lambda cirurgia : cirurgia['cirurgiao'] == 2 & cirurgia['dia'] == 4
# cirurgiasC2SextaFeira = _filter(solucao, filterF)
def _filter(_map, filterFunction):
    _filtered = {}
    for key in _map:
        if filterFunction(_map[key]):
           _filtered[key] = _map[key] 
    return _filtered

def filterBy(_map, column, columnValue):
    _filtered = {}
    for key in _map:
        if column in _map[key]:
            if _map[key][column] == columnValue:
                _filtered[key] = _map[key]
    return _filtered

def filterNotBy(_map, column, columnValue):
    _filtered = {}
    for key in _map:
        if column in _map[key]:
            if _map[key][column] != columnValue:
                _filtered[key] = _map[key]
    return _filtered

def getCirurgia(dataset, indice):
    cirurgia = {
        "c": dataset['c'][indice],
        "p": dataset['p'][indice],
        "w": dataset['w'][indice],
        "e": dataset['e'][indice],
        "h": dataset['h'][indice],
        "tc": dataset['tc'][indice]
    }
    return cirurgia

def getIndexFromId(id):
    return id - 1

def getIdFromIndex(index):
    return index + 1

def createEspecialidadesSalaDia(S, D):
    e = []
    for i in range(0, S):
        e.append([])
        for j in range(0, D):
            e[i].append(0)
    
    return np.array(e)


def mapToList(map):
    lista = []
    for key in map:
        lista.append(map[key])
    return lista

#funciona para xcstd marcando 1 apenas no slot inicial
def xcstdToMap(xcstd, cirurgias):
    _map = {}
    for c in xcstd:
        for s in xcstd[c]:
            for t in xcstd[c][s]:
                for d in xcstd[c][s][t]:
                    if xcstd[c][s][t][d] == 1:
                        cirurgia = {
                            "id": c,
                            "sala": s,
                            "horaInicio": t,
                            "horaFim": t + cirurgias[c]['tc'] - 1,
                            "dia": d,
                            "duracao": cirurgias[c]['tc'],
                            "cirurgiao": cirurgias[c]['h'],
                            "diasEspera": cirurgias[c]['w'],
                            "prioridade": cirurgias[c]['p'],
                            "especialidade": cirurgias[c]['e'],
                            "alocada": True
                        }
                        _map[c] = cirurgia

    for c in cirurgias:
        if not c in _map:
            _map[c] = {
                            "id": c,
                            "sala": None,
                            "dia": None,
                            "duracao": cirurgias[c]['tc'],
                            "cirurgiao": cirurgias[c]['h'],
                            "diasEspera": cirurgias[c]['w'],
                            "prioridade": cirurgias[c]['p'],
                            "especialidade": cirurgias[c]['e'],
                            "alocada": False
                        }

    return _map

def overlap(cirurgia1, cirurgia2):
    if cirurgia1['sala'] == cirurgia2['sala']:
        if cirurgia1['horaInicio'] <= cirurgia2['horaInicio'] and cirurgia1['horaFim'] >= cirurgia2['horaInicio']:
            return True
        if cirurgia2['horaInicio'] <= cirurgia1['horaInicio'] and cirurgia2['horaFim'] >= cirurgia1['horaInicio']:
            return True
    else:
        if cirurgia1['horaInicio'] < cirurgia2['horaInicio'] and cirurgia1['horaFim'] > cirurgia2['horaInicio']:
            return True
        if cirurgia2['horaInicio'] < cirurgia1['horaInicio'] and cirurgia2['horaFim'] > cirurgia1['horaInicio']:
            return True
    
    return False


def ordenaCirurgias(cirurgias, compareF):    
    for i in range(0, len(cirurgias)):
        for j in range(0, len(cirurgias)):
            if compareF(cirurgias[i]) < compareF(cirurgias[j]):
                swap = cirurgias[j]
                cirurgias[j] = cirurgias[i]
                cirurgias[i] = swap
    return cirurgias

def desalocarCirurgia(solucao, cirurgiaId):
    solucao[cirurgiaId]['alocada'] = False
    solucao[cirurgiaId]['dia'] = None
    solucao[cirurgiaId]['sala'] = None
    del solucao[cirurgiaId]['horaInicio']
    del solucao[cirurgiaId]['horaFim']