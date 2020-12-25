from utils import readDataset, createMap, filterBy, getDistinctSpecialtyArr, xcstdToMap
from guloso2 import gerarSolucaoInicial
from fitness import fitnessFunction, fitnessFunction2, FO1, viavel
from buscaLocal import trocaCirurgiasMesmoDia, trocaCirurgiasDiasDiferente

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

print(f'Solucao Viavel: {viavel(solucao, S, T, D)}')

# for i in range(0, 10):
#     s1 = trocaCirurgiasDiasDiferente({'solucao': solucao, 'D': D})
#     print('\n\n')
#     fo1 = FO1(s1, z)
#     print(f'FO = {fo1}  - Viavel: {viavel(s1, S, T, D)} \n\n')
#     print(s1)

for i in range(0, 10):
    s1 = trocaCirurgiasMesmoDia({'solucao': solucao, 'D': D})
    print('\n\n')
    fo1 = FO1(s1, z)
    print(f'FO = {fo1}  - Viavel: {viavel(s1, S, T, D)} \n\n')
    print(s1)

# implementar metodo de busca local
#   - verificar se solucao é viavel
# melhorar algoritmo guloso
