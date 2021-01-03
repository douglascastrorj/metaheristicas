from utils import filterBy, filterNotBy, getPenalizacao, _filter, overlap, mapToList, ordenaCirurgias

MAX_SLOTS_MEDICO_DIA = 24
MAX_SLOTS_MEDICO_SEMANA = 100

def viavel(solucao, S, T, D, verbose=False):
    cirurgioes = []
    especialidades = []
    for c in solucao:
        cirurgioes.append(solucao[c]['cirurgiao'])
        especialidades.append(solucao[c]['especialidade'])
    
    cirurgioes = set(cirurgioes)
    especialidades = set(especialidades)

    for c in solucao:
        cirurgia = solucao[c]

        if cirurgia['alocada'] == True  and cirurgia['horaFim'] > T:
            if verbose:
                print('cirurgia com T > 45', cirurgia)
            return False

        if cirurgia['prioridade'] == 1:
            if  cirurgia['alocada'] == True and cirurgia['dia'] > 0:
                if verbose:
                    print('cirurgia p1 alocada em outro dia', cirurgia)
                return False

    #verifica perdiodo de higienizacao entre cirurgias
    for d in range(0, D):
        for s in range(0, S):
            filterF = lambda cirurgia : cirurgia['dia'] == d and cirurgia['sala'] == s
            cirurgiasDiaSala = _filter(solucao, filterF)
            cirurgiasDiaSala = mapToList(cirurgiasDiaSala)
            getValor = lambda cirurgia : cirurgia['horaFim']
            cirurgiasDiaSala = ordenaCirurgias(cirurgiasDiaSala, getValor)
            for cirurgiaAnterior, cirurgiaCorrente in zip(cirurgiasDiaSala, cirurgiasDiaSala[1:]):
                if cirurgiaCorrente['horaInicio'] - cirurgiaAnterior['horaFim'] < 3:
                    if verbose:
                        print(f'Solucao nao respeita criterio de higienizacao {cirurgiaCorrente["horaInicio"]} - { cirurgiaAnterior["horaFim"]}')
                    return False

    # Check if some room has more than one specialty in the same day
    for d in range(0, D):
        for s in range(0, S):
            filterF = lambda cirurgia : cirurgia['sala'] == s and cirurgia['dia'] == d
            surgeries =  _filter(solucao, filterF)
            specialties = []
            for c in surgeries:
                specialties.append(surgeries[c]['especialidade'])

            if len(set(specialties)) > 1:
                if verbose:
                    print(f"Room {s} has more than one specialty at day {d}. Check surgeries: {surgeries}.")
                return False

    # Check if some surgeon exceeds limit of 24/100 timesteps
    for day in range(1, D):
        for cirurgiao in cirurgioes:
            filterF = lambda cirurgia : cirurgia['alocada'] == True and cirurgia['cirurgiao'] == cirurgiao
            cirurgiasSemana = _filter(solucao, filterF)
            tempoSemana = 0
            for c in cirurgiasSemana:
                tempoSemana += cirurgiasSemana[c]['duracao']

            cirurgiasDia = filterBy(cirurgiasSemana, 'dia', day)
            tempoDia = 0
            for c in cirurgiasDia:
                tempoDia += cirurgiasDia[c]['duracao']
            
            if(tempoDia > MAX_SLOTS_MEDICO_DIA):
                if verbose:
                    print(f'Cirurgiao {cirurgiao} possui mais que {MAX_SLOTS_MEDICO_DIA} no dia {day}.')
                return False
            
            if(tempoSemana > MAX_SLOTS_MEDICO_SEMANA):
                if verbose:
                    print(f'Cirurgiao {cirurgiao} possui mais que {MAX_SLOTS_MEDICO_SEMANA}.')
                return False

    # Check if some surgeon has overlapping surgeries
    for day in range(0, D):
        for cirurgiao in cirurgioes:
            filterF = lambda cirurgia : cirurgia['alocada'] == True and cirurgia['cirurgiao'] == cirurgiao and cirurgia['dia'] == day
            cirurgiasDia = _filter(solucao, filterF)
            for c1 in cirurgiasDia:
                for c2 in cirurgiasDia:
                    if c1 == c2:
                        continue

                    cirurgia1 = cirurgiasDia[c1]
                    cirurgia2 = cirurgiasDia[c2]
                    if overlap(cirurgia1, cirurgia2):
                        if verbose:
                            print(f'cirurgias {c1} - {c2} do cirurgiao {cirurgiao} colidem')
                        return False
                    


    # Check if surgeries overlap
    for day in range(1, D):
        for s in range(0, S):
            filterDiaSala = lambda cirurgia : cirurgia['dia'] == d and cirurgia['sala'] == s and cirurgia['alocada'] == True
            cirurgiasDiaSala = _filter(solucao, filterDiaSala)
            for c1 in cirurgiasDiaSala:
                for c2 in cirurgiasDiaSala:
                    cirurgia1 = cirurgiasDiaSala[c1]
                    cirurgia2 = cirurgiasDiaSala[c2]
                    if overlap(cirurgia1, cirurgia2):
                        if verbose:
                            print(f'cirurgias {c1} - {c2} colidem')
                        return False

    return True



