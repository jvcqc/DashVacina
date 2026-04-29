import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="DashVacina", layout="wide")
st.title("DASHVACINA: Dados de Vacinação")

# 1. CARREGAMENTO E LIMPEZA INICIAL (Lógica do Código 1)
df = pd.read_csv('vacinacao.csv')

# Padronização para garantir que o filtro funcione
df['location'] = df['location'].str.strip().str.upper()
paises_alvo = ['BRAZIL', 'INDIA', 'UNITED STATES']

# Filtramos apenas os países desejados
df_filtrado = df[df['location'].isin(paises_alvo)].copy()
df_filtrado['date'] = pd.to_datetime(df_filtrado['date'])

# --- A. TOTAL DE VACINAÇÕES POR DATA E PAÍSES (GRÁFICO DE SÉRIE) ---
st.subheader("A. Total de Vacinações por Data e Países")
# Pivotamos para ter as datas no índice e países como colunas
df_pivot_serie = df_filtrado.pivot_table(index='date', columns='location', values='total_vaccinations', aggfunc='max')
st.line_chart(df_pivot_serie)

# Criando colunas para os gráficos B e C ficarem lado a lado (como no Código 1)
col1, col2 = st.columns(2)

with col1:
    # --- B. PESSOAS DIARIAMENTE VACINADAS (HISTOGRAMA) ---
    st.subheader("B. Vacinação Diária (BRA, IND, USA)")
    fig_hist = px.histogram(
        df_filtrado,
        x="date",
        y="daily_vaccinations",
        color="location",
        barmode="group",
        title="Vacinação Diária"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    # --- C. PESSOAS TOTALMENTE VACINADAS (PIZZA) ---
    st.subheader("C. Pessoas Totalmente Vacinadas")
    
    # Limpeza de nulos específica para garantir que Brasil e Índia apareçam
    df_pizza_data = df_filtrado.dropna(subset=['people_fully_vaccinated'])
    df_pizza_final = df_pizza_data.groupby('location')['people_fully_vaccinated'].max().reset_index()
    
    fig_pizza = px.pie(
        df_pizza_final,
        values='people_fully_vaccinated',
        names='location',
        title='Distribuição Total de Vacinados'
    )
    st.plotly_chart(fig_pizza, use_container_width=True)
