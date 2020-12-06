from utils import filterBy, filterNotBy, createDecisionDict, getDistinctSpecialtyArr2, createMedicSlotMap, createEspecialidadesSalaDia
import numpy as np

MAX_SLOTS_MEDICO_DIA = 24
MAX_SLOTS_MEDICO_SEMANA = 100
T = 46


def gerarSolucaoInicial(cirurgias, S, D, verbose = False):
    
    # contar slots usados pelos medicos
    medicSlotMap = createMedicSlotMap(cirurgias)

    # preencher d1 de todas as salas com cirurgias prioridade 1
    cirurgiasP1 = filterBy(cirurgias, 'p', 1)
    demaisCirurgias = filterNotBy(cirurgias, 'p', 1)

    E = getDistinctSpecialtyArr2(cirurgias)
    Xcstd, yesd, z = createDecisionDict(cirurgias, S, T, D, E)

    cirurgiasAtendidas = []
    tempoSalas = np.zeros((S, D))

    especialidadesDaSalaNoDia = createEspecialidadesSalaDia(S, D)

    popularVariaveis(S, cirurgiasP1, cirurgiasAtendidas, tempoSalas, especialidadesDaSalaNoDia, medicSlotMap, Xcstd, yesd, 0)
    for d in range(0, D):
        popularVariaveis(S, demaisCirurgias, cirurgiasAtendidas, tempoSalas, especialidadesDaSalaNoDia, medicSlotMap, Xcstd, yesd, d)

    
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
                        # print('\n\n INICIO E FIM CIRURGIA')
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

    return ocupado

def popularVariaveis(S, cirurgias, cirurgiasAtendidas, tempoSalas, especialidadesDaSalaNoDia, medicSlotMap, Xcstd, yesd, d):
    for s in range(0, S):
        # TODO: verificar qual Especialidade das cirurgias de P1 seria melhor
        keys = [*cirurgias]
        for c in keys:
            cirurgia = cirurgias[c]

            podeAdicionar = verificaSePodeAdicionar(cirurgia, cirurgiasAtendidas, tempoSalas[s][d], especialidadesDaSalaNoDia[s][d], medicSlotMap, False)
            if podeAdicionar == False:
                continue
            
            #verificar se cirurgiao esta ocupado
            ocupadoNoPeriodo = cirurgiaoOcupadoNoPeriodo(cirurgias, cirurgia, Xcstd, tempoSalas[s][d], d)
            if ocupadoNoPeriodo['ocupado']:
                continue


            Xcstd[cirurgia['c']][s][tempoSalas[s][d]][d] = 1
            yesd[cirurgia['e']][s][d] = 1

            # atualizar variaveis de controle
            cirurgiasAtendidas.append(c)
            if tempoSalas[s][d] >= 0: 
                tempoSalas[s][d] += 2
            tempoSalas[s][d] += cirurgia['tc']

            medicSlotMap[cirurgia['h']]['slotsDia'] += cirurgia['tc']
            medicSlotMap[cirurgia['h']]['slotsSemana'] += cirurgia['tc']

            especialidadesDaSalaNoDia[s][d] = cirurgia['e']