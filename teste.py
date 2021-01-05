from utils import readDataset, createMap, filterBy, getDistinctSpecialtyArr, xcstdToMap, desalocarCirurgia
from guloso2 import gerarSolucaoInicial
from fitness import fitnessFunction, FO2, viavel
from buscaLocal import trocaCirurgiasMesmoDia, trocaCirurgiasDiasDiferente, insercaoDeUmaOuMaisCirurgiasDaListaEspera, removeCirurgias
from metaheuristica import simulatedAnealing
from instancias import gerarInstancia

S = 2
T = 46
D = 5

config = {
    'S': S,
    'T': T,
    'D': D
}


dataset = readDataset('toy2.txt')
cirurgias = createMap(dataset)


# cirurgias = gerarInstancia(N=50, H=10, E=4)
# cirurgias = gerarInstancia(N=20, H=5, E=4)

xcstd, yesd, z = gerarSolucaoInicial(cirurgias, S, D, verbose=True)

solucao = xcstdToMap(xcstd, cirurgias)
v = viavel(solucao, S, T, D, verbose=True)

print(FO2(solucao))
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

best = {
    1: {'id': 1, 'sala': 0, 'horaInicio': 0, 'horaFim': 4, 'dia': 0, 'duracao': 5, 'cirurgiao': 1, 'diasEspera': 1, 'prioridade': 1, 'especialidade': 1, 'alocada': True
    },
    3: {'id': 3, 'sala': 0, 'horaInicio': 7, 'horaFim': 14, 'dia': 0, 'duracao': 8, 'cirurgiao': 1, 'diasEspera': 1, 'prioridade': 1, 'especialidade': 1, 'alocada': True
    },
    4: {'id': 4, 'sala': 0, 'horaInicio': 17, 'horaFim': 27, 'dia': 0, 'duracao': 11, 'cirurgiao': 1, 'diasEspera': 1, 'prioridade': 1, 'especialidade': 1, 'alocada': True
    },
    6: {'id': 6, 'sala': 1, 'horaInicio': 43, 'horaFim': 57, 'dia': 0, 'duracao': 14, 'cirurgiao': 2, 'diasEspera': 9, 'prioridade': 3, 'especialidade': 2, 'alocada': True
    },
    8: {'id': 8, 'sala': 0, 'horaInicio': 0, 'horaFim': 3, 'dia': 1, 'duracao': 3, 'cirurgiao': 2, 'diasEspera': 5, 'prioridade': 3, 'especialidade': 2, 'alocada': True
    },
    2: {'id': 2, 'sala': 1, 'horaInicio': 28, 'horaFim': 40, 'dia': 0, 'duracao': 13, 'cirurgiao': 1, 'diasEspera': 1, 'prioridade': 1, 'especialidade': 2, 'alocada': True
    },
    5: {'id': 5, 'sala': 1, 'dia': 0, 'duracao': 10, 'cirurgiao': 2, 'diasEspera': 10, 'prioridade': 2, 'especialidade': 2, 'alocada': True, 'horaInicio': 16, 'horaFim': 25
    },
    7: {'id': 7, 'sala': 1, 'dia': 0, 'duracao': 11, 'cirurgiao': 2, 'diasEspera': 8, 'prioridade': 2, 'especialidade': 2, 'alocada': True, 'horaInicio': 0, 'horaFim': 10
    }
}


# s_ = insercaoDeUmaOuMaisCirurgiasDaListaEspera({'solucao': best, 'D': D, 'S': S, 'alpha': 0})
# print(f'FO (best) {FO2(best)} FO s_ {FO2(s_)}')
# print(viavel(best, S, T, D))

