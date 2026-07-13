from fastapi import FastAPI
from app.config import settings

# Inicializa o FastAPI com metadados organizados
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="API para análise automatizada de reviews usando NLP clássico e IA Generativa (Groq/LangChain)."
)

# Rota de "Health Check" (Checagem de Saúde da API)
# Essencial em projetos profissionais para que sistemas de monitoramento verifiquem se a API está online.
@app.get("/", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION
    }