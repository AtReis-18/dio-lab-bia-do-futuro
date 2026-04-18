# Base de Conhecimento

> [!TIP]
> **Prompt usado para esta etapa:**
> 
> Organize a base de conhecimento do agente "Edu" usando os 4 arquivos da pasta `data/` (em anexo). Explique pra que serve cada arquivo e monte um exemplo de contexto formatado que será enviado pro LLM. Preencha o template abaixo.
>
> [cole ou anexe o template `02-base-conhecimento.md` pra contexto]

## Dados Utilizados

| Arquivo | Formato | Para que serve no Edu? |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores, ou seja, dar continuidade ao atendimento de forma mais eficiente. |
| `perfil_investidor.json` | JSON | Personalizar as explicações sobre as dúvidas e necessidades de aprendizado do cliente. |
| `produtos_financeiros.json` | JSON | Conhecer os produtos disponíveis para que eles possam ser ensinados ao cliente. |
| `transacoes.csv` | CSV | Analisar o fluxo de caixa do cliente e usar essas informações de forma didática. |

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Existem duas possibilidades, injetar os dados diretamente no prompt (Ctrl + C, Ctrl + V) ou carregar os arquivos via código, como no exemplo abaixo:

```python
import pandas as pd
import json

perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Para simplificar, podemos simplesmente "injetar" os dados em nosso prompt, agarntindo que o Agente tenha o melhor contexto possível. Lembrando que, em soluções mais robustas, o ideal é que essas informaçoes sejam carregadas dinamicamente para que possamos ganhar flexibilidade.

```text
DADOS DO CLIENTE E PERFIL (data/perfil_investidor.json):
{
  "nome": "João Silva",
  "idade": 32,
  "profissao": "Empresário (Sócio-Proprietário)",
  "setor_atuacao": "Fabricação de embalagens de material plástico",
  "renda_mensal_prolabore": 35000.00,
  "perfil_investidor": "Moderado",
  "objetivo_principal": "Expansão de capacidade produtiva e sede própria",
  "patrimonio_total_estimado": 2500000.00,
  "reserva_emergencia_pessoal": 150000.00,
  "aceita_risco_financeiro": true,
  "metas": [
    {
      "meta": "Modernização do maquinário (Injeção Plástica)",
      "valor_necessario": 450000.00,
      "prazo": "2026-12"
    },
    {
      "meta": "Aquisição de Galpão para Sede Industrial Própria",
      "valor_necessario": 1500000.00,
      "prazo": "2029-12"
    }
  ],
  "historico_credito": "Bom pagador, utiliza linhas de capital de giro sazonalmente"
}

TRANSACOES DO CLIENTE (data/transacoes.csv):
estrutura_conta,planejado_jan_26,realizado_jan_26
1. ENTRADAS (Receita de Vendas),250000.00,235000.00
1.1. Vendas à Vista,100000.00,110000.00
1.2. Vendas à Prazo (Recebíveis),150000.00,125000.00
2. SAÍDAS (Custos e Despesas),-180000.00,-192000.00
2.1. Deduções (Impostos e Comissões),-30000.00,-28500.00
2.2. Fornecedores (Matéria-prima),-90000.00,-105000.00
2.3. Despesas Fixas (Aluguel/Folha),-60000.00,-58500.00
3. INVESTIMENTOS,-20000.00,-25000.00
3.1. Máquinas e Equipamentos,-20000.00,-25000.00
4. GERAÇÃO FINAL DE FLUXO DE CAIXA,50000.00,18000.00

HISTORICO DE ATENDIMENTO DO CLIENTE (data/historico_atendimento.csv):
data,canal,tema,resumo,resolvido
2025-11-10,chat,Capital de Giro,Cliente buscou entender a diferença entre Giro Parcelado e Rotativo para compra de matéria-prima,sim
2025-11-25,chat,FINAME/BNDES,Otto explicou as condições de carência para financiamento de nova injetora de plástico,sim
2025-12-05,telefone,Antecipação de Recebíveis,Dúvida sobre taxa de desconto para duplicatas de clientes do varejo (vendas a prazo),sim
2026-01-15,chat,Fluxo de Caixa,Análise do desvio entre planejado e realizado de Janeiro e impacto na liquidez,sim
2026-02-02,email,Crédito Imobiliário PJ,Primeira consulta sobre garantias necessárias para financiamento de galpão industrial (Home Equity vs Financiamento),sim

