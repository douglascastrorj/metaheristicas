from utils import readDataset, createMap, filterBy, getDistinctSpecialtyArr
from guloso2 import gerarSolucaoInicial
import json

S = 1
T = 46
D = 5

dataset = readDataset('toy2.txt')
cirurgias = createMap(dataset)

solucaoInicial, yesd, z = gerarSolucaoInicial(cirurgias, S, D, verbose=True)

print(solucaoInicial)

print('\n')
print(z)