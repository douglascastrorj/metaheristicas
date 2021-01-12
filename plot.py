from utils import _filter
import matplotlib.pyplot as plt

def exportGradeHorarios(solucao, config):
    csv = open('grade.csv', 'w')
    for s in range(0, config['S']):
        csv.write(f'SALA: {s}\n')
        csv.write(f'*\t\t')
        for t in range(0, config['T']):
            csv.write(f'{t}\t')

        csv.write('\n')
        for d in range(0, config['D']):
            for t in range(0, config['T']):
                filterF = lambda cirurgia : cirurgia['dia'] == d and cirurgia['sala'] == s and (cirurgia['horaInicio'] == t or cirurgia['horaFim'] == t)
                cirurgiasDiaSala = _filter(solucao, filterF)

                filterF2 = lambda cirurgia : cirurgia['dia'] == d and cirurgia['sala'] == s
                cirurgiasDiaSala2 = _filter(solucao, filterF2)

                e = '-'
                if len(cirurgiasDiaSala2) > 0:
                    e = cirurgiasDiaSala2[ list(cirurgiasDiaSala2.keys())[0]]['especialidade']

                if t == 0:
                    csv.write(f'{e} / {d}\t')
                
                if len(cirurgiasDiaSala) == 0:
                    csv.write(f'-\t')
                else:
                    c = list(cirurgiasDiaSala.keys())[0]
                    csv.write(f'{c}\t')
            csv.write('\n')
        
        csv.write('\n\n')


    csv.close()
       
def plotChart(history, title):
    # print(history)
    plt.plot([h['fo'] for h in history])
    plt.ylabel('FO')
    plt.suptitle(title)
    plt.show()