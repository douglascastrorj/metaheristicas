from utils import readDataset, createMap, filterBy, getDistinctSpecialtyArr
from guloso2 import gerarSolucaoInicial
from fitness import fitnessFunction, fitnessFunction2

S = 2
T = 46
D = 5

dataset = readDataset('toy.txt')
cirurgias = createMap(dataset)

solucaoInicial, yesd, z = gerarSolucaoInicial(cirurgias, S, D, verbose=True)

print(solucaoInicial)

fo = fitnessFunction(cirurgias, S, T, D, solucaoInicial, z)
fo2 = fitnessFunction2(cirurgias, S, T, D, solucaoInicial, z)
print(f'FO = {fo}')
print(f'FO2 = {fo2}')


# implementar metodo de busca local
#   - verificar se solucao é viavel
# melhorar algoritmo guloso
