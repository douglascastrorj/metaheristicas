import random 
import copy

from utils import filterBy, _filter, ordenaCirurgias, getPenalizacao, mapToList

from fitness import viavel

# sobreposicao de horario cirurgiao
# maximo horario cirurgiao
# sobreposicao de horario cirurgia
# manter especialidade da sala (a menos q sala so tenha uma cirurgia)
# periodo de higienizacao

def primeiraMelhoria(funcaoBusca, params):
    pass


def trocaCirurgiasMesmoDia(params):
    solucaoAnterior = copy.deepcopy(params['solucao'])
    solucao = copy.deepcopy(params['solucao'])

    D = params['D']
    d = random.randint(0, D - 1)

    cirurgiasD = filterBy(solucaoAnterior, 'dia', d)
    # #print(list(cirurgiasD.keys()))
    if len(list(cirurgiasD.keys())) < 2:
        return solucaoAnterior
    
    c1 = random.choice(list(cirurgiasD.keys()))
    c2 = random.choice(list(cirurgiasD.keys()))

    solucao[c1]['horaInicio'] = solucaoAnterior[c2]['horaInicio']
    solucao[c1]['horaFim'] = solucaoAnterior[c2]['horaInicio'] + solucaoAnterior[c1]['duracao']
    solucao[c1]['sala'] = solucaoAnterior[c2]['sala']

    solucao[c2]['horaInicio'] = solucaoAnterior[c1]['horaInicio']
    solucao[c2]['horaFim'] = solucaoAnterior[c1]['horaInicio'] + solucaoAnterior[c2]['duracao']
    solucao[c2]['sala'] = solucaoAnterior[c1]['sala']

    return solucao

   

def trocaCirurgiasDiasDiferente(params):
    solucaoAnterior = copy.deepcopy(params['solucao'])
    solucao = copy.deepcopy(params['solucao'])

    D = params['D']

    cirurgiasD = {}
    for d in range(0, D):
        cd = filterBy(solucao, 'dia', d)
        if len(cd.keys()) > 0:
            cirurgiasD[d] = cd

    if len(cirurgiasD.keys()) < 2:
        # #print('nao existem cirurgias em dias diferentes')
        return solucao
    
    d1 = random.choice(list(cirurgiasD.keys()))
    d2 = random.choice( [d for d in list(cirurgiasD.keys()) if not d == d1] )


    c1 = random.choice(list(cirurgiasD[d1].keys()))
    c2 = random.choice(list(cirurgiasD[d2].keys()))

    solucao[c1]['horaInicio'] = solucaoAnterior[c2]['horaInicio']
    solucao[c1]['horaFim'] = solucaoAnterior[c2]['horaInicio'] + solucaoAnterior[c1]['duracao']
    solucao[c1]['dia'] = solucaoAnterior[c2]['dia']
    solucao[c1]['sala'] = solucaoAnterior[c2]['sala']

    solucao[c2]['horaInicio'] = solucaoAnterior[c1]['horaInicio']
    solucao[c2]['horaFim'] = solucaoAnterior[c1]['horaInicio'] + solucaoAnterior[c2]['duracao']
    solucao[c2]['dia'] = solucaoAnterior[c1]['dia']
    solucao[c2]['sala'] = solucaoAnterior[c1]['sala']

    # #print(f'\n\n c1 {c1} c2 {c2}\n\n')
    # #print(solucaoAnterior)
    # #print('\n- --------- -\n')
    # #print(solucao)

    return solucao

#inserindo apenas uma por enquanto
#sortear cirurgia a ser inserida de forma gulosa com base em um alpha (0 = totalmente aleatorio, 1 = totalmente guloso)
def insercaoDeUmaOuMaisCirurgiasDaListaEspera(params):
    solucao = copy.deepcopy(params['solucao'])

    idsCirurgiasNaoAlocadas = [c for c in solucao.keys() if solucao[c]['alocada'] == False]

    if len(idsCirurgiasNaoAlocadas) == 0:
        return solucao
    
    cirurgias_ = mapToList(params['solucao'])
    cirurgias_ = [ c for c in cirurgias_ if c['alocada'] == False ]

    #print(cirurgias_)
    
    compareF = lambda cirurgia : float(cirurgia['prioridade']) / (cirurgia['diasEspera'] * getPenalizacao(cirurgia['prioridade']))
    cirurgias_ = ordenaCirurgias(cirurgias_, compareF)

    # print(cirurgias_)
    # random.shuffle(cirurgias_)
    maxPos = max( int(len(cirurgias_) * (1 - params['alpha'])),  1)
    # #print(maxPos)
    cirurgias_ = cirurgias_[: maxPos]
    
    # #print(cirurgias_, idsCirurgiasNaoAlocadas)
  
    cirurgiaEscolhida = random.choice(cirurgias_)
    # print('cirurgiaEscolhida ', cirurgiaEscolhida)

    for d in range(0, params['D']):
        for s in range(0, params['S']):
            # print('d - s :', d , s)
            filterF = lambda cirurgia : cirurgia['dia'] == d and cirurgia['sala'] == s
            cirurgiasDiaSala = _filter(solucao, filterF)
            cirurgiasDiaSala = mapToList(cirurgiasDiaSala)
            getValor = lambda cirurgia : cirurgia['horaFim']
            cirurgiasDiaSala = ordenaCirurgias(cirurgiasDiaSala, getValor)
            
            inicio = 0
            fim =  cirurgiaEscolhida['duracao'] - 1
            if len(cirurgiasDiaSala) > 0:
                ultimaDoDiaSala = cirurgiasDiaSala[len(cirurgiasDiaSala) - 1]
                inicio = ultimaDoDiaSala['horaFim'] + 3
                fim = ultimaDoDiaSala['horaFim'] + 3 + cirurgiaEscolhida['duracao'] - 1

            cirurgia = {
                            "id": cirurgiaEscolhida['id'],
                            "sala": s,
                            "horaInicio": inicio,
                            "horaFim": fim,
                            "dia": d,
                            "duracao": cirurgiaEscolhida['duracao'],
                            "cirurgiao": cirurgiaEscolhida['cirurgiao'],
                            "diasEspera": cirurgiaEscolhida['diasEspera'],
                            "prioridade": cirurgiaEscolhida['prioridade'],
                            "especialidade": cirurgiaEscolhida['especialidade'],
                            "alocada": True
                        }
            
            solucao[cirurgia['id']] = cirurgia

            # print('inicio fim ', inicio, fim)
            if viavel(solucao, params['S'], 46, params['D']) == False:
                solucao = params['solucao']
                continue

            # #print('busca local ', cirurgia)
            return solucao
            #se puder adicionar cirurgia adiciona e retorna


    return params['solucao']


