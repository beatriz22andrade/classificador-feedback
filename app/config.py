import os
from dotenv import load_dotenv

# Carrega as variáveis contidas no arquivo .env
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Classificador Inteligente de Feedback de Clientes"
    PROJECT_VERSION: str = "1.0.0"
    
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    if not GROQ_API_KEY:
        raise ValueError("CRÍTICO: A variável GROQ_API_KEY não foi encontrada no arquivo .env")

settings = Settings()