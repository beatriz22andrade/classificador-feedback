from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from app.config import settings

# 1. Definindo a estrutura exata para que a IA retorne usando Pydantic.
# Isso garante consistência nos dados e evita respostas aleatórias.
class AnaliseIAFeedback(BaseModel):
    categoria_erro: str = Field(description="A categoria do problema. Deve ser estritamente uma destas: LOGISTICA, QUALIDADE_PRODUTO, ATENDIMENTO, PRECO ou OUTROS.")
    motivo_resumido: str = Field(description="Um resumo do problema real em até 3 palavras.")
    resposta_cliente: str = Field(description="Uma resposta empática, profissional, em português brasileiro, pedindo desculpas e indicando que o suporte entrará em contato.")

def analisar_feedback_critico_com_ia(texto_original: str) -> dict:
    """
    Usa LangChain para conectar ao Groq (Llama 3) e processar feedbacks 
    com engenharia de prompt estruturada e saída em formato JSON estável.
    """
    # 2. Inicializa o modelo de IA via Groq de forma leve e rápida
    # Temperatura 0.0 para que a IA seja o mais determinística/técnica possível
    llm = ChatGroq(
        temperature=0.0,
        model_name="llama3-8b-8192",
        groq_api_key=settings.GROQ_API_KEY
    )
    
    # 3. Configura o JsonOutputParser atrelado à nossa estrutura Pydantic
    parser = JsonOutputParser(pydantic_object=AnaliseIAFeedback)
    
    # 4. Prompt estruturado (System + Human)
    # Usamos o parser para injetar as instruções de formato direto no prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "Você é um especialista em Customer Experience (Sucesso do Cliente). "
            "Sua tarefa é analisar feedbacks negativos de clientes e extrair informações críticas estruturadas.\n\n"
            "{format_instructions}"
        )),
        ("human", "Analise o seguinte feedback de cliente: '{texto_cliente}'")
    ])
    
    # 5. Montamos a Chain usando o LangChain Expression Language (LCEL)
    # O operador '|' conecta a entrada -> prompt -> modelo -> formatador de saída
    chain = prompt | llm | parser
    
    try:
        # Executa a chamada passando as variáveis necessárias
        resultado_json = chain.invoke({
            "texto_cliente": texto_original,
            "format_instructions": parser.get_format_instructions()
        })
        return resultado_json
    except Exception as e:
        # Fallback de erro caso a API falhe ou mude o formato
        return {
            "categoria_erro": "OUTROS",
            "motivo_resumido": "Erro no processamento",
            "resposta_cliente": f"Prezado cliente, identificamos sua insatisfação e nossa equipe de suporte entrará em contato o quanto antes."
        }