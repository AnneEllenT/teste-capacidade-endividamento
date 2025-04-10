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
plafond_1a = 237_540.00  # 1º plafond de 1ª habitação
plafond_total = 475_080.00  # Plafond total (soma dos 2 plafonds)

st.set_page_config(page_title="Capacidade de Endividamento", layout="centered")
st.title("🏡 Calculadora de Capacidade de Endividamento")

# Seleção de tipo de habitação
tipo_habitacao = st.selectbox("Para que pretende a simulação?", ["1ª habitação", "2ª habitação"])

# Entradas do usuário
data_nascimento = st.date_input("Data de nascimento (DD-MM-AAAA)", format="DD-MM-YYYY", min_value=datetime(1900, 1, 1))
rendimento_bruto = st.number_input("Rendimento Bruto (€)", min_value=0.0, step=100.0)

# Inputs para encargos
IRS = st.number_input("IRS (€)", min_value=0.0, step=10.0)
seguranca_social = st.number_input("Segurança Social (€)", min_value=0.0, step=10.0)
seguro_saude = st.number_input("Seguro de Saúde (€)", min_value=0.0, step=10.0)

# Botão para calcular
if st.button("Calcular"):

    # Cálculo da idade e meses restantes
    hoje = datetime.today()
    idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
    meses_restantes = min((70 - idade) * 12, 480)  # Limitar a 480 meses (40 anos)

    # Cálculo do valor disponível para 1º plafond (sem deduzir encargos)
    valor_disponivel_1p = (rendimento_bruto * 14) / 24

    # Limitar o valor disponível para o 1º plafond a 237.540€
    valor_1p = min(valor_disponivel_1p, plafond_1a)

    # Cálculo do valor do 2º plafond (caso necessário)
    valor_necessario_2p = max(0, rendimento_bruto - IRS - seguranca_social - seguro_saude)
    valor_2p = max(0, valor_necessario_2p)

    # Calcular o total disponível para financiamento
    total_financiamento = valor_1p + valor_2p

    # Cálculo da mensalidade do 1º plafond
    try:
        mensalidade_1p = round(
            valor_1p / ((1 - math.pow(1 + taxa_mensal, -meses_restantes)) / taxa_mensal),
            2
        )
    except:
        valor_1p = 0
        mensalidade_1p = 0

    # Exibindo os resultados
    st.markdown("### ✅ Resultado")
    st.write(f"📅 **Idade atual**: **{idade} anos**")
    st.write(f"📆 **Meses disponíveis até os 70 anos**: **{meses_restantes} meses**")

    st.markdown("#### 🧮 **1º Plafond**")
    st.write(f"💰 **Valor disponível (1º plafond)**: **€ {formatar_moeda(valor_1p)}**")
    st.write(f"💳 **Prestação estimada (1º plafond)**: **€ {formatar_moeda(mensalidade_1p)}**")

    st.markdown("#### ➕ **2º Plafond**")
    st.write(f"💰 **Valor disponível (2º plafond)**: **€ {formatar_moeda(valor_2p)}**")

    st.markdown("### 🏦 **Valor total de financiamento**")
    st.write(f"💰 **Valor total de financiamento**: **€ {formatar_moeda(total_financiamento)}**")
