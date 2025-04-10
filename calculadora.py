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
outros_encargos = st.number_input("Outros Encargos e Seguros (€)", min_value=0.0, step=10.0)
coparticipante = st.checkbox("Tem coparticipante?")

if st.button("Calcular"):

    # Cálculo da idade e meses restantes
    hoje = datetime.today()
    idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
    meses_restantes = min((70 - idade) * 12, 480)

    # Cálculo do valor disponível para 1º plafond
    valor_disponivel_1p = ((rendimento_bruto * 14) / 24) - sams - valor_IRS - seguranca_social

    # Mensalidade do 1º plafond com o valor correto
    try:
        mensalidade_1p = round(
            valor_disponivel_1p / ((1 - math.pow(1 + taxa_mensal, -meses_restantes)) / taxa_mensal),
            2
        )
        valor_1p = mensalidade_1p * ((1 - math.pow(1 + taxa_mensal, -meses_restantes)) / taxa_mensal)
        valor_1p = min(valor_1p, plafond_1a)
        mensalidade_1p = round(
            valor_1p / ((1 - math.pow(1 + taxa_mensal, -meses_restantes)) / taxa_mensal),
            2
        )
    except:
        valor_1p = 0
        mensalidade_1p = 0

    # Cálculo 2º plafond (se houver capacidade extra)
    valor_2p = 0
    mensalidade_2p = 0

    if valor_1p < plafond_total:
        encargos_divididos = outros_encargos / 2 if coparticipante else outros_encargos

        # Valor restante do rendimento após pagar encargos e mensalidade do 1º plafond
        valor_disponivel_2p = rendimento_bruto - valor_IRS - seguranca_social - sams - encargos_divididos - mensalidade_1p

        if valor_disponivel_2p > 0:
            try:
                mensalidade_2p = round(
                    valor_disponivel_2p / ((1 - math.pow(1 + taxa_mensal, -meses_restantes)) / taxa_mensal),
                    2
                )
                valor_2p = mensalidade_2p * ((1 - math.pow(1 + taxa_mensal, -meses_restantes)) / taxa_mensal)
                valor_2p = min(valor_2p, plafond_total - valor_1p)
                mensalidade_2p = round(
                    valor_2p / ((1 - math.pow(1 + taxa_mensal, -meses_restantes)) / taxa_mensal),
                    2
                )
            except:
                valor_2p = 0
                mensalidade_2p = 0

    valor_total = valor_1p + valor_2p
    mensalidade_total = mensalidade_1p + mensalidade_2p

    # Resultados
    st.markdown("### ✅ Resultado")
    st.write(f"📅 Idade atual: **{idade} anos**")
    st.write(f"📆 Meses disponíveis até os 70 anos: **{meses_restantes} meses**")

    st.markdown("#### 🧮 1º Plafond")
    st.write(f"💰 Valor disponível (1º plafond): **€ {formatar_moeda(valor_1p)}**")
    st.write(f"💳 Prestação estimada (1º plafond): **€ {formatar_moeda(mensalidade_1p)}**")

    if valor_2p > 0:
        st.markdown("#### ➕ 2º Plafond")
        st.write
