import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from src.limpeza import COLUNAS_NOTAS, LABELS_NOTAS, ORDEM_TEMPO

PASTA_GRAFICOS = "graficos"
CORES = ["#E63946", "#457B9D", "#F4A261", "#2A9D8F", "#E9C46A", "#264653"]

os.makedirs(PASTA_GRAFICOS, exist_ok=True)


# ---------------------------------------------------------------------------
# Estatísticas
# ---------------------------------------------------------------------------

def calcular_medias(df: pd.DataFrame) -> pd.Series:
    """Retorna a média de cada indicador de nota."""
    return df[COLUNAS_NOTAS].mean().round(2)


def classificar_nps(media: float) -> str:
    """Classifica a média de 'indicaria' conforme zonas de NPS."""
    if media >= 9:
        return "zona de promotores (alta fidelização)"
    elif media >= 7:
        return "zona neutra (satisfeitos, sem entusiasmo)"
    else:
        return "zona de detratores (risco de churn)"


def sugestoes_validas(df: pd.DataFrame) -> list:
    """Retorna apenas sugestões com conteúdo relevante."""
    ignorar = "sem sugestão|não sei|não entendo|nenhuma|n/a"
    mask = (
        ~df["sugestoes"].str.lower().str.contains(ignorar, na=False)
        & (df["sugestoes"].str.len() > 10)
    )
    return df.loc[mask, "sugestoes"].tolist()


def imprimir_resumo(df: pd.DataFrame) -> None:
    """Imprime o resumo estatístico completo no terminal."""
    medias = calcular_medias(df)
    media_geral = medias.mean().round(2)

    print("Médias por indicador (0 a 10):")
    for label, col in zip(LABELS_NOTAS, COLUNAS_NOTAS):
        print(f"  {label:<25} {medias[col]:.2f}")
    print(f"\n  {'Média geral':<25} {media_geral:.2f}")

    forte_col = medias.idxmax()
    fraco_col  = medias.idxmin()
    label_forte = LABELS_NOTAS[COLUNAS_NOTAS.index(forte_col)]
    label_fraco  = LABELS_NOTAS[COLUNAS_NOTAS.index(fraco_col)]

    print("\nResumo da análise")
    print("-" * 40)
    print(f"Ponto mais forte : {label_forte} ({medias[forte_col]:.1f}/10)")
    print(f"Ponto mais fraco : {label_fraco} ({medias[fraco_col]:.1f}/10)")
    print(f"Indicaria a rádio: média {medias['indicaria']:.1f} — {classificar_nps(medias['indicaria'])}")

    validas = sugestoes_validas(df)
    if validas:
        print(f"\nSugestões com conteúdo ({len(validas)}):")
        for s in validas:
            print(f"  - {s}")
    else:
        print("\nNenhuma sugestão com conteúdo relevante foi registrada.")


# ---------------------------------------------------------------------------
# Gráficos
# ---------------------------------------------------------------------------

def _estilo_base(fig, ax):
    """Aplica o tema escuro padrão a um par fig/ax."""
    fig.patch.set_facecolor("#1E1E2E")
    ax.set_facecolor("#1E1E2E")


def grafico_medias(df: pd.DataFrame) -> None:
    """Barras horizontais com a média de cada indicador."""
    medias = calcular_medias(df)

    fig, ax = plt.subplots(figsize=(10, 5))
    _estilo_base(fig, ax)

    y = np.arange(len(LABELS_NOTAS))
    barras = ax.barh(y, medias.values, color=CORES[:len(LABELS_NOTAS)],
                     height=0.55, edgecolor="none")

    for barra, valor in zip(barras, medias.values):
        ax.text(valor - 0.3, barra.get_y() + barra.get_height() / 2,
                f"{valor:.1f}", va="center", ha="right",
                fontsize=12, fontweight="bold", color="white")

    ax.set_yticks(y)
    ax.set_yticklabels(LABELS_NOTAS, color="white", fontsize=11)
    ax.set_xlim(0, 11)
    ax.set_xlabel("Nota média (0–10)", color="#AAAAAA", fontsize=10)
    ax.set_title("Indicadores de satisfação — Massa FM Itapema",
                 color="white", fontsize=13, pad=14)
    ax.tick_params(colors="#AAAAAA")
    ax.spines[["top", "right", "bottom", "left"]].set_visible(False)
    ax.xaxis.set_tick_params(colors="#AAAAAA")
    ax.axvline(7, color="#FFFFFF", linewidth=0.6, linestyle="--",
               alpha=0.4, label="Referência 7.0")
    ax.legend(facecolor="#2A2A3E", labelcolor="white", fontsize=9, loc="lower right")

    plt.tight_layout()
    caminho = f"{PASTA_GRAFICOS}/01_medias_indicadores.png"
    plt.savefig(caminho, dpi=150, bbox_inches="tight", facecolor="#1E1E2E")
    plt.close()
    print(f"Gráfico salvo: {caminho}")


