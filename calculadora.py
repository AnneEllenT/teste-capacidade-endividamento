import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta

# Função para formatar números com ponto e vírgula e 2 casas decimais
def formatar_moeda(valor):
    return f"{valor:,.2f}".replace(",", ";").replace(".", ",")  # Usa f-string para formatação

# Layout inicial
st.set_page_config(page_title="Calculadora de Endividamento", layout="centered")
st.title("Calculadora de Capacidade de Endividamento")

# Formulário para dados pessoais e financeiros
st.subheader("Dados Pessoais")

# Dados financeiros
rendimento_bruto = st.number_input("Rendimento bruto (€)", min_value=0.0, step=100.0)
valor_irs = st.number_input("Valor de IRS (€)", min_value=0.0, step=100.0)
seguranca_social = st.number_input("Segurança Social (€)", min_value=0.0, step=100.0)
seguro_saude = st.number_input("Seguro de Saúde (€)", min_value=0.0, step=100.0)
outros_encargos = st.number_input("Outros Encargos e Seguros (€)", min_value=0.0, step_
