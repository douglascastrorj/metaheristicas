from utils import filterBy, filterNotBy, getPenalizacao, _filter, overlap

MAX_SLOTS_MEDICO_DIA = 24
MAX_SLOTS_MEDICO_SEMANA = 100

def viavel(solucao, S, T, D):
    cirurgioes = []
    especialidades = []
    for c in solucao:
        cirurgioes.append(solucao[c]['cirurgiao'])
        especialidades.append(solucao[c]['especialidade'])
    
    cirurgioes = set(cirurgioes)
    especialidades = set(especialidades)

    # Check if some room has more than one specialty in the same day
    for d in range(0, D):
        for s in range(0, S):
            filterF = lambda cirurgia : cirurgia['sala'] == s and cirurgia['dia'] == d
            surgeries =  _filter(solucao, filterF)
            specialties = []
            for c in surgeries:
                specialties.append(surgeries[c]['especialidade'])

            if len(set(specialties)) > 1:
                # print(f"Room {s} has more than one specialty at day {d}. Check surgeries: {surgeries}.")
                return False

    # Check if some surgeon exceeds limit of 24/100 timesteps
    for day in range(1, D):
        for cirurgiao in cirurgioes:
            cirurgiasSemana = filterBy(solucao, 'cirurgiao', cirurgiao)
            tempoSemana = 0
            for c in cirurgiasSemana:
                tempoSemana += cirurgiasSemana[c]['duracao']

            cirurgiasDia = filterBy(cirurgiasSemana, 'dia', day)
            tempoDia = 0
            for c in cirurgiasDia:
                tempoDia += cirurgiasDia[c]['duracao']
            
            if(tempoDia > MAX_SLOTS_MEDICO_DIA):
                # print(f'Cirurgiao {cirurgiao} possui mais que {MAX_SLOTS_MEDICO_DIA} no dia {day}.')
                return False
            
            if(tempoSemana > MAX_SLOTS_MEDICO_SEMANA):
                # print(f'Cirurgiao {cirurgiao} possui mais que {MAX_SLOTS_MEDICO_SEMANA}.')
                return False

    # Check if some surgeon has overlapping surgeries
    for day in range(0, D):
        for cirurgiao in cirurgioes:
            cirurgiasSemana = filterBy(solucao, 'cirurgiao', cirurgiao)
            cirurgiasDia = filterBy(cirurgiasSemana, 'dia', day)
            for c1 in cirurgiasDia:
                for c2 in cirurgiasDia:
                    if c1 == c2:
                        continue

                    cirurgia1 = cirurgiasDia[c1]
                    cirurgia2 = cirurgiasDia[c2]
                    if overlap(cirurgia1, cirurgia2):
                        # print(f'cirurgias {c1} - {c2} do cirurgiao {cirurgiao} colidem')
                        return False
                    


    # Check if surgeries overlap
    for day in range(1, D):
        for s in range(0, S):
            filterDiaSala = lambda cirurgia : cirurgia['dia'] == d and cirurgia['sala'] == s
            cirurgiasDiaSala = _filter(solucao, filterDiaSala)
            for c1 in cirurgiasDiaSala:
                for c2 in cirurgiasDiaSala:
                    cirurgia1 = cirurgiasDiaSala[c1]
                    cirurgia2 = cirurgiasDiaSala[c2]
                    if overlap(cirurgia1, cirurgia2):
                        # print(f'cirurgias {c1} - {c2} colidem')
                        return False

    return True



def FO1(solucao, z):
    fo = 0

    cirurgiasD0 = filterBy(solucao, 'dia', 0)
    for c in cirurgiasD0:
        cirurgia = cirurgiasD0[c]
        # print (cirurgia)
        wc = cirurgia['diasEspera']
        fo += (wc + 3) * cirurgia['duracao']

    cirurgiasNaoP1 = filterNotBy(solucao, 'prioridade', 1)
    for c in cirurgiasNaoP1:
        cirurgia = cirurgiasNaoP1[c]
        wc = cirurgia['diasEspera'] 
        d = cirurgia['dia']
        fo += (wc + 2 + (d + 1)) * cirurgia['duracao'] # nosso d vai de 0 a 4

        pc = cirurgia['prioridade']
        Epc = getPenalizacao(pc)
        fo += pc * Epc * z[c]

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
