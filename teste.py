from utils import readDataset, createMap, filterBy, getDistinctSpecialtyArr, xcstdToMap, desalocarCirurgia
from guloso2 import gerarSolucaoInicial
from fitness import fitnessFunction, FO1, viavel, FO2
from buscaLocal import trocaCirurgiasMesmoDia, trocaCirurgiasDiasDiferente, insercaoDeUmaOuMaisCirurgiasDaListaEspera, removeCirurgias
from metaheuristica import simulatedAnealing
from instancias import gerarInstancia

S = 3
T = 46
D = 5



dataset = readDataset('toy.txt')
cirurgias = createMap(dataset)


# cirurgias = gerarInstancia(N=50, H=20, E=4)
# cirurgias = gerarInstancia(N=20, H=5, E=4)

xcstd, yesd, z = gerarSolucaoInicial(cirurgias, S, D, verbose=True)

solucao = xcstdToMap(xcstd, cirurgias)
v = viavel(solucao, S, T, D)

# print(FO2(solucao))
# if v == False:
#     print(solucao)
#     print(f'\n\n(SOLUCAO INICIAL) FO = {FO1(solucao)}  - Viavel: {v} \n\n')
# print(solucao)

# desalocarCirurgia(solucao, 1)
# desalocarCirurgia(solucao, 5)
# desalocarCirurgia(solucao, 6)

# print(solucao)

# print(solucao)

# for i in range(0, 10):
#     s1 = trocaCirurgiasDiasDiferente({'solucao': solucao, 'D': D})
#     print('\n\n')
#     fo1 = FO1(s1, z)
#     print(f'FO = {fo1}  - Viavel: {viavel(s1, S, T, D)} \n\n')
#     print(s1)

# print(solucao)
# print('-------')
# print(removeCirurgias({'solucao': solucao, 'alpha': 1}))

# best = simulatedAnealing(solucao, FO1, SAmax=100, T0=300, alpha=0.65)
# print(best)
# print(f'\n\n(SOLUCAO INICIAL) FO = {FO1(solucao)}  - Viavel: {viavel(solucao, S, T, D)} \n\n')
# print(f'(MELHOR SOLUCAO) FO = {FO1(best)}  - Viavel: {viavel(best, S, T, D)} \n\n')
