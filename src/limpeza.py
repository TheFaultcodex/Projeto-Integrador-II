import pandas as pd

# Colunas esperadas no CSV exportado do Google Forms
COLUNAS = [
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

# Colunas que contêm notas numéricas (0 a 10)
COLUNAS_NOTAS = [
    "satisfacao_geral",
    "retorno_anuncios",
    "atendimento_equipe",
    "alcance_radio",
    "indicaria",
]

# Rótulos legíveis para cada coluna de nota, usados nos gráficos
LABELS_NOTAS = [
    "Satisfação geral",
    "Retorno dos anúncios",
    "Atendimento da equipe",
    "Alcance / divulgação",
    "Indicaria a rádio",
]

# Ordem cronológica esperada para a coluna tempo_cliente
ORDEM_TEMPO = [
    "Menos de 3 meses",
    "De 3 a 6 meses",
    "De 6 meses a 1 ano",
    "Mais de 1 ano",
]


def carregar(caminho: str) -> pd.DataFrame:
    """Lê o CSV e aplica toda a limpeza necessária.

    Etapas realizadas:
    - Renomeia as colunas para nomes padronizados
    - Converte o timestamp para datetime
    - Preenche campos de texto vazios com valores padrão
    - Garante que as notas sejam numéricas
    - Remove linhas completamente duplicadas
    - Remove linhas sem nenhuma nota preenchida

    Retorna um DataFrame limpo pronto para análise.
    """
    df = pd.read_csv(caminho)

    # Renomeia independente do cabeçalho original do Forms
    df.columns = COLUNAS

    # Timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"], dayfirst=True)

    # Texto
    df["empresa"] = df["empresa"].fillna("Não informado").str.strip()
    df["segmento"] = df["segmento"].fillna("Não informado").str.strip()
    df["tempo_cliente"] = df["tempo_cliente"].fillna("Não informado").str.strip()
    df["sugestoes"] = df["sugestoes"].fillna("Sem sugestão").str.strip()

    # Notas: converte para numérico, erros viram NaN
    for col in COLUNAS_NOTAS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove linhas duplicadas
    antes = len(df)
    df = df.drop_duplicates()
    duplicatas = antes - len(df)
    if duplicatas > 0:
        print(f"Limpeza: {duplicatas} linha(s) duplicada(s) removida(s).")

    # Remove linhas sem nenhuma nota (provavelmente submissões vazias)
    df = df.dropna(subset=COLUNAS_NOTAS, how="all")

    return df.reset_index(drop=True)


def resumo(df: pd.DataFrame) -> None:
    """Imprime um resumo básico dos dados carregados."""
    data_inicio = df["timestamp"].min().strftime("%d/%m/%Y")
    data_fim    = df["timestamp"].max().strftime("%d/%m/%Y")

    print("Dados carregados")
    print("-" * 40)
    print(f"Respostas  : {len(df)}")
    print(f"Período    : {data_inicio} a {data_fim}")
    print(f"Empresas   : {df['empresa'].nunique()} identificadas")
    print(f"Segmentos  : {df['segmento'].nunique()} categorias")

    nulos = df[COLUNAS_NOTAS].isnull().sum()
    if nulos.any():
        print("\nNotas ausentes por coluna:")
        print(nulos[nulos > 0].to_string())
    print()