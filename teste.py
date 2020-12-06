from utils import readDataset, createMap, filterBy, getDistinctSpecialtyArr
from guloso2 import gerarSolucaoInicial

dataset = readDataset('toy2.txt')

cirurgias = createMap(dataset)

cirurgiasP1 = filterBy(cirurgias, 'p', 1)

print(cirurgiasP1)


S = 2
T = 46
D = 5

solucaoInicial = gerarSolucaoInicial(cirurgias, S, T, D)

print(solucaoInicial)