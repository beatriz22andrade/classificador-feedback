import spacy
import pandas as pd
import re

# Modelo leve de português do spaCy
try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    raise ImportError("O modelo pt_core_news_sm do spaCy não foi encontrado. Execute o comando de download.")

def limpar_texto(texto: str) -> str:
    """
    Função clássica de NLP para limpar e padronizar o texto do review:
    1. Transforma em letras minúsculas.
    2. Remove pontuações e caracteres especiais.
    3. Remove Stopwords (palavras comuns que não agregam contexto, como 'de', 'para', 'com').
    4. Aplica Lematização (reduz a palavra ao seu formato raiz. Ex: 'comi', 'comeu' -> 'comer').
    """
    if not isinstance(texto, str) or not texto.strip():
        return ""
    
    # Limpeza: Letras em minúsculos e remoção de caracteres especiais / espaços extras
    texto_limpo = texto.lower()
    texto_limpo = re.sub(r'[^\w\s]', '', texto_limpo)
    texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
    
    # Processa o texto com o pipeline do spaCy
    doc = nlp(texto_limpo)
    
    # 3 e 4. Filtragem de stopwords e extração do Lemma (raiz da palavra)
    tokens_validos = [
        token.lemma_ for token in doc 
        if not token.is_stop and not token.is_space
    ]
    
    return " ".join(tokens_validos)

def analisar_sentimento_lexico(texto_limpo: str) -> str:
    """
    Uma abordagem clássica e simples de NLP baseada em regras (Léxico).
    Verifica a presença de palavras-chave fortemente positivas ou negativas.
    Isso ajuda a fazer uma triagem rápida antes de gastar tokens com a IA.
    """
    # Listas simplificada (abordagem baseada em dicionário)
    palavras_positivas = {'bom', 'otimo', 'excelente', 'maravilhoso', 'gostar', 'amar', 'perfeito', 'recomendar'}
    palavras_negativas = {'ruim', 'pessimo', 'horrivel', 'quebrar', 'defeito', 'odiar', 'atrasar', 'errado', 'nao'}
    
    palavras_texto = set(texto_limpo.split())
    
    score_positivo = len(palavras_texto.intersection(palavras_positivas))
    score_negativo = len(palavras_texto.intersection(palavras_negativas))
    
    if score_negativo > score_positivo:
        return "NEGATIVO"
    elif score_positivo > score_negativo:
        return "POSITIVO"
    return "NEUTRO"

def processar_lote_feedbacks(feedbacks: list[str]) -> pd.DataFrame:
    """
    Usa o Pandas para estruturar os dados recebidos, simulando a manipulação
    de dados em larga escala que empresas de tecnologia fazem.
    """
    # Cria o DataFrame original do Pandas
    df = pd.DataFrame({"texto_original": feedbacks})
    
    # Aplica a limpeza de NLP linha por linha 
    df["texto_processado"] = df["texto_original"].apply(limpar_texto)
    
    # Aplica a análise de sentimento inicial estruturada
    df["analise_inicial"] = df["texto_processado"].apply(analisar_sentimento_lexico)
    
    return df