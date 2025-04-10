import streamlit as st
from datetime import datetime
import math
import locale

# Define a função de formatação
def formatar_moeda(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Taxa de juros anual e mensal efetiva (65% de 2.65%)
taxa_juros_anual = 2.65 / 100
taxa_efetiva = taxa_juros_anual * 0.65
taxa_mensal = taxa_efetiva / 12

# Plafonds
plafond_1a_habitacao = 237540
plafond_2a_habitacao = 237540
plafond_total = plafond_1a_habitacao + plafond_2a_habitacao

st.title("🧮 Calculadora de Capacidade de Endividamento")

# Tipo de habitação
tipo_habitacao = st.selectbox("Para que pretende a simulação?", ["1ª habitação", "2ª habitação"])

# Entrada de dados
data_nascimento = st.date_input("Data de nascimento (DD-MM-AAAA)", format="DD-MM-YYYY", min_value=datetime(1900, 1, 1), max_value=datetime(2024, 12, 31))
rendimento_bruto = st.number_input("Rendimento Bruto (€)", min_value=0.0, step=100.0)
valor_IRS = st.number_input("Valor de IRS (€)", min_value=0.0, step=10.0)
seguranca_social = st.number_input("Segurança Social (€)", min_value=0.0, step=10.0)
sams = st.number_input("Seg. Saúde (SAMS, etc.) (€)", min_value=0.0, step=10.0)
outros_encargos = st.number_input("Outros Encargos e Seguros (€)", min_value=0.0, step=10.0)
coparticipante = st.checkbox("Tem coparticipante?")

if st.button("Calcular"):
    # Cálculo dos meses disponíveis
    hoje = datetime.today()
    idade_atual = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
    meses_restantes = min((70 - idade_atual) * 12, 480)

    # Valor disponível
    valor_disponivel = ((rendimento_bruto * 14) / 24) - sams - valor_IRS - seguranca_social

    # Ajuste por coparticipante
    encargos_totais = sams + valor_IRS + seguranca_social + outros_encargos
    if coparticipante:
        encargos_totais -= (outros_encargos / 2)

    # Mensalidade máxima
    try:
        mensalidade = round(
            valor_disponivel / ((1 - math.pow(1 + taxa_mensal, -meses_restantes)) / taxa_mensal),
            2
        )
    except ZeroDivisionError:
        mensalidade = 0

    # Cálculo de valores com regras de plafond
    valor_1a_habitacao = min((rendimento_bruto * 14) / 24, plafond_1a_habitacao)
    restante_disponivel = capacidade_restante = valor_disponivel - mensalidade if tipo_habitacao == "1ª habitação" else valor_disponivel
    valor_2a_habitacao = min(restante_disponivel, plafond_2a_habitacao)

    # Valor máximo final
    if tipo_habitacao == "1ª habitação":
        valor_total = valor_1a_habitacao
    else:
        valor_total = valor_2a_habitacao

    valor_total = min(valor_total, plafond_total)

    st.markdown("### 💡 Resultado")
    st.write(f"Idade atual: {idade_atual} anos")
    st.write(f"Meses disponíveis até os 70 anos: {meses_restantes} meses")
    st.write(f"A sua mensalidade será de € {formatar_moeda(mensalidade)}")
    st.write(f"Valor máximo de financiamento: € {formatar_moeda(valor_total)}")
