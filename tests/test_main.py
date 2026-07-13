from fastapi.testclient import TestClient
from app.main import app
from src.nlp_utils import limpar_texto

client = TestClient(app)

# 1. Teste do NLP (spaCy)
def test_limpeza_texto_nlp():
    texto_sujo = "O produto é maravilhoso, chegou super rápido!"
    texto_limpo = limpar_texto(texto_sujo)
    
    # O spaCy deve lematizar e remover stopwords
    assert "maravilhoso" in texto_limpo
    assert "rapido" in texto_limpo or "rápido" in texto_limpo
    assert " o " not in f" {texto_limpo} "

# 2. Teste de Integração da Rota do FastAPI
def test_health_check_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"