PRODUTOS DISPONIVEIS PARA ENSINO (data/produtos_financeiros.json):
[
  {
    "nome": "Capital de Giro (Simples/Tradicional)",
    "categoria": "Crédito para Fluxo de Caixa",
    "risco": "Moderado",
    "custo": "Taxas de juros pré ou pós-fixadas e IOF",
    "prazo": "Curto a médio prazo",
    "indicado_para": "Financiamento do ciclo operacional, compra de estoque, pagamento de salários e equilíbrio de caixa[cite: 3, 4]."
  },
  {
    "nome": "Capital de Giro Linha Governamental (BNDES Progeren)",
    "categoria": "Crédito Estruturado / Governamental",
    "risco": "Baixo a Moderado",
    "custo": "Custo Financeiro + Taxa do BNDES + Taxa do Agente Financeiro",
    "prazo": "Longo prazo",
    "indicado_para": "Apoio financeiro estrutural para aquisição de insumos, matérias-primas e recomposição de estoque[cite: 4, 5]."
  },
  {
    "nome": "Conta Garantida",
    "categoria": "Crédito Rotativo",
    "risco": "Moderado",
    "custo": "Juros sobre o saldo devedor e encargos contratuais",
    "prazo": "Imediato (disponibilidade permanente)",
    "indicado_para": "Uso conforme a necessidade da empresa para cobrir descasamentos temporários no caixa[cite: 3, 6]."
  },
  {
    "nome": "Cheque Flex PJ",
    "categoria": "Crédito Rotativo Emergencial",
    "risco": "Alto (pela falta de garantia real imediata)",
    "custo": "Juros cobrados apenas sobre o valor e o período utilizados",
    "prazo": "Curto prazo / Imediato",
    "indicado_para": "Necessidades emergenciais de caixa com renovação automática e simplicidade de uso[cite: 3, 6]."
  },
  {
    "nome": "Antecipação de Recebíveis (Cartões)",
    "categoria": "Antecipação de Ativos",
    "risco": "Baixo (garantido por vendas já realizadas)",
    "custo": "Taxa de desconto por período antecipado",
    "prazo": "Imediato",
    "indicado_para": "Transformar vendas parceladas a cartão (Visa/Master) em recursos à vista para o caixa[cite: 3]."
  },
  {
    "nome": "Antecipação de Duplicatas",
    "categoria": "Antecipação de Ativos",
    "risco": "Baixo a Moderado",
    "custo": "Taxa de desconto + Tarifas bancárias",
    "prazo": "Imediato",
    "indicado_para": "Empresas que possuem vendas faturadas com duplicatas registradas em cobrança simples[cite: 3]."
  },
  {
    "nome": "Cessão de Recebíveis ORPAGS",
    "categoria": "Antecipação de Ativos",
    "risco": "Baixo",
    "custo": "Taxa de desconto competitiva e isenção de IOF",
    "prazo": "Imediato",
    "indicado_para": "Receber à vista vendas parceladas nos cartões com otimização tributária (sem IOF)[cite: 3]."
  },
  {
    "nome": "Hot Money",
    "categoria": "Crédito de Curtíssimo Prazo",
    "risco": "Alto",
    "custo": "Taxas diárias elevadas",
    "prazo": "Curtíssimo prazo (até 29 dias)",
    "indicado_para": "Cobertura de falhas pontuais e imediatas de caixa por poucos dias[cite: 3, 6]."
  },
  {
    "nome": "Compror",
    "categoria": "Financiamento de Compras",
    "risco": "Moderado",
    "custo": "Juros negociados para pagamento ao banco",
    "prazo": "Curto a médio prazo",
    "indicado_para": "Financiar a compra de bens e serviços junto a fornecedores, permitindo negociar descontos à vista[cite: 3, 6]."
  },
  {
    "nome": "Vendor",
    "categoria": "Financiamento de Vendas",
    "risco": "Moderado",
    "custo": "Taxas de financiamento repassadas ao comprador ou assumidas pela empresa",
    "prazo": "Curto a médio prazo",
    "indicado_para": "Empresas que desejam vender a prazo para seus clientes, mas receber o valor à vista do banco[cite: 3, 6]."
  },{
    "nome": "BNDES Finame (Pós-fixado)",
    "categoria": "Financiamento de Bens (Repasse BNDES)",
    "risco": "Baixo a Moderado",
    "custo": "Custo Financeiro (TJLP/TLP) + Taxa do BNDES + Spread do Agente Financeiro",
    "prazo": "Até 72 meses para pagar, com carência de até 6 meses para a primeira parcela do principal",
    "indicado_para": "Aquisição de máquinas, equipamentos novos, caminhões, ônibus e tratores de fabricação nacional e cadastrados no CFI do BNDES."
  },
  {
    "nome": "CDC Veículos PJ",
    "categoria": "Financiamento de Veículos",
    "risco": "Moderado",
    "custo": "Taxas de juros prefixadas, IOF e Tarifas bancárias",
    "prazo": "Até 60 meses para pagar, com até 60 dias para o vencimento da primeira parcela",
    "indicado_para": "Aquisição ou troca de veículos leves e pesados, como automóveis, motos, caminhões e utilitários."
  },
  {
    "nome": "CDC Outros Bens",
    "categoria": "Financiamento de Bens Diversos",
    "risco": "Moderado",
    "custo": "Taxas de juros prefixadas e incidência de IOF",
    "prazo": "De 1 a 48 meses para pagar, com carência de até 60 dias para a primeira parcela",
    "indicado_para": "Financiamento de máquinas, equipamentos, eletrônicos, móveis de escritório, utensílios e equipamentos de informática."
  }
]
```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

O exemplo de contexto montado abaixo, se baiseia nos dados originais da base de conhecimento, mas os sintetiza deixando apenas as informações mais relevantes, otimizando assim o consumo de tokens. Entretanto, vale lembrar que mais importante do que economizar tokens, é ter todas as informações relevantes disponíveis em seu contexto.

```
DADOS DO CLIENTE:


RESUMO DE GASTOS:


PRODUTOS DISPONÍVEIS PARA EXPLICAR:

```
