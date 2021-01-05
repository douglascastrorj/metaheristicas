from utils import readDataset, createMap, filterBy, getDistinctSpecialtyArr, xcstdToMap, desalocarCirurgia
from guloso2 import gerarSolucaoInicial
from fitness import fitnessFunction, FO2, viavel
from buscaLocal import trocaCirurgiasMesmoDia, trocaCirurgiasDiasDiferente, insercaoDeUmaOuMaisCirurgiasDaListaEspera, removeCirurgias
from metaheuristica import simulatedAnealing
from instancias import gerarInstancia

S = 4
T = 46
D = 5

config = {
    'S': S,
    'T': T,
    'D': D
}


dataset = readDataset('dataset/i001.csv')
cirurgias = createMap(dataset)


# cirurgias = gerarInstancia(N=50, H=10, E=4)
# cirurgias = gerarInstancia(N=20, H=5, E=4)

xcstd, yesd, z = gerarSolucaoInicial(cirurgias, S, D, verbose=False)

solucao = xcstdToMap(xcstd, cirurgias)
v = viavel(solucao, S, T, D, verbose=True)

print(f'FO Inicial: {FO2(solucao)}')
# if v == False:
#     print(solucao)
#     print(f'\n\n(SOLUCAO INICIAL) FO = {FO2(solucao)}  - Viavel: {v} \n\n')
# print(solucao)

# desalocarCirurgia(solucao, 1)
# desalocarCirurgia(solucao, 5)
# desalocarCirurgia(solucao, 6)

# print(solucao)

# print(solucao)

# for i in range(0, 10):
#     s1 = trocaCirurgiasDiasDiferente({'solucao': solucao, 'D': D})
#     print('\n\n')
#     FO2 = FO2(s1, z)
#     print(f'FO = {FO2}  - Viavel: {viavel(s1, S, T, D)} \n\n')
#     print(s1)

# print(solucao)
# print('-------')
# print(removeCirurgias({'solucao': solucao, 'alpha': 1}))

best = simulatedAnealing(solucao, config, FO2, SAmax=500, T0=300, alpha=0.6, verbose=True)
print(best)
print(f'\n\n(SOLUCAO INICIAL) FO = {FO2(solucao)}  - Viavel: {viavel(solucao, S, T, D)} \n\n')
print(f'(MELHOR SOLUCAO) FO = {FO2(best)}  - Viavel: {viavel(best, S, T, D)} \n\n')

# s_ = insercaoDeUmaOuMaisCirurgiasDaListaEspera({'solucao': best, 'D': D, 'S': S, 'alpha': 0})
# print(f'FO (best) {FO2(best)} FO s_ {FO2(s_)}')
# print(viavel(best, S, T, D))