def FO1(solucao):
    fo = 0

    cirurgiasD0 = filterBy(solucao, 'dia', 0)
    for c in cirurgiasD0:
        cirurgia = cirurgiasD0[c]
        if cirurgia['alocada'] == False:
            continue
        # #print (cirurgia)
        wc = cirurgia['diasEspera']
        fo += (wc + 3) * cirurgia['duracao']

    cirurgiasNaoP1 = filterNotBy(solucao, 'prioridade', 1)
    for c in cirurgiasNaoP1:
        cirurgia = cirurgiasNaoP1[c]
        if cirurgia['alocada'] == False:
            continue

        wc = cirurgia['diasEspera'] 
        d = cirurgia['dia']
        fo += (wc + 2 + (d + 1)) * cirurgia['duracao'] # nosso d vai de 0 a 4

    for c in cirurgiasNaoP1:
        cirurgia = cirurgiasNaoP1[c]
        if cirurgia['alocada'] == False:
            pc = cirurgia['prioridade']
            Epc = getPenalizacao(pc)
            fo += pc * Epc

    return fo

def fitnessFunction( cirurgias, S, T, D, Xcstd, z):

    cirurgiasNaoP1 = filterNotBy(cirurgias, 'p', 1)

    fo = 0

    for c in cirurgias:
        cirurgia = cirurgias[c]
        wc = cirurgia['w']
        for s in range(0, S):
            for t in range(0,T):
                xcst1 = Xcstd[c][s][t][0]
                fo += (wc + 3)*xcst1 * cirurgia['tc']

    for c in cirurgiasNaoP1:
        cirurgia = cirurgiasNaoP1[c]
        wc = cirurgia['w']
        for s in range(0, S):
            for t in range(0, T):
                for d in range(0, D):
                    xcstd = Xcstd[c][s][t][d]
                    fo += (wc + 2 + (d + 1))*xcstd * cirurgia['tc'] # nosso d vai de 0 a 4
        pc = cirurgia['p']
        Epc = getPenalizacao(pc)
        fo += pc * Epc * z[c]

    return fo



def FO2(solucao):
    lp = { 1: 3, 2: 15, 3: 60, 4: 365 }

    fo = 0
    
    filterFunc = lambda cirurgia : cirurgia['prioridade'] == 1 and cirurgia['alocada'] == True and cirurgia['dia'] != 0
    cirurgiasP1 = _filter(solucao, filterFunc)
    for c in cirurgiasP1:
        cirurgia = cirurgiasP1[c]
        wc = cirurgia['diasEspera']
        d = cirurgia['dia'] + 1
        fo += 10*(wc + 2)**d
    
    cirurgiasAlocadas = filterBy(solucao, 'alocada', True)
    for c in cirurgiasAlocadas:
        cirurgia = cirurgiasAlocadas[c]
        wc = cirurgia['diasEspera']
        d = cirurgia['dia'] + 1
        lpc = lp[cirurgia['prioridade']]
        vc = int(wc > lpc)

        fo += ( (wc + 2 + d)**2 ) + ((wc + 2 + d - lpc)**2) * vc
    

    cirurgiasNaoAlocadas = filterBy(solucao, 'alocada', False)
    for c in cirurgiasNaoAlocadas:
        cirurgia = cirurgiasNaoAlocadas[c]
        wc = cirurgia['diasEspera']
        lpc = lp[cirurgia['prioridade']]
        epsilon = getPenalizacao(cirurgia['prioridade'])
        vc = int(wc > lpc)

        fo += ((wc + 7)**2)*epsilon + (epsilon*(wc + 9 -lpc)**2)*vc
 
    return fo