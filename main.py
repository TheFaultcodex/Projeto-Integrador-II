##Script básico para a tratamento báisco de dados + importação de bibliotecas essenciais.
from src.limpeza import carregar, resumo
from src.analise import imprimir_resumo, gerar_todos
 
ARQUIVO_CSV = "data/respostas.csv"
 
df = carregar(ARQUIVO_CSV)
resumo(df)
imprimir_resumo(df)
gerar_todos(df)