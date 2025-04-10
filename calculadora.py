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

# Plafond
plafond_1a_habitacao = 237_540.00

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

    # Cálculo do valor disponível (1/24 avos com encargos)
    valor_disponivel = ((rendimento_bruto * 14) / 24) - sams - valor_IRS - seguranca_social

    # Ajustes se houver coparticipante (dividimos os encargos relacionados à habitação)
    encargos_divididos = outros_encargos / 2 if coparticipante else outros_encargos

    # Cálculo da mensalidade com base no valor disponível
    try:
        mensalidade_maxima = round(
            valor_disponivel / ((1 - math.pow(1 + taxa_mensal, -meses_restantes)) / taxa_mensal),
            2
        )

        # Agora calculamos o valor de financiamento possível com essa mensalidade
        valor_possivel = mensalidade_maxima * ((1 - math.pow(1 + taxa_mensal, -meses_restantes)) / taxa_mensal)

        # Aplicamos o limite do plafond
        valor_financiamento = min(valor_possivel, plafond_1a_habitacao)

        # Se limitou, recalculamos a nova mensalidade com o valor permitido
        mensalidade_corrigida = round(
            valor_financiamento / ((1 - math.pow(1 + taxa_mensal, -meses_restantes)) / taxa_mensal),
            2
        )

    except:
        mensalidade_maxima = 0
        valor_financiamento = 0
        mensalidade_corrigida = 0

    # Resultados
    st.markdown("### ✅ Resultado")
    st.write(f"📅 Idade atual: **{idade} anos**")
    st.write(f"📆 Meses disponíveis até os 70 anos: **{meses_restantes} meses**")
    st.write(f"💰 Valor disponível para financiamento: **€ {formatar_moeda(valor_disponivel)}**")
    st.write(f"🏦 Valor máximo de financiamento (com base no plafond): **€ {formatar_moeda(valor_financiamento)}**")
    st.write(f"💳 Prestação estimada: **€ {formatar_moeda(mensalidade_corrigida)}**")
