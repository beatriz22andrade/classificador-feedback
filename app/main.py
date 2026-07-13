from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.config import settings
from src.nlp_utils import processar_lote_feedbacks
from src.ai_utils import analisar_feedback_critico_com_ia

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="API para análise automatizada de reviews usando NLP clássico e IA Generativa (Groq/LangChain)."
)

# 1. Modelo Pydantic para validar os dados que chegam na requisição HTTP
class LoteFeedbackInput(BaseModel):
    feedbacks: list[str]

@app.get("/", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION
    }

# 2. A rota principal POST que amarra todo o nosso ecossistema
@app.post("/analisar", tags=["Processamento de IA & NLP"])
async def analisar_lote_feedbacks(dados: LoteFeedbackInput):
    if not dados.feedbacks:
        raise HTTPException(status_code=400, detail="A lista de feedbacks não pode estar vazia.")
    
    try:
        # Etapa 1: (NLP Clássico)
        df_processado = processar_lote_feedbacks(dados.feedbacks)
        
        resultados_finais = []
        
        # Etapa 2: Enriquecer os dados com o LangChain
        for _, linha in df_processado.iterrows():
            item_resultado = {
                "texto_original": linha["texto_original"],
                "texto_limpo_nlp": linha["texto_processado"],
                "triagem_inicial": linha["analise_inicial"]
            }
            
            # Se a triagem inicial do NLP indicar que o feedback não é estritamente POSITIVO,
            # usa-se a LLM para entender o problema.
            if linha["analise_inicial"] in ["NEGATIVO", "NEUTRO"]:
                analise_ia = analisar_feedback_critico_com_ia(linha["texto_original"])
                # Junta os dados do dicionário gerado pela IA ao nosso resultado
                item_resultado.update(analise_ia)
            else:
                # Se for positivo, economizamos tokens da API e geramos dados estáticos simples
                item_resultado.update({
                    "categoria_erro": "NENHUM",
                    "motivo_resumido": "Sucesso",
                    "resposta_cliente": "Agradecemos muito pelo seu feedback positivo! Conte sempre conosco."
                })
                
            resultados_finais.append(item_resultado)
            
        return {
            "total_processado": len(resultados_finais),
            "resultados": resultados_finais
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no processamento do lote: {str(e)}")