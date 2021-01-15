import pandas as pd
import matplotlib.pyplot as plt

titulo = "σ1=10, σ2=5, σ3=15. Objetivo: 21807.5"
output = "allOps_greedy_randOnly_10-5-15__N50_t21807_fullrand_s70_p1-4_w20_t5-20_e5_g20"

files = [
    ("resultados/times_resultado_i3.csv.txt", "Legenda"),
    # Acrescentar mais arquivos aqui
]


fig = plt.Figure()

for f in files:
    lab = f[1]
    data = pd.read_table(f[0], names=[lab])
    # tetoOld = f[2]

    data = data.sort_values(by=[lab])

    times = data[lab].tolist()

    N = len(times)

    prob = [(i+1)/N for i in range(N)]

    plt.step(times, prob,  where='post', label=lab)

plt.xlabel("Tempo (s)")
plt.ylabel("Probabilidade Acumulada")
plt.title(titulo)
plt.grid(color='grey', linestyle='-', linewidth=1, alpha=.1)
plt.legend()

# plt.savefig(f"{output}.pdf")
plt.show()