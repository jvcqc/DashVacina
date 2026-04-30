import pandas as pd
import plotly.express as px
import streamlit as st

# Carregamento de dados (Caminho relativo para funcionar no Cloud)
df = pd.read_csv('vacinacao.csv')

# Tratamento de Dados
df['date'] = pd.to_datetime(df['date'])
df['location'] = df['location'].str.upper()

# Preparação dos DataFrames
df_serie_temporal = df[['date', 'location', 'total_vaccinations']].dropna()

paises_alvo = ['BRAZIL', 'INDIA', 'UNITED STATES']
df_diario_paises = df[df['location'].isin(paises_alvo)]

df_pizza_total = df_diario_paises.groupby('location')['people_fully_vaccinated'].max().reset_index()

# --- GRÁFICO 1: LINHA (NATIVO STREAMLIT) ---
st.subheader("Total de Vacinações por Data e Países")
df_pivot_serie = df_serie_temporal.pivot(index='date', columns='location', values='total_vaccinations')
st.line_chart(df_pivot_serie)

# --- GRÁFICO 2: HISTOGRAMA (PLOTLY) ---
fig_hist = px.histogram(df_diario_paises,
                        x="date",
                        y="daily_vaccinations",
                        color="location",
                        barmode="group",
                        title="Vacinação Diária (BRA, IND, USA)")

fig_hist.update_layout(xaxis_title='Data', yaxis_title='Vacinações Diárias')
st.plotly_chart(fig_hist) # Garante a exibição no Streamlit

# --- GRÁFICO 3: PIZZA (PLOTLY) ---
fig_pizza = px.pie(df_pizza_total,
                   values='people_fully_vaccinated',
                   names='location',
                   title='Total de Vacinados por País')

st.plotly_chart(fig_pizza)
