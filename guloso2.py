from utils import filterBy, createDecisionDict, getDistinctSpecialtyArr2, createMedicSlotMap, createEspecialidadesSalaDia
import numpy as np

MAX_SLOTS_MEDICO_DIA = 24
MAX_SLOTS_MEDICO_SEMANA = 100
T = 46


def gerarSolucaoInicial(cirurgias, S, D, verbose = False):
    
    # contar slots usados pelos medicos
    medicSlotMap = createMedicSlotMap(cirurgias)

    # preencher d1 de todas as salas com cirurgias prioridade 1
    cirurgiasP1 = filterBy(cirurgias, 'p', 1)

    E = getDistinctSpecialtyArr2(cirurgias)
    Xcstd, yesd, z = createDecisionDict(cirurgias, S, T, D, E)

    cirurgiasAtendidas = []
    tempoSalas = np.zeros((S, D))

    especialidadesDaSalaNoDia = createEspecialidadesSalaDia(S, D)

    for s in range(0, S):
        # TODO: verificar qual Especialidade das cirurgias de P1 seria melhor
        keys = [*cirurgiasP1]
        for c in keys:
            cirurgia = cirurgiasP1[c]

            podeAdicionar = verificaSePodeAdicionar(cirurgia, cirurgiasAtendidas, tempoSalas[s][0], especialidadesDaSalaNoDia[s][0], medicSlotMap, verbose)
            if podeAdicionar == False:
                continue
            
            #verificar se cirurgiao esta ocupado
            ocupadoNoPeriodo = cirurgiaoOcupadoNoPeriodo(cirurgias, cirurgia, Xcstd, tempoSalas[s][0], 0)
            if ocupadoNoPeriodo['ocupado']:
                if verbose:
                    print(f'cirurgiao {cirurgia["h"]} esta ocupado no periodo {ocupadoNoPeriodo["inicio"]} <-> {ocupadoNoPeriodo["fim"]}')
                continue

            if verbose:
                print(f'adicionando cirurgia {c} na sala {s} d 0')
                print( 'cirurgia: ', cirurgia )

            Xcstd[cirurgia['c']][s][tempoSalas[s][0]][0] = 1
            yesd[cirurgia['e']][s][0] = 1

            # atualizar variaveis de controle
            cirurgiasAtendidas.append(c)
            if tempoSalas[s][0] >= 0: 
                tempoSalas[s][0] += 2
            tempoSalas[s][0] += cirurgia['tc']

            medicSlotMap[cirurgia['h']]['slotsDia'] += cirurgia['tc']
            medicSlotMap[cirurgia['h']]['slotsSemana'] += cirurgia['tc']

            especialidadesDaSalaNoDia[s][0] = cirurgia['e']

    for s in range(0, S):
        keys = [*cirurgias]
        for c in cirurgias:
            #
            if c in cirurgiasP1:
                continue

            for d in range(0, D):
                cirurgia = cirurgias[c] 

                podeAdicionar = verificaSePodeAdicionar(cirurgia, cirurgiasAtendidas, tempoSalas[s][d], especialidadesDaSalaNoDia[s][d], medicSlotMap, verbose)
                if podeAdicionar == False:
                    continue

                ocupadoNoPeriodo = cirurgiaoOcupadoNoPeriodo(cirurgias, cirurgia, Xcstd, tempoSalas[s][0], d)
                if ocupadoNoPeriodo['ocupado']:
                    if verbose:
                        print(f'cirurgiao {cirurgia["h"]} esta ocupado no periodo {ocupadoNoPeriodo["inicio"]} <-> {ocupadoNoPeriodo["fim"]}')
                    continue

                if verbose:
                    print(f'adicionando cirurgia {c} na sala {s} d 0')
                    print( 'cirurgia: ', cirurgia )

                Xcstd[cirurgia['c']][s][tempoSalas[s][d]][d] = 1
                yesd[cirurgia['e']][s][d] = 1

                # atualizar variaveis de controle
                cirurgiasAtendidas.append(c)
                if tempoSalas[s][d] >= 0: 
                    tempoSalas[s][d] += 3
                tempoSalas[s][d] += cirurgia['tc']

                medicSlotMap[cirurgia['h']]['slotsDia'] += cirurgia['tc']
                medicSlotMap[cirurgia['h']]['slotsSemana'] += cirurgia['tc']

                especialidadesDaSalaNoDia[s][d] = cirurgia['e']

    #preencher z
    for c in cirurgias:
        if c not in cirurgiasAtendidas:
            z[c] = 1

    return Xcstd, yesd, z


