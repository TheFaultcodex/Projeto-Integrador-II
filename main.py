import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Caminhos
ARQUIVO_CSV = "data/respostas.csv"
PASTA_GRAFICOS = "graficos"
os.makedirs(PASTA_GRAFICOS, exist_ok=True)

CORES = ["#E63946", "#457B9D", "#F4A261", "#2A9D8F", "#E9C46A", "#264653"]

df = pd.read_csv(ARQUIVO_CSV)

# Renomeia colunas para nomes mais curtos e fáceis de usar
df.columns = [
    "timestamp",
    "empresa",
    "tempo_cliente",
    "segmento",
    "satisfacao_geral",
    "retorno_anuncios",
    "atendimento_equipe",
    "alcance_radio",
    "indicaria",
    "sugestoes",
]

df["timestamp"] = pd.to_datetime(df["timestamp"], dayfirst=True)
df["empresa"] = df["empresa"].fillna("Não informado").str.strip()
df["sugestoes"] = df["sugestoes"].fillna("Sem sugestão").str.strip()

data_inicio = df["timestamp"].min().strftime("%d/%m/%Y")
data_fim    = df["timestamp"].max().strftime("%d/%m/%Y")

print("Análise de satisfação — Rádio Massa FM Itapema")
print("-" * 50)
print(f"Respostas coletadas : {len(df)}")
print(f"Período             : {data_inicio} a {data_fim}")
print(f"Empresas            : {df['empresa'].nunique()} identificadas\n")

print("Respostas por segmento:")
print(df["segmento"].value_counts().to_string())

print("\nTempo como cliente:")
print(df["tempo_cliente"].value_counts().to_string())

colunas_notas = [
    "satisfacao_geral",
    "retorno_anuncios",
    "atendimento_equipe",
    "alcance_radio",
    "indicaria",
]

labels_notas = [
    "Satisfação geral",
    "Retorno dos anúncios",
    "Atendimento da equipe",
    "Alcance / divulgação",
    "Indicaria a rádio",
]

medias = df[colunas_notas].mean().round(2)
media_geral = medias.mean().round(2)

print("\nMédias por indicador (0 a 10):")
for label, col in zip(labels_notas, colunas_notas):
    print(f"  {label:<25} {medias[col]:.2f}")
print(f"\n  {'Média geral':<25} {media_geral:.2f}")

fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor("#1E1E2E")
ax.set_facecolor("#1E1E2E")

y = np.arange(len(labels_notas))
barras = ax.barh(y, medias.values, color=CORES[:len(labels_notas)], height=0.55, edgecolor="none")

for barra, valor in zip(barras, medias.values):
    ax.text(valor - 0.3, barra.get_y() + barra.get_height() / 2,
            f"{valor:.1f}", va="center", ha="right",
            fontsize=12, fontweight="bold", color="white")

ax.set_yticks(y)
ax.set_yticklabels(labels_notas, color="white", fontsize=11)
ax.set_xlim(0, 11)
ax.set_xlabel("Nota média (0–10)", color="#AAAAAA", fontsize=10)
ax.set_title("Indicadores de satisfação — Massa FM Itapema", color="white", fontsize=13, pad=14)
ax.tick_params(colors="#AAAAAA")
ax.spines[["top", "right", "bottom", "left"]].set_visible(False)
ax.xaxis.set_tick_params(colors="#AAAAAA")
ax.axvline(7, color="#FFFFFF", linewidth=0.6, linestyle="--", alpha=0.4, label="Referência 7.0")
ax.legend(facecolor="#2A2A3E", labelcolor="white", fontsize=9, loc="lower right")

plt.tight_layout()
plt.savefig(f"{PASTA_GRAFICOS}/01_medias_indicadores.png", dpi=150, bbox_inches="tight", facecolor="#1E1E2E")
plt.close()
print(f"\nGráfico salvo: {PASTA_GRAFICOS}/01_medias_indicadores.png")

contagem_seg = df["segmento"].value_counts()

fig, ax = plt.subplots(figsize=(7, 7))
fig.patch.set_facecolor("#1E1E2E")
ax.set_facecolor("#1E1E2E")

wedges, texts, autotexts = ax.pie(
    contagem_seg.values,
    labels=contagem_seg.index,
    autopct="%1.0f%%",
    colors=CORES[:len(contagem_seg)],
    startangle=140,
    wedgeprops=dict(edgecolor="#1E1E2E", linewidth=2),
    textprops=dict(color="white", fontsize=11),
)
for at in autotexts:
    at.set_fontsize(12)
    at.set_fontweight("bold")

ax.set_title("Segmentos dos clientes anunciantes", color="white", fontsize=13, pad=16)
plt.tight_layout()
plt.savefig(f"{PASTA_GRAFICOS}/02_segmentos.png", dpi=150, bbox_inches="tight", facecolor="#1E1E2E")
plt.close()
print(f"Gráfico salvo: {PASTA_GRAFICOS}/02_segmentos.png")

ordem_tempo = ["Menos de 3 meses", "De 3 a 6 meses", "De 6 meses a 1 ano", "Mais de 1 ano"]
contagem_tempo = df["tempo_cliente"].value_counts().reindex(
    [t for t in ordem_tempo if t in df["tempo_cliente"].values]
)

fig, ax = plt.subplots(figsize=(8, 5))
fig.patch.set_facecolor("#1E1E2E")
ax.set_facecolor("#1E1E2E")

bars = ax.bar(contagem_tempo.index, contagem_tempo.values,
              color=CORES[:len(contagem_tempo)], edgecolor="none", width=0.5)

