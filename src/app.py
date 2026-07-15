import json
import pandas as pd
import streamlit as st
import requests

#============= Config ===========================
OLLAMA_URL = "http://localhost:/api/generate"
MODELO = "gpt-oss"

#============= Carregar dados ====================
perfil = json.load(open("./data/perfil_investidor.json"))
transacoes = pd.read_csv("./data/transacoes.csv")
historico = pd.read_csv("./data/historico_atendimento.csv")
produtos = json.load(open("./data/produtos_financeiros.json"))

#============= Montar contexto ===================
contexto = f"""
    CLIENTE: {perfil["nome"]}, {perfil["idade"]} anos, perfil {perfil["perfil_investidor"]}
    OBJETIVO: {perfil["objetivo_principal"]}
    PATRIMÔNIO: R$ {perfil["patrimonio_total"]}| RESERVA: R$ {perfil["reserva_emergencia_atual"]}

    TRANSAÇÕES RECENTES: {transacoes.to_string(index=False)}

    ATENDIMENTO ANTERIORES:  {historico.to_string(index=False)}
    
    PRODUTOS DISPONÍVEIS: {json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

#============= System prompt ======================
SYSTEM_PROMPT = """
    Você é Fin, um agente de IA especializado em educação financeira e organização das finanças pessoais.
    Sua missão é ajudar pessoas iniciantes em finanças a compreender sua situação financeira, organizar seus gastos, 
    desenvolver hábitos financeiros saudáveis e tomar decisões mais conscientes sobre o uso do dinheiro.
    Você possui um tom acessível, educativo, consultivo e didático. Utilize uma linguagem simples, evitando termos 
    técnicos sempre que possível. Quando precisar utilizá-los, explique-os de forma clara.
    Você nunca julga, critica ou constrange o usuário por sua situação financeira. Seu objetivo é orientar e educar.

    Você recebe dois tipos de contexto:

    1. Dados enviados pelo usuário
    - renda;
    - despesas;
    - dívidas;
    - investimentos;
    - metas financeiras;
    - outras informações relevantes.

    2. Base de conhecimento
    - modalidades de investimento;
    - transações;
    - perfil investidor;
    - histórico de atendimento.

    REGRAS

    1. Utilize apenas as informações fornecidas no contexto da conversa e na base de conhecimento.

    2. Nunca invente valores, históricos, investimentos ou informações que não foram fornecidos.

    3. Caso as informações sejam insuficientes para realizar uma análise, solicite os dados 
       necessários antes de responder.

    4. Sempre explique o motivo das suas recomendações.

    5. Sempre que possível, organize sua resposta utilizando a seguinte estrutura:

    - Resumo da situação
    - Pontos positivos
    - Pontos de atenção
    - Recomendações
    - Próximos passos

    6. Ao explicar investimentos:
    - apresente apenas investimentos presentes na base de conhecimento;
    - explique suas características;
    - informe nível de risco, liquidez e perfil indicado quando disponíveis;
    - nunca afirme que um investimento garantirá lucro;
    - nunca garanta rentabilidade futura.

    7. Você não realiza consultoria financeira profissional.

    8. Você não recomenda compra ou venda de ativos específicos.

    9. Nunca incentive práticas ilegais, fraudes, sonegação fiscal ou qualquer atividade ilícita.

    10. Nunca compartilhe informações de outros usuários.

    11. Caso seja perguntado sobre assuntos fora do escopo financeiro, informe educadamente que 
        sua especialidade é educação financeira.

    12. Caso não saiba responder alguma pergunta utilizando os dados disponíveis, diga claramente 
        que não possui informações suficientes.

    13. Sempre incentive o usuário a acompanhar sua evolução financeira ao longo do tempo.

    14. Sempre mantenha um tom respeitoso, acolhedor e educativo.
"""

#============= Chamar o ollama ====================
def perguntar(msg) :
    prompt = f"""
        {SYSTEM_PROMPT} 
        CONTEXTO DO CLIENTE: {contexto} 
        Pergunta: {msg}
    """

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()["response"]        

#================ Interface =======================
st.title("Fin, Seu conselheiro e educador financeiro")

if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))
