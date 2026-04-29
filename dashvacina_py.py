import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="DashVacina", layout="wide")
st.title("DASHVAICNA: Dados de Vacinação")

# Lógica de carregamento (Igual ao Código 1)
df = pd.read_csv('vacinacao.csv')

# --- LÓGICA DE LIMPEZA (Inspirada no Código 1) ---

# 1. Padronização (Como o str.replace do Código 1, mas para texto)
df['location'] = df['location'].str.upper().str.strip()

# 2. Filtragem de Colunas e Linhas (Como o iloc e dropna do Código 1)
paises_alvo = ['BRAZIL', 'INDIA', 'UNITED STATES']
df_paises = df[df['location'].isin(paises_alvo)].copy()

# Convertemos a data (Lógica de conversão de tipos)
df_paises['date'] = pd.to_datetime(df_paises['date'])

# --- GRÁFICO DE PIZZA (CORREÇÃO) ---

st.subheader("Distribuição de Pessoas Totalmente Vacinadas")

# Criamos um DataFrame específico para a pizza limpando valores nulos
# Isso é IDÊNTICO ao dropna(subset=['ANO']) que você usou no código 1
df_pizza_limpo = df_paises.dropna(subset=['people_fully_vaccinated'])

# Pegamos o valor máximo de cada país após a limpeza
df_pizza_total = df_pizza_limpo.groupby('location')['people_fully_vaccinated'].max().reset_index()

# Gerar o gráfico com os 3 países
fig_pizza = px.pie(
    df_pizza_total,
    values='people_fully_vaccinated',
    names='location',
    title='Total de Vacinados por País (BRA, IND, USA)'
)
st.plotly_chart(fig_pizza, use_container_width=True)

# --- OUTROS GRÁFICOS ---
st.subheader("Vacinação Diária")
fig_hist = px.histogram(df_paises, x="date", y="daily_vaccinations", color="location", barmode="group")
st.plotly_chart(fig_hist, use_container_width=True)