for bar, val in zip(bars, contagem_tempo.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
            str(val), ha="center", va="bottom", color="white", fontsize=12, fontweight="bold")

ax.set_ylabel("Número de clientes", color="#AAAAAA", fontsize=10)
ax.set_title("Tempo de relacionamento com a Massa FM", color="white", fontsize=13, pad=14)
ax.tick_params(colors="#AAAAAA")
ax.set_yticks(range(0, contagem_tempo.max() + 2))
ax.spines[["top", "right", "left"]].set_visible(False)
ax.spines["bottom"].set_color("#444444")
ax.yaxis.set_tick_params(colors="#AAAAAA")

plt.tight_layout()
plt.savefig(f"{PASTA_GRAFICOS}/03_tempo_cliente.png", dpi=150, bbox_inches="tight", facecolor="#1E1E2E")
plt.close()
print(f"Gráfico salvo: {PASTA_GRAFICOS}/03_tempo_cliente.png")

valores_radar = list(medias.values) + [medias.values[0]]
angulos = np.linspace(0, 2 * np.pi, len(labels_notas), endpoint=False).tolist()
angulos += angulos[:1]

fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
fig.patch.set_facecolor("#1E1E2E")
ax.set_facecolor("#1E1E2E")

ax.plot(angulos, valores_radar, color="#E63946", linewidth=2)
ax.fill(angulos, valores_radar, color="#E63946", alpha=0.25)

ax.set_xticks(angulos[:-1])
ax.set_xticklabels(labels_notas, color="white", fontsize=10)
ax.set_yticks([2, 4, 6, 8, 10])
ax.set_yticklabels(["2", "4", "6", "8", "10"], color="#AAAAAA", fontsize=8)
ax.set_ylim(0, 10)
ax.grid(color="#444444", linewidth=0.5)
ax.spines["polar"].set_color("#444444")
ax.set_title("Visão geral dos indicadores", color="white", fontsize=13, pad=20)

plt.tight_layout()
plt.savefig(f"{PASTA_GRAFICOS}/04_radar.png", dpi=150, bbox_inches="tight", facecolor="#1E1E2E")
plt.close()
print(f"Gráfico salvo: {PASTA_GRAFICOS}/04_radar.png")

fig, ax = plt.subplots(figsize=(8, 5))
fig.patch.set_facecolor("#1E1E2E")
ax.set_facecolor("#1E1E2E")

x = np.arange(len(df))
largura = 0.35

ax.bar(x - largura / 2, df["satisfacao_geral"], largura,
       label="Satisfação geral", color="#E63946", edgecolor="none")
ax.bar(x + largura / 2, df["retorno_anuncios"], largura,
       label="Retorno dos anúncios", color="#457B9D", edgecolor="none")

# Linhas de média tracejadas
ax.axhline(medias["satisfacao_geral"], color="#E63946", linewidth=1, linestyle="--", alpha=0.5)
ax.axhline(medias["retorno_anuncios"], color="#457B9D", linewidth=1, linestyle="--", alpha=0.5)

ax.set_xticks(x)
ax.set_xticklabels([f"R{i+1}" for i in range(len(df))], color="#AAAAAA", fontsize=10)
ax.set_yticks(range(0, 12, 2))
ax.set_ylim(0, 11)
ax.set_ylabel("Nota", color="#AAAAAA", fontsize=10)
ax.set_title("Satisfação geral vs retorno dos anúncios", color="white", fontsize=12, pad=14)
ax.tick_params(colors="#AAAAAA")
ax.legend(facecolor="#2A2A3E", labelcolor="white", fontsize=10)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.spines["bottom"].set_color("#444444")

plt.tight_layout()
plt.savefig(f"{PASTA_GRAFICOS}/05_satisfacao_vs_retorno.png", dpi=150, bbox_inches="tight", facecolor="#1E1E2E")
plt.close()
print(f"Gráfico salvo: {PASTA_GRAFICOS}/05_satisfacao_vs_retorno.png")

ponto_forte_col = medias.idxmax()
ponto_fraco_col = medias.idxmin()
label_forte = labels_notas[colunas_notas.index(ponto_forte_col)]
label_fraco  = labels_notas[colunas_notas.index(ponto_fraco_col)]

media_indicaria = medias["indicaria"]
if media_indicaria >= 9:
    classificacao_nps = "zona de promotores (alta fidelização)"
elif media_indicaria >= 7:
    classificacao_nps = "zona neutra (satisfeitos, sem entusiasmo)"
else:
    classificacao_nps = "zona de detratores (risco de churn)"

# Filtra sugestões que têm conteúdo real
sugestoes_validas = df[
    ~df["sugestoes"].str.lower().str.contains("sem sugestão|não sei|não entendo", na=False)
    & (df["sugestoes"].str.len() > 10)
]["sugestoes"].tolist()

print("\nResumo da análise")
print("-" * 50)
print(f"Ponto mais forte : {label_forte} ({medias[ponto_forte_col]:.1f}/10)")
print(f"Ponto mais fraco : {label_fraco} ({medias[ponto_fraco_col]:.1f}/10)")
print(f"Indicaria a rádio: média {media_indicaria:.1f} — {classificacao_nps}")

if sugestoes_validas:
    print(f"\nSugestões com conteúdo ({len(sugestoes_validas)}):")
    for s in sugestoes_validas:
        print(f"  - {s}")
else:
    print("\nNenhuma sugestão com conteúdo relevante foi registrada.")

print(f"\nGráficos disponíveis em: ./{PASTA_GRAFICOS}/")
