from utils import readDataset, createMap, filterBy, getDistinctSpecialtyArr
from guloso2 import gerarSolucaoInicial
import json

S = 2
T = 46
D = 5

dataset = readDataset('toy.txt')
cirurgias = createMap(dataset)

solucaoInicial, yesd, z = gerarSolucaoInicial(cirurgias, S, D, verbose=True)

print(solucaoInicial)

print('\n')
print(z)

# implementar metodo de busca local
#   - verificar se solucao é viavel
# melhorar algoritmo guloso