#sortear cirurgia a ser inserida de forma gulosa com base em um alpha (0 = totalmente aleatorio, 1 = totalmente guloso)
def removeCirurgias(params):
    solucao = copy.deepcopy(params['solucao'])

    alocadas = filterBy(solucao, 'alocada', True)

    if len(alocadas) == 0:
        return solucao

    cirurgias_ = mapToList(alocadas)
    compareF = lambda cirurgia : float(cirurgia['prioridade']) / (cirurgia['diasEspera'] * getPenalizacao(cirurgia['prioridade']))
    cirurgias_ = ordenaCirurgias(cirurgias_, compareF)
    cirurgias_.reverse()

    maxPos = max( int(len(cirurgias_) * (1 - params['alpha'])),  1)
    cirurgias_ = cirurgias_[: maxPos]
    
    # #print(cirurgias_, idsCirurgiasNaoAlocadas)
  
    cirurgiaEscolhida = random.choice(cirurgias_)
    cirurgiaAlocada = cirurgiaEscolhida['id']

    # print(f'cirurgia {cirurgiaAlocada} removida')

    solucao[cirurgiaAlocada]['dia'] = None
    solucao[cirurgiaAlocada]['sala'] = None
    solucao[cirurgiaAlocada]['horaInicio'] = None
    solucao[cirurgiaAlocada]['horaFim'] = None
    solucao[cirurgiaAlocada]['alocada'] = False

    return solucao 

def trocaCirurgiaMarcadaPorCirurgiaListaEspera(params):
    solucao = copy.deepcopy(params['solucao'])

    alocadas = filterBy(solucao, 'alocada', True)
    naoAlocadas = filterBy(solucao, 'alocada', False)

    if len(alocadas) == 0 or len(naoAlocadas) == 0:
        return solucao

    cirurgiaAlocada = random.choice(list(alocadas.keys()))
    cirurgiaNaoAlocada = random.choice(list(naoAlocadas.keys()))

    solucao[cirurgiaNaoAlocada]['dia'] = solucao[cirurgiaAlocada]['dia']
    solucao[cirurgiaNaoAlocada]['sala'] = solucao[cirurgiaAlocada]['sala']
    solucao[cirurgiaNaoAlocada]['horaInicio'] = solucao[cirurgiaAlocada]['horaInicio']
    solucao[cirurgiaNaoAlocada]['horaFim'] = solucao[cirurgiaAlocada]['horaInicio'] + solucao[cirurgiaNaoAlocada]['duracao'] - 1
    solucao[cirurgiaNaoAlocada]['alocada'] = True

    solucao[cirurgiaAlocada]['dia'] = None
    solucao[cirurgiaAlocada]['sala'] = None
    solucao[cirurgiaAlocada]['horaInicio'] = None
    solucao[cirurgiaAlocada]['horaFim'] = None
    solucao[cirurgiaAlocada]['alocada'] = False


    return solucao

def realocarHorario(params):
    solucao = copy.deepcopy(params['solucao'])

    alocadas = filterBy(solucao, 'alocada', True)
    cirurgiaEscolhida = random.choice(list(alocadas.keys()))
    deslocamento = random.randint(1, 10)
    direcao = random.choice([1, -1])

    solucao[cirurgiaEscolhida]['horaInicio'] += deslocamento * direcao
    solucao[cirurgiaEscolhida]['horaFim'] += deslocamento * direcao  

    return solucao

def trocaCirurgiaMarcadaPorDuasCirurgiasListaEspera(params):
    solucao = copy.deepcopy(params['solucao'])
    return solucao

def trocaDuasCirurgiasMarcadasPorUmaCirurgiaListaEspera(params):
    solucao = copy.deepcopy(params['solucao'])
    return solucao

def trocaDuasCirurgiasMarcadasPorDuasCirurgiasListaEspera(params):
    solucao = copy.deepcopy(params['solucao'])
    return solucao

def trocaDuasFimSemanaPorUmaInicioSemana(params):
    solucao = copy.deepcopy(params['solucao'])
    return solucao