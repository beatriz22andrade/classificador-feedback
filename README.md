# Classificador Inteligente de Feedback de Clientes (IA & NLP)

## 🚀 Sobre o Projeto
Este projeto consiste em um ecossistema completo para a triagem e processamento automatizado de feedbacks de clientes em larga escala. A solução combina técnicas tradicionais de **Processamento de Linguagem Natural (NLP)** com o poder de **Modelos de Linguagem de Grande Escala (LLMs)**, encapsulados em uma API assíncrona de alta performance.

O grande diferencial deste projeto é a **otimização de custos e performance**: o sistema utiliza um pipeline léxico de NLP clássico para fazer uma triagem inicial dos dados. Avaliações positivas são arquivadas de forma econômica, enquanto feedbacks neutros ou críticos acionam uma cadeia inteligente generativa que categoriza o problema e gera uma resposta de desculpas empática e personalizada em tempo real.

---

## 🛠️ Tecnologias e Ferramentas

### Back-End & Dados
- **Python 3.12:** Base do desenvolvimento de toda a lógica de programação.
- **FastAPI:** Framework web assíncrono de alto desempenho usado para expor os endpoints REST.
- **Pandas:** Utilizado para a manipulação rápida e estruturação dos feedbacks em formato de DataFrames na memória.

### Inteligência Artificial & NLP
- **spaCy (Modelo `pt_core_news_sm`):** Responsável pelo pipeline de NLP clássico (tokenização, remoção de stopwords e lematização para extração da raiz das palavras).
- **LangChain (LCEL):** Orquestrador de IA usado para ligar componentes de prompt, modelos de chat e formatadores de saída em cadeia (*chaining*).
- **Groq API (Llama 3 8B):** Infraestrutura de LLM executada com temperatura zero para respostas ultra rápidas, baratas e estritamente determinísticas.

### DevOps & Boas Práticas
- **Docker (Multi-Stage Build):** Containerização otimizada para reduzir o tamanho final da imagem (removendo pacotes C de compilação pós-instalação das bibliotecas de NLP).
- **Git & Conventional Commits:** Controle de versão profissional utilizando prefixos semânticos claros (`feat:`, `fix:`, `chore:`, `docs:`).

---

## 🏗️ Arquitetura do Pipeline de Dados

O fluxo de dados do endpoint `POST /analisar` segue a seguinte linha de execução:

1. **Validação:** O FastAPI recebe e valida o payload JSON usando esquemas do **Pydantic**.
2. **Normalização (NLP):** O texto bruto passa por limpeza regex (remoção de caracteres especiais), conversão para minúsculas e lematização via **spaCy**.
3. **Triagem (Pandas):** Uma análise léxica baseada em dicionários classifica preliminarmente o sentimento da linha do DataFrame.
4. **Enriquecimento com IA (LangChain):** Se o sentimento for crítico, o texto original é enviado para o modelo Llama 3 estruturado via `JsonOutputParser` com contratos rígidos do Pydantic.
5. **Entrega:** A API retorna um JSON unificado e pronto para ser consumido por um front-end ou banco de dados.

---

## ⚙️ Como Executar o Projeto

### Pré-requisitos
- Docker Desktop instalado e integrado com o WSL 2 (caso esteja no Windows).
- Uma API Key configurada na plataforma do [Groq Console](https://console.groq.com/).

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
   cd classificador-feedback
