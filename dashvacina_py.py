import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="DashVacina",
    layout="wide")

st.title("DASHVAICNA: Um Dashboard sobre os Dados de Vacinacao por Paises e Datas")

df = pd.read_csv('vacinacao.csv')

df['date'] = pd.to_datetime(df['date'])

df['location'] = df['location'].str.upper()

df_serie_temporal = df[['date', 'location', 'total_vaccinations']].dropna()

paises_alvo = ['BRAZIL', 'INDIA', 'UNITED STATES']
df_diario_paises = df[df['location'].isin(paises_alvo)]

df_pizza_total = df_diario_paises.groupby('location')['people_fully_vaccinated'].max().reset_index()

st.subheader("Total de Vacinações por Data e Países")

# Mova o filtro para antes do pivot
df_serie_temporal = df_serie_temporal[df_serie_temporal['location'].isin(paises_alvo)]
df_pivot_serie = df_serie_temporal.pivot(index='date', columns='location', values='total_vaccinations')

st.line_chart(df_pivot_serie)

import plotly.express as px

st.subheader("Pessoas Diariamente Vacinadas (BRA, IND, USA)")

fig_hist = px.histogram(df_diario_paises,
                        x="date",
                        y="daily_vaccinations",
                        color="location",
                        barmode="group",
                        title="Vacinação Diária")
st.plotly_chart(fig_hist)

st.subheader("Distribuição de Pessoas Totalmente Vacinadas")
fig_pizza = px.pie(df_pizza_total,
                   values='people_fully_vaccinated',
                   names='location',
                   title='Total de Vacinados por País')
st.plotly_chart(fig_pizza)
