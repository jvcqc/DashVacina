import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="DashVacina",
    layout="wide")

st.title("DASHVACINA: Um Dashboard sobre os Dados de Vacinação por Países e Datas")

# 1. CARREGAMENTO E PADRONIZAÇÃO (Lógica do Código 1: Limpar antes de usar)
df = pd.read_csv('vacinacao.csv')
df['location'] = df['location'].str.strip().str.upper() # Remove espaços e padroniza
df['date'] = pd.to_datetime(df['date'])

# 2. FILTRAGEM (Lógica do Código 1: Selecionar apenas o necessário)
paises_alvo = ['BRAZIL', 'INDIA', 'UNITED STATES']
df_diario_paises = df[df['location'].isin(paises_alvo)].copy()

# --- A. TOTAL DE VACINAÇÕES POR DATA (SÉRIE TEMPORAL) ---
st.subheader("Total de Vacinações por Data e Países")
df_pivot_serie = df_diario_paises.pivot_table(index='date', columns='location', values='total_vaccinations', aggfunc='max')
st.line_chart(df_pivot_serie)

# Criando colunas para os gráficos B e C (Igual ao layout do Código 1)
col1, col2 = st.columns(2)

with col1:
    # --- B. VACINAÇÃO DIÁRIA (HISTOGRAMA) ---
    st.subheader("Pessoas Diariamente Vacinadas (BRA, IND, USA)")
    fig_hist = px.histogram(df_diario_paises,
                            x="date",
                            y="daily_vaccinations",
                            color="location",
                            barmode="group",
                            title="Vacinação Diária")
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    # --- C. PESSOAS TOTALMENTE VACINADAS (PIZZA) - TRECHO CORRIGIDO ---
    st.subheader("Distribuição de Pessoas Totalmente Vacinadas")
    
    # LÓGICA DE LIMPEZA: Removemos as linhas onde a vacinação está vazia (NaN)
    # Isso é idêntico ao df.dropna(subset=['ANO']) do seu código da UFERSA
    df_pizza_limpo = df_diario_paises.dropna(subset=['people_fully_vaccinated'])
    
    # Agora o agrupamento conseguirá achar o valor máximo para os 3 países
    df_pizza_total = df_pizza_limpo.groupby('location')['people_fully_vaccinated'].max().reset_index()

    fig_pizza = px.pie(df_pizza_total,
                        values='people_fully_vaccinated',
                        names='location',
                        title='Total de Vacinados por País')
    st.plotly_chart(fig_pizza, use_container_width=True)
