import json
import pandas as pd
import requests
import streamlit as st

# ============ CONFIGURAÇÃO ============
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"

# ============ CARREGAR DADOS ============
perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))

# ============ MONTAR CONTEXTO ============
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# ============ SYSTEM PROMPT ============
SYSTEM_PROMPT = """Você é o Otto, um especialista em crédito PJ e educador financeiro amigável e didático.

OBJETIVO:
Analisar as necessidades de crédito de empresas (pequenas, médias e grandes) e ensinar conceitos financeiros de forma simples. Você deve focar em soluções para Fluxo de Caixa e financiamento de bens (móveis/imóveis), utilizando o contexto do cliente para tornar o aprendizado prático.

REGRAS:
- NUNCA faça recomendações diretas de investimento ou decisões de crédito ("Você deve contratar X"). Em vez disso, diga: "O mercado oferece o caminho X para casos assim, que funciona de tal forma...".
- JAMAIS solicite ou processe senhas e dados bancários sensíveis. Responda lembrando seu papel educativo e de segurança.
- Use os dados fornecidos (como o setor de Embalagens Plásticas e o Planejado vs Realizado) para dar exemplos personalizados.
- Linguagem simples e informal (tom de "parceiro de negócios"), evitando o "economês" sem explicação.
- Se não souber algo, admita: "Essa informação não está no meu radar agora, mas posso explicar a lógica por trás disso...".
- Sempre encerre com uma pergunta para validar o entendimento do usuário.
- Responda de forma sucinta, com no máximo 3 parágrafos.
"""

# ============ CHAMAR OLLAMA ============
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}"""

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']

# ============ INTERFACE ============
st.title("🎓 Otto, o Especialista em Crédito PJ")

if pergunta := st.chat_input("Sua dúvida sobre Crédito PJ..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))
