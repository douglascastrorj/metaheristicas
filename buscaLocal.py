import random 
import copy

from utils import filterBy, _filter, ordenaCirurgias, getPenalizacao, mapToList

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
    print(list(cirurgiasD.keys()))
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
        print('nao existem cirurgias em dias diferentes')
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

    # print(f'\n\n c1 {c1} c2 {c2}\n\n')
    # print(solucaoAnterior)
    # print('\n- --------- -\n')
    # print(solucao)

    return solucao

#inserindo apenas uma por enquanto
def insercaoDeUmaOuMaisCirurgiasDaListaEspera(params):
    solucaoAnterior = copy.deepcopy(params['solucao'])
    solucao = copy.deepcopy(params['solucao'])

    idsCirurgiasNaoAlocadas = [c for c in params['cirurgias'].keys() if not c in solucao]

    if len(idsCirurgiasNaoAlocadas) == 0:
        return solucao
    
    #sortear cirurgia a ser inserida de forma gulosa com base em um alpha (0 = totalmente aleatorio, 1 = totalmente guloso)
    cirurgias_ = mapToList(params['cirurgias'])
    compareF = lambda cirurgia : float(getPenalizacao(cirurgia['p'])) /  cirurgia['w']
    cirurgias_ = ordenaCirurgias(cirurgias_, compareF)
    random.shuffle(cirurgias_)
    cirurgias_ = cirurgias_[: int(len(cirurgias_) * params['alpha'])]

    cirurgiaEscolhida = random.choice(cirurgias_)

    for d in range(0, params['D']):
        for s in range(0, params['S']):
            filterF = lambda cirurgia : cirurgia['dia'] == d & cirurgia['sala'] == s
            cirurgiasDiaSala = _filter(solucao, filterF)
            mapToList(cirurgiasDiaSala)
            getValor = lambda cirurgia : cirurgia['horarioFim']
            cirurgiasDiaSala = ordenaCirurgias(cirurgiasDiaSala, getValor)

            #se puder adicionar cirurgia adiciona e retorna


    return solucao


def trocaCirurgiaMarcadaPorCirurgiaListaEspera(Xcstd, cirurgias):

    return Xcstd

def trocaCirurgiaMarcadaPorDuasCirurgiasListaEspera(Xcstd, cirurgias):

    return Xcstd

def trocaDuasCirurgiasMarcadasPorUmaCirurgiaListaEspera(Xcstd, cirurgias):

    return Xcstd

def trocaDuasCirurgiasMarcadasPorDuasCirurgiasListaEspera(Xcstd, cirurgias):

    return Xcstd

def trocaDuasFimSemanaPorUmaInicioSemana(Xcstd, cirurgias):

    return Xcstd