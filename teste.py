from utils import readDataset, createMap, filterBy, getDistinctSpecialtyArr, xcstdToMap
from guloso2 import gerarSolucaoInicial
from fitness import fitnessFunction, FO1, viavel
from buscaLocal import trocaCirurgiasMesmoDia, trocaCirurgiasDiasDiferente, insercaoDeUmaOuMaisCirurgiasDaListaEspera

S = 2
T = 46
D = 5

dataset = readDataset('toy.txt')
cirurgias = createMap(dataset)

xcstd, yesd, z = gerarSolucaoInicial(cirurgias, S, D, verbose=True)

solucao = xcstdToMap(xcstd, cirurgias)
print(solucao)
del solucao[1]
del solucao[5]
del solucao[6]
print(solucao)

fo1 = FO1(solucao, z)
print(f'FO = {fo1}')

print(f'Solucao Viavel: {viavel(solucao, S, T, D)}')

s1 = insercaoDeUmaOuMaisCirurgiasDaListaEspera({'alpha': 0, 'cirurgias': cirurgias, 'solucao': solucao, 'D': D, 'S': S})
print(s1)
# for i in range(0, 10):
#     s1 = trocaCirurgiasDiasDiferente({'solucao': solucao, 'D': D})
#     print('\n\n')
#     fo1 = FO1(s1, z)
#     print(f'FO = {fo1}  - Viavel: {viavel(s1, S, T, D)} \n\n')
#     print(s1)

