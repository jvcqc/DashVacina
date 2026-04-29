import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="DashVacina", layout="wide")

st.title("DASHVACINA: Dados de Vacinação (Lógica Otimizada)")

# 1. CARREGAMENTO
df = pd.read_csv('vacinacao.csv')

# 2. FILTRAGEM PRECOCE (A lógica do Código 1: trabalhar só com o necessário)
# Filtramos os países ANTES de qualquer conversão ou pivot
paises_alvo = ['BRAZIL', 'INDIA', 'UNITED STATES']
df['location'] = df['location'].str.upper()

# 3. Criamos um DataFrame que contém APENAS esses 3 países
df_paises_selecionados = df[df['location'].isin(paises_alvo)]

# 4. LIMPEZA (Igual à função clean_currency do Código 1, mas para datas)
df_filtrado['date'] = pd.to_datetime(df_filtrado['date'])

# 5. PREPARAÇÃO PARA OS GRÁFICOS
# Agora o pivot é instantâneo porque só tem 3 países
df_pivot_serie = df_filtrado.pivot_table(
    index='date', 
    columns='location', 
    values='total_vaccinations', 
    aggfunc='max'
)

# 6. VISUALIZAÇÃO
st.subheader("Total de Vacinações por Data")
st.line_chart(df_pivot_serie)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Vacinação Diária")
    fig_hist = px.histogram(df_filtrado, x="date", y="daily_vaccinations", 
                            color="location", barmode="group")
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    st.subheader("Distribuição de Pessoas Totalmente Vacinadas")
    fig_pizza = px.pie(
    df_pizza_total, 
    values='people_fully_vaccinated', 
    names='location', 
    title='Total de Vacinados por País (BRA, IND, USA)',
    color_discrete_sequence=px.colors.qualitative.Pastel # Opcional: cores diferentes
)

st.plotly_chart(fig_pizza, use_container_width=True)

