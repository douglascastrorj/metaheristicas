from utils import readDataset, createMap, filterBy, getDistinctSpecialtyArr, xcstdToMap
from guloso2 import gerarSolucaoInicial
from fitness import fitnessFunction, fitnessFunction2, FO1
from buscaLocal import trocaCirurgiasMesmoDia

S = 2
T = 46
D = 5

dataset = readDataset('toy.txt')
cirurgias = createMap(dataset)

xcstd, yesd, z = gerarSolucaoInicial(cirurgias, S, D, verbose=True)


fo = fitnessFunction(cirurgias, S, T, D, xcstd, z)
fo2 = fitnessFunction2(cirurgias, S, T, D, xcstd, z)

print(f'FO = {fo}')
print(f'FO2 = {fo2}')

# trocaCirurgiasMesmoDia(xcstd, cirurgias, 0)


solucao = xcstdToMap(xcstd, cirurgias)
# print(solucao)

fo1 = FO1(solucao, z)
print(f'FO = {fo1}')

# implementar metodo de busca local
#   - verificar se solucao é viavel
# melhorar algoritmo guloso
