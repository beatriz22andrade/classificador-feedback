# ==========================================
# Estágio 1: Builder (Construção e Instalação)
# ==========================================
FROM python:3.12-slim AS builder

WORKDIR /app

# Instala dependências do sistema operacional necessárias para compilar pacotes C (comum em NLP)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas o arquivo de dependências para aproveitar o cache de camadas do Docker
COPY requirements.txt .

# Instala as dependências do Python dentro de uma pasta local (/app/wheels) para serem movidas depois
RUN pip install --no-cache-dir --user -r requirements.txt

# Baixa o modelo do spaCy diretamente no escopo do usuário do builder
RUN python -m spacy download pt_core_news_sm --user

# ==========================================
# Estágio 2: Runner (Imagem Final de Produção)
# ==========================================
FROM python:3.12-slim AS runner

WORKDIR /app

# Variáveis de ambiente importantes para otimizar o Python no Docker
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/root/.local/bin:$PATH

# Copia apenas as bibliotecas e pacotes instalados no estágio do Builder
COPY --from=builder /root/.local /root/.local

# Copia o código-fonte da aplicação para o contêiner
COPY ./app /app/app
COPY ./src /app/src
# Nota: O arquivo .env NÃO deve ser copiado para dentro da imagem por segurança!

# Expõe a porta padrão que o FastAPI vai rodar
EXPOSE 8000

# Comando para rodar o Uvicorn apontando para a produção (sem a flag --reload que gasta CPU)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]