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
outros_encargos = st.number_input("Outros Encargos e Seguros (€)", min_value=0.0, step=100.0)

# Caixa de seleção para Tipo de Imóvel (Obrigatório)
tipo_imovel = st.selectbox("Selecione o tipo de imóvel", ["1ª Habitação", "2ª Habitação"])

# Coparticipante (checkbox)
coparticipante = st.checkbox("Há coparticipante no cálculo?", value=False)

# Taxa de juros original (por exemplo, 2,65% ao ano)
taxa_juros_original_ano = 2.65 / 100  # 2,65% convertendo para decimal

# Aplicando 65% da taxa de juros original
taxa_juros_efetiva_ano = taxa_juros_original_ano * 0.65

# Convertendo para taxa mensal
taxa_juros_mensal = taxa_juros_efetiva_ano / 12  # taxa anual dividida por 12 meses

# Valor disponível para financiamento
valor_disponivel = st.number_input("Valor disponível para financiamento (€)", min_value=0.0, step=1000.0)

# Data de nascimento
data_nasc = st.date_input("Data de nascimento", max_value=date.today())

# Cálculo do número de meses até completar 70 anos (limite de 480 meses)
idade_atual = relativedelta(date.today(), data_nasc).years
idade_70_anos = 70 - idade_atual
meses_restantes = idade_70_anos * 12  # Calcula o número de meses restantes até completar 70 anos
meses_restantes = min(meses_restantes, 480)  # Limita a 480 meses

# Exibir meses restantes para o empréstimo
st.write(f"Você tem no máximo {meses_restantes} meses disponíveis para o empréstimo.")

# Cálculo da renda líquida (Rendimento Bruto - Encargos obrigatórios)
renda_liquida = rendimento_bruto - (valor_irs + seguranca_social + seguro_saude + outros_encargos)

# Se houver coparticipante, não somamos o rendimento, apenas dividimos as mensalidades
if coparticipante:
    # Dividimos por 2 o valor das mensalidades
    st.write("Como há coparticipante, o valor das mensalidades será dividido por 2.")
    capacidade_endividamento = (renda_liquida * 0.30) / 2 if tipo_imovel == "1ª Habitação" else (renda_liquida * 0.20) / 2
else:
    # Se não houver coparticipante, calculamos a capacidade de endividamento normalmente
    if tipo_imovel == "1ª Habitação":
        capacidade_endividamento = renda_liquida * 0.30  # 30% da renda líquida
    else:
        capacidade_endividamento = renda_liquida * 0.20  # 20% da renda líquida

# Exibir a capacidade de endividamento formatado
st.write(f"Sua capacidade máxima de endividamento é € {formatar_moeda(capacidade_endividamento)}")

# Cálculo da mensalidade com a fórmula de amortização
mensalidade = round(valor_disponivel / ((1 - (1 + taxa_juros_mensal) ** (-meses_restantes)) / taxa_juros_mensal), 2)

# Se houver coparticipante, a mensalidade é dividida por 2
if coparticipante:
    mensalidade /= 2

# Exibir a mensalidade formatada
st.write(f"A sua mensalidade será de € {formatar_moeda(mensalidade)}")

# Cálculo do valor máximo de empréstimo com base na capacidade de endividamento
valor_maximo = capacidade_endividamento * ((1 - (1 + taxa_juros_mensal) ** (-meses_restantes)) / taxa_juros_mensal)

# Se houver coparticipante, o valor máximo de empréstimo também será ajustado
if coparticipante:
    valor_maximo /= 2

# Exibir o valor máximo do empréstimo calculado
st.write(f"O valor máximo de empréstimo que você pode solicitar é € {formatar_moeda(valor_maximo)}")

# Exibir a taxa de juros mensal efetiva
st.write(f"A taxa de juros mensal efetiva aplicada é de {round(taxa_juros_mensal * 100, 4)}%")
