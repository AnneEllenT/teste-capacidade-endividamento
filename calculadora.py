import streamlit as st
from datetime import date

# Layout inicial
st.set_page_config(page_title="Calculadora de Endividamento", layout="centered")
st.title("Teste Capacidade de Endividamento")

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
nome = st.text_input("Nome completo")
email = st.text_input("E-mail corporativo")
data_nasc = st.date_input("Data de nascimento")

st.subheader("Dados Financeiros")
renda_mensal = st.number_input("Renda mensal (R$)", min_value=0.0, step=100.0)
encargos_mensais = st.number_input("Encargos mensais (R$)", min_value=0.0, step=100.0)

# Ação
if st.button("Calcular"):
    idade = date.today().year - data_nasc.year
    renda_liquida = renda_mensal - encargos_mensais
    capacidade = renda_liquida * 0.3  # 30% da renda líquida

    st.success(f"{nome}, você tem {idade} anos.")
    st.info(f"Sua renda líquida atual é de R$ {renda_liquida:.2f}.")
    st.success(f"Você pode comprometer até R$ {capacidade:.2f} com dívidas.")
