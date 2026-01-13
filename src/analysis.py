import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- CONFIGURAZIONE ---
CSV_PATH = "../result/experiment_results.csv"
OUTPUT_DIR = "../result/plots"

# Crea la cartella per i grafici se non esiste
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Leggi i dati
try:
    df = pd.read_csv(CSV_PATH)
except FileNotFoundError:
    print(f"Errore: Non trovo il file {CSV_PATH}. Assicurati di aver eseguito experiments.py")
    exit()

# Imposta lo stile
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 12})

def save_plot(filename):
    path = os.path.join(OUTPUT_DIR, filename)
    plt.tight_layout()
    plt.savefig(path, dpi=300)
    print(f"Grafico salvato in: {path}")
    plt.close()

# ---------------------------------------------------------
# 1. GRAFICO DEI TEMPI DI ESECUZIONE (Scala Logaritmica)
# ---------------------------------------------------------
plt.figure(figsize=(10, 6))
chart = sns.barplot(
    data=df,
    x="Problem",
    y="Time",
    hue="Algorithm",
    palette="viridis"
)

# Imposta scala logaritmica perché i tempi variano da 0.001s a 100s+
chart.set_yscale("log")
plt.title("Execution Time Comparison (Log Scale)", fontsize=16)
plt.ylabel("Time (seconds) - Log Scale")
plt.xlabel("Problem Instance")
plt.xticks(rotation=45)
plt.grid(True, which="minor", ls="--", alpha=0.3)

save_plot("plot_time.png")

# ---------------------------------------------------------
# 2. GRAFICO DEI NODI ESPANSI (Scala Logaritmica)
# ---------------------------------------------------------
plt.figure(figsize=(10, 6))
chart = sns.barplot(
    data=df,
    x="Problem",
    y="Expanded",
    hue="Algorithm",
    palette="magma"
)

# Scala logaritmica necessaria: Blind search esplode esponenzialmente
chart.set_yscale("log")
plt.title("Expanded Nodes Comparison (Log Scale)", fontsize=16)
plt.ylabel("Nodes Expanded - Log Scale")
plt.xlabel("Problem Instance")
plt.xticks(rotation=45)

save_plot("plot_expanded.png")

# ---------------------------------------------------------
# 3. GRAFICO DELLA LUNGHEZZA DEL PIANO (Validazione Ottimalità)
# ---------------------------------------------------------
plt.figure(figsize=(10, 6))
chart = sns.barplot(
    data=df,
    x="Problem",
    y="Cost",
    hue="Algorithm",
    palette="rocket"
)

# Qui scala lineare va bene, i costi devono essere identici
plt.title("Solution Cost (Optimality Check)", fontsize=16)
plt.ylabel("Plan Length (Number of Actions)")
plt.xlabel("Problem Instance")
plt.xticks(rotation=45)
# Aggiungiamo i valori sopra le barre per mostrare che sono uguali
for container in chart.containers:
    chart.bar_label(container)

save_plot("plot_cost.png")

print("Generazione completata.")
