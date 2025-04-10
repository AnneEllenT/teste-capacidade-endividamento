import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta

# Layout inicial
st.set_page_config(page_title="Calculadora de Endividamento", layout="centered")
st.title("Calculadora de Capacidade de Endividamento")

st.markdown("""
<style>
    .stButton>button {
        background-color: #004080;
        color: white;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Formulário
st.subheader("Dados Pessoais")

# Dados financeiros
rendimento_bruto = st.number_input("Rendimento bruto (R$)", min_value=0.0, step=100.0)
valor_irs = st.number_input("Valor de IRS (R$)", min_value=0.0, step=100.0)
seguranca_social = st.number_input("Segurança Social (R$)", min_value=0.0, step=100.0)
seguro_saude = st.number_input("Seguro de Saúde (R$)", min_value=0.0, step=100.0)
outros_encargos = st.number_input("Outros Encargos e Seguros (R$)", min_value=0.0, step=100.0)

# Caixa de seleção para Tipo de Imóvel (Obrigatório)
tipo_imovel = st.selectbox("Selecione o tipo de imóvel", ["1ª Habitação", "2ª Habitação"])

# Coparticipante (checkbox)
coparticipante = st.checkbox("Há coparticipante no cálculo?", value=False)

# Taxa de juros mensal (por exemplo, 0.5% ao mês)
taxa_juros_mensal = st.number_input("Taxa de juros mensal (%)", min_value=0.0, max_value=100.0, step=0.1) / 100

# Valor disponível para financiamento
valor_disponivel = st.number_input("Valor disponível para financiamento (R$)", min_value=0.0, step=1000.0)

# Data de nascimento
data_nasc = st.date_input("Data de nascimento", max_value=date.today())

# Cálculo do número de meses até completar 70 anos (limite de 480 meses)
idade_atual = relativedelta(date.today(), data_nasc).years
idade_70_anos = 70 - idade_atual
meses_restantes = idade_70_anos * 12  # Calcula o número de meses restantes até completar 70 anos
meses_restantes = min(meses_restantes, 480)  # Limita a 480 meses

# Exibir meses restantes para o empréstimo
st.write(f"Você tem no máximo {meses_restantes} meses disponíveis para o empréstimo.")

# Ação do botão
if st.button("Calcular"):
    # Cálculo da renda líquida
    renda_liquida = rendimento_bruto - (valor_irs + seguranca_social + seguro_saude + outros_encargos)
    
    # Se houver coparticipante, soma o rendimento dele
    if coparticipante:
        rendimento_bruto_coparticipante = st.number_input("Rendimento Bruto Coparticipante (R$)", min_value=0.0, step=100.0)
        renda_liquida += rendimento_bruto_coparticipante - (valor_irs + seguranca_social + seguro_saude + outros_encargos)
    
    # Cálculo de capacidade de endividamento
    if tipo_imovel == "1ª Habitação":
        capacidade_endividamento = renda_liquida * 0.30  # 30% da renda líquida
    else:
        capacidade_endividamento = renda_liquida * 0.20  # 20% da renda líquida

    # Cálculo da mensalidade com a fórmula
    mensalidade = round(valor_disponivel / ((1 - (1 + taxa_juros_mensal) ** (-meses_restantes)) / taxa_juros_mensal), 2)

    # Exibição do valor máximo com base na fórmula adicional
    valor_maximo = min(valor_disponivel * (1 - (1 + taxa_juros_mensal) ** (-meses_restantes)) / taxa_juros_mensal, capacidade_endividamento)

    # Resultados finais
    st.success(f"Sua capacidade máxima de endividamento é R$ {capacidade_endividamento:.2f}")
    st.success(f"O valor máximo de mensalidade que você pode pagar é R$ {mensalidade:.2f}")
    st.success(f"O valor máximo de empréstimo que você pode solicitar é R$ {valor_maximo:.2f}")