def grafico_segmentos(df: pd.DataFrame) -> None:
    """Pizza com a distribuição de segmentos dos clientes."""
    contagem = df["segmento"].value_counts()

    fig, ax = plt.subplots(figsize=(7, 7))
    _estilo_base(fig, ax)

    _, texts, autotexts = ax.pie(
        contagem.values,
        labels=contagem.index,
        autopct="%1.0f%%",
        colors=CORES[:len(contagem)],
        startangle=140,
        wedgeprops=dict(edgecolor="#1E1E2E", linewidth=2),
        textprops=dict(color="white", fontsize=11),
    )
    for at in autotexts:
        at.set_fontsize(12)
        at.set_fontweight("bold")

    ax.set_title("Segmentos dos clientes anunciantes",
                 color="white", fontsize=13, pad=16)
    plt.tight_layout()
    caminho = f"{PASTA_GRAFICOS}/02_segmentos.png"
    plt.savefig(caminho, dpi=150, bbox_inches="tight", facecolor="#1E1E2E")
    plt.close()
    print(f"Gráfico salvo: {caminho}")


def grafico_tempo_cliente(df: pd.DataFrame) -> None:
    """Barras verticais mostrando há quanto tempo cada cliente anuncia."""
    contagem = df["tempo_cliente"].value_counts().reindex(
        [t for t in ORDEM_TEMPO if t in df["tempo_cliente"].values]
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    _estilo_base(fig, ax)

    bars = ax.bar(contagem.index, contagem.values,
                  color=CORES[:len(contagem)], edgecolor="none", width=0.5)

    for bar, val in zip(bars, contagem.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                str(val), ha="center", va="bottom",
                color="white", fontsize=12, fontweight="bold")

    ax.set_ylabel("Número de clientes", color="#AAAAAA", fontsize=10)
    ax.set_title("Tempo de relacionamento com a Massa FM",
                 color="white", fontsize=13, pad=14)
    ax.tick_params(colors="#AAAAAA")
    ax.set_yticks(range(0, contagem.max() + 2))
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color("#444444")
    ax.yaxis.set_tick_params(colors="#AAAAAA")

    plt.tight_layout()
    caminho = f"{PASTA_GRAFICOS}/03_tempo_cliente.png"
    plt.savefig(caminho, dpi=150, bbox_inches="tight", facecolor="#1E1E2E")
    plt.close()
    print(f"Gráfico salvo: {caminho}")


def grafico_radar(df: pd.DataFrame) -> None:
    """Gráfico radar com os cinco indicadores de satisfação."""
    medias = calcular_medias(df)
    valores = list(medias.values) + [medias.values[0]]
    angulos = np.linspace(0, 2 * np.pi, len(LABELS_NOTAS), endpoint=False).tolist()
    angulos += angulos[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("#1E1E2E")
    ax.set_facecolor("#1E1E2E")

    ax.plot(angulos, valores, color="#E63946", linewidth=2)
    ax.fill(angulos, valores, color="#E63946", alpha=0.25)

    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(LABELS_NOTAS, color="white", fontsize=10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["2", "4", "6", "8", "10"], color="#AAAAAA", fontsize=8)
    ax.set_ylim(0, 10)
    ax.grid(color="#444444", linewidth=0.5)
    ax.spines["polar"].set_color("#444444")
    ax.set_title("Visão geral dos indicadores", color="white", fontsize=13, pad=20)

    plt.tight_layout()
    caminho = f"{PASTA_GRAFICOS}/04_radar.png"
    plt.savefig(caminho, dpi=150, bbox_inches="tight", facecolor="#1E1E2E")
    plt.close()
    print(f"Gráfico salvo: {caminho}")


def grafico_satisfacao_vs_retorno(df: pd.DataFrame) -> None:
    """Barras agrupadas comparando satisfação geral e retorno dos anúncios."""
    medias = calcular_medias(df)

    fig, ax = plt.subplots(figsize=(8, 5))
    _estilo_base(fig, ax)

    x = np.arange(len(df))
    largura = 0.35

    ax.bar(x - largura / 2, df["satisfacao_geral"], largura,
           label="Satisfação geral", color="#E63946", edgecolor="none")
    ax.bar(x + largura / 2, df["retorno_anuncios"], largura,
           label="Retorno dos anúncios", color="#457B9D", edgecolor="none")

    ax.axhline(medias["satisfacao_geral"], color="#E63946",
               linewidth=1, linestyle="--", alpha=0.5)
    ax.axhline(medias["retorno_anuncios"], color="#457B9D",
               linewidth=1, linestyle="--", alpha=0.5)

    ax.set_xticks(x)
    ax.set_xticklabels([f"R{i+1}" for i in range(len(df))],
                       color="#AAAAAA", fontsize=10)
    ax.set_yticks(range(0, 12, 2))
    ax.set_ylim(0, 11)
    ax.set_ylabel("Nota", color="#AAAAAA", fontsize=10)
    ax.set_title("Satisfação geral vs retorno dos anúncios",
                 color="white", fontsize=12, pad=14)
    ax.tick_params(colors="#AAAAAA")
    ax.legend(facecolor="#2A2A3E", labelcolor="white", fontsize=10)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color("#444444")

    plt.tight_layout()
    caminho = f"{PASTA_GRAFICOS}/05_satisfacao_vs_retorno.png"
    plt.savefig(caminho, dpi=150, bbox_inches="tight", facecolor="#1E1E2E")
    plt.close()
    print(f"Gráfico salvo: {caminho}")


def gerar_todos(df: pd.DataFrame) -> None:
    """Executa todos os gráficos em sequência."""
    grafico_medias(df)
    grafico_segmentos(df)
    grafico_tempo_cliente(df)
    grafico_radar(df)
    grafico_satisfacao_vs_retorno(df)
    print(f"\nTodos os gráficos salvos em: ./{PASTA_GRAFICOS}/")