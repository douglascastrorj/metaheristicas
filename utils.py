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


def getDistinctSpecialty(dataset):
    especialidadesDistintas = []
    for e in dataset['e']:
        if not e in especialidadesDistintas:
            especialidadesDistintas.append(e)
    
    return len(especialidadesDistintas)


def getPenalizacao(prioridade):
    if prioridade == 1:
        return 90
    if prioridade == 2:
        return 20
    if prioridade == 3:
        return 5
    if prioridade == 4:
        return 1

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