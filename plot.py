from utils import _filter

def exportGradeHorarios(solucao, config):
    csv = open('grade.csv', 'w')
    for s in range(0, config['S']):
        csv.write(f'SALA: {s}\n')
        csv.write(f'*\t')
        for t in range(0, config['T']):
            csv.write(f'{t}\t')

        csv.write('\n')
        for d in range(0, config['D']):
            for t in range(0, config['T']):
                if t == 0:
                    csv.write(f'{d}\t')
                filterF = lambda cirurgia : cirurgia['dia'] == d and cirurgia['sala'] == s and (cirurgia['horaInicio'] == t or cirurgia['horaFim'] == t)
                cirurgiasDiaSala = _filter(solucao, filterF)
                if len(cirurgiasDiaSala) == 0:
                    csv.write(f'-\t')
                else:
                    c = list(cirurgiasDiaSala.keys())[0]
                    csv.write(f'{c}\t')
            csv.write('\n')
        
        csv.write('\n\n')


    csv.close()
       