import json
import pandas as pd
import streamlit as st
from openai import OpenAI

# ============ CONFIGURAÇÃO ============
client = OpenAI(api_key="SUA_API_KEY_AQUI")  # ou use variável de ambiente

MODELO = "gpt-4.1-mini"  # custo-benefício bom

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
Analisar as necessidades de crédito de empresas (pequenas, médias e grandes) e ensinar conceitos financeiros de forma simples.

REGRAS:
- NUNCA faça recomendações diretas de investimento ou decisões de crédito.
- JAMAIS solicite dados sensíveis.
- Use exemplos com base nos dados fornecidos.
- Linguagem simples e informal.
- Sempre encerre com uma pergunta.
- Máximo de 3 parágrafos.
"""

# ============ CHAMAR OPENAI ============
def perguntar(msg):
    response = client.responses.create(
        model=MODELO,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
CONTEXTO DO CLIENTE:
{contexto}

Pergunta: {msg}
"""
            }
        ],
        temperature=0.7
    )

    return response.output_text


# ============ INTERFACE ============
st.title("🎓 Otto, o Especialista em Crédito PJ")

if pergunta := st.chat_input("Sua dúvida sobre Crédito PJ..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        resposta = perguntar(pergunta)
        st.chat_message("assistant").write(resposta)
if pergunta := st.chat_input("Sua dúvida sobre Crédito PJ..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))
