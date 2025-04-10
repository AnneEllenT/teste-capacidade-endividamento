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

# Data de nascimento (formato DD-MM-AAAA)
data_nasc = st.date_input("Data de nascimento", max_value=date.today())
idade = relativedelta(date.today(), data_nasc).years

# Verificação de idade (opcional, se quiser validar se a pessoa é maior de idade ou não)
if idade < 18:
    st.warning("Você precisa ter pelo menos 18 anos para usar esta calculadora.")

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

# Ação do botão
if st.button("Calcular"):
    if idade < 18:
        st.error("Apenas pessoas maiores de idade podem usar a calculadora.")
    else:
        # Cálculo da renda líquida (Rendimento Bruto - Encargos obrigatórios)
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
        
        # Exibir o resultado
        st.success(f"Sua capacidade máxima de endividamento é R$ {capacidade_endividamento:.2f}")
