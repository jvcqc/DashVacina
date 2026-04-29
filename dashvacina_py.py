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
df_filtrado = df[df['location'].isin(paises_alvo)].copy()

# 3. LIMPEZA (Igual à função clean_currency do Código 1, mas para datas)
df_filtrado['date'] = pd.to_datetime(df_filtrado['date'])

# 4. PREPARAÇÃO PARA OS GRÁFICOS
# Agora o pivot é instantâneo porque só tem 3 países
df_pivot_serie = df_filtrado.pivot_table(
    index='date', 
    columns='location', 
    values='total_vaccinations', 
    aggfunc='max'
)

# 5. VISUALIZAÇÃO
st.subheader("Total de Vacinações por Data")
st.line_chart(df_pivot_serie)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Vacinação Diária")
    fig_hist = px.histogram(df_filtrado, x="date", y="daily_vaccinations", 
                            color="location", barmode="group")
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    st.subheader("Distribuição Total")
    df_pizza = df_filtrado.groupby('location')['people_fully_vaccinated'].max().reset_index()
    fig_pizza = px.pie(df_pizza, values='people_fully_vaccinated', names='location')
    st.plotly_chart(fig_pizza, use_container_width=True)
