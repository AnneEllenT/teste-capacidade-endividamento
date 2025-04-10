import streamlit as st
from datetime import datetime
import math

# Função para formatar valores com vírgula e duas casas decimais
def formatar_moeda(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Taxa de juro: 2.65% * 65%
taxa_anual = 2.65 / 100
taxa_efetiva = taxa_anual * 0.65
taxa_mensal = taxa_efetiva / 12

# Plafonds
plafond_1a = 237_540.00
plafond_total = 475_080.00

st.set_page_config(page_title="Capacidade de Endividamento", layout="centered")
st.title("🏡 Calculadora de Capacidade de Endividamento")

# Seleção de tipo de habitação
tipo_habitacao = st.selectbox("Para que pretende a simulação?", ["1ª habitação", "2ª habitação"])

# Entradas do usuário
data_nascimento = st.date_input("Data de nascimento (DD-MM-AAAA)", format="DD-MM-YYYY", min_value=datetime(1900, 1, 1))
rendimento_bruto = st.number_input("Rendimento Bruto (€)", min_value=0.0, step=100.0)
valor_IRS = st.number_input("Valor de IRS (€)", min_value=0.0, step=10.0)
seguranca_social = st.number_input("Segurança Social (€)", min_value=0.0, step=10.0)
sams = st.number_input("Seg. Saúde (SAMS, etc.) (€)", min_value=0.0, step=10.0)
out