def verificaSePodeAdicionar(cirurgia, cirurgiasAtendidas, tempoSalaS, especialidadesDaSalaNoDia, medicSlotMap, verbose):
    # verifica se cirurgia foi atendida
    c = cirurgia['c']
    if c in cirurgiasAtendidas:
        if verbose:
            print(f'cirurgia {c} ja foi atendida')
        return False

    # verifica se cirurgia cabe na sala
    if(tempoSalaS + cirurgia['tc'] + 2 > T):
        if not (tempoSalaS == 0 and cirurgia['tc'] == T):
            if verbose:
                print(f'cirurgia {c} nao cabe na sala no dia 0')
            return False
    
    # verifica se medico pode atender cirurgia
    if medicSlotMap[cirurgia['h']]['slotsDia']  + cirurgia['tc'] > MAX_SLOTS_MEDICO_DIA:
        if verbose:
            print(f'medico {cirurgia["h"]} nao possui slots para realizar cirurgia {c} no dia')
        return False
    if medicSlotMap[cirurgia['h']]['slotsSemana']  + cirurgia['tc'] > MAX_SLOTS_MEDICO_SEMANA:
        if verbose:
            print(f'medico {cirurgia["h"]} nao possui slots para realizar cirurgia {c} na semana')
        return False
    
    # verifica se adicionar cirurgia matem bloco fechado
    if especialidadesDaSalaNoDia != 0 and especialidadesDaSalaNoDia != cirurgia['e']:
        if verbose:
            print(f'cirurgia de especialidade {cirurgia["e"]} nao pode ser atendida na sala dia 0')
        return False
    
    return True

def cirurgiaoOcupadoNoPeriodo(cirurgias, cirurgia, Xcstd, t, d):
    cirurgiao = cirurgia['h']

    inicioCirurgia = t
    fimCirurgia = t + cirurgia['tc'] -1
    
    ocupado = {
        "ocupado": False
    }
    
    for c in Xcstd:
        cirurgiaCorrente = cirurgias[c]
        if cirurgiaCorrente['h'] != cirurgiao:
            continue
        
        for s in Xcstd[c]:
            for t_ in Xcstd[c][s]:
                if Xcstd[c][s][t_][d] == 1:
                    inicioCirurgiaCorrente = t_
                    fimCirurgiaCorrente = t_ + cirurgiaCorrente['tc'] -1

                    if cirurgia['c'] == 4:
                        print('\n\n INICIO E FIM CIRURGIA')
                        print(f' {inicioCirurgia} - {fimCirurgia}')
                        print(f' {inicioCirurgiaCorrente} - {fimCirurgiaCorrente}')

                    if inicioCirurgia <= inicioCirurgiaCorrente and fimCirurgia >= inicioCirurgiaCorrente:
                        ocupado['inicio'] = inicioCirurgiaCorrente
                        ocupado['fim'] = fimCirurgiaCorrente
                        ocupado['ocupado'] = True
                    if inicioCirurgiaCorrente <= inicioCirurgia and fimCirurgiaCorrente >= inicioCirurgia:
                        ocupado['inicio'] = inicioCirurgiaCorrente
                        ocupado['fim'] = fimCirurgiaCorrente
                        ocupado['ocupado'] = True

    print('\n\n')
    return ocupado                   