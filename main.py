from utils import readDataset, getSurgeryByPriority
import guloso


#criar variaveis de decisao
# Xcstd, yesd, z = utils.createDecisionVar(C, S, T, D, E)


S = 1
#ler dataset
dataset = readDataset('toy2.txt')

solucao = guloso.gerarSolucaoInicial(dataset, S)


priority1 = getSurgeryByPriority(dataset, 1)

# print(solucao)

for c in priority1:
    print('----------\n\n')
    print(solucao[c][0])

