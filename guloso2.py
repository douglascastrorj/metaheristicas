from utils import filterBy, createDecisionDict, getDistinctSpecialtyArr2, createMedicSlotMap, createEspecialidadesSalaDia
import numpy as np

MAX_SLOTS_MEDICO_DIA = 24
MAX_SLOTS_MEDICO_SEMANA = 100

def gerarSolucaoInicial(cirurgias, S, T, D):
    
    # contar slots usados pelos medicos
    medicSlotMap = createMedicSlotMap(cirurgias)

    # preencher d1 de todas as salas com cirurgias prioridade 1
    cirurgiasP1 = filterBy(cirurgias, 'p', 1)

    E = getDistinctSpecialtyArr2(cirurgias)
    Xcstd, yesd, z = createDecisionDict(cirurgias, S, T, D, E)

    cirurgiasAtendidas = []
    tempoSalas = np.zeros(S)

    especialidadesDaSalaNoDia = createEspecialidadesSalaDia(S, D)

    for s in range(0, S):
        # TODO: verificar qual Especialidade das cirurgias de P1 seria melhor
        for c in cirurgiasP1:
            cirurgia = cirurgiasP1[c]

            # verifica se cirurgia foi atendida
            if c in cirurgiasAtendidas:
                print(f'cirurgia {c} ja foi atendida')
                continue

            # verifica se cirurgia cabe na sala
            if(tempoSalas[s] + cirurgia['tc'] + 2 > T):
                if not (tempoSalas[s] == 0 and cirurgia['tc'] == T):
                    print(f'cirurgia {c} nao cabe na sala {s} no dia 0')
                    continue
            
            # verifica se medico pode atender cirurgia
            if medicSlotMap[cirurgia['h']]['slotsDia']  + cirurgia['tc'] > MAX_SLOTS_MEDICO_DIA:
                print(f'medico {cirurgia["h"]} nao possui slots para realizar cirurgia {c} no dia')
                continue
            if medicSlotMap[cirurgia['h']]['slotsSemana']  + cirurgia['tc'] > MAX_SLOTS_MEDICO_SEMANA:
                print(f'medico {cirurgia["h"]} nao possui slots para realizar cirurgia {c} na semana')
                continue
            
            # verifica se adicionar cirurgia matem bloco fechado
            if especialidadesDaSalaNoDia[s][0] != 0 and especialidadesDaSalaNoDia[s][0] != cirurgia['e']:
                print(f'cirurgia de especialidade {cirurgia["e"]} nao pode ser atendida na sala {s} dia 0')
                continue

            print(f'adicionando cirurgia {c} na sala {s} d 0')
            print( 'cirurgia: ', cirurgia )
            Xcstd[cirurgia['c']][s][tempoSalas[s]][0] = 1

            # atualizar variaveis de controle
            cirurgiasAtendidas.append(c)
            if tempoSalas[s] >= 0: 
                tempoSalas[s] += 3
            tempoSalas[s] += cirurgia['tc']

            medicSlotMap[cirurgia['h']]['slotsDia'] += cirurgia['tc']
            medicSlotMap[cirurgia['h']]['slotsSemana'] += cirurgia['tc']

            especialidadesDaSalaNoDia[s][0] = cirurgia['e']


    return Xcstd