import pandas as pd
import plotly.express as px
import streamlit as st

# 1. CONFIGURAÇÃO DA PÁGINA (Idêntica ao Código 1)
st.set_page_config(
    page_title="DashVacina",
    layout="wide")

st.title("DASHVACINA: Um Dashboard sobre os Dados de Vacinação")

# 2. CARREGAMENTO DOS DADOS
df = pd.read_csv('vacinacao.csv')

# 3. LIMPEZA E PADRONIZAÇÃO (Lógica do Código 1: Limpar antes de processar)
# Removemos espaços em branco e transformamos em MAIÚSCULO
df['location'] = df['location'].str.strip().str.upper()

# Filtramos apenas os países alvo (BRAZIL, INDIA, UNITED STATES)
paises_alvo = ['BRAZIL', 'INDIA', 'UNITED STATES']
df_filtrado = df[df['location'].isin(paises_alvo)].copy()

# --- A GRANDE CORREÇÃO: Conversão de tipos (Como você fez no Código 1) ---
# Na sua planilha, existem textos "none" que impedem o cálculo.
# O pd.to_numeric com errors='coerce' transforma esses textos em valores vazios (NaN)
df_filtrado['people_fully_vaccinated'] = pd.to_numeric(df_filtrado['people_fully_vaccinated'], errors='coerce')
df_filtrado['total_vaccinations'] = pd.to_numeric(df_filtrado['total_vaccinations'], errors='coerce')
df_filtrado['daily_vaccinations'] = pd.to_numeric(df_filtrado['daily_vaccinations'], errors='coerce')

# Convertemos a data para o formato correto
df_filtrado['date'] = pd.to_datetime(df_filtrado['date'])


# --- ITEM A: TOTAL DE VACINAÇÕES POR DATA E PAÍSES (Gráfico de Série) ---
st.subheader("A. Total de Vacinações por Data e Países")
# Criamos uma tabela dinâmica (pivot) para alimentar o gráfico de linhas
df_pivot_serie = df_filtrado.pivot_table(index='date', columns='location', values='total_vaccinations', aggfunc='max')
st.line_chart(df_pivot_serie)


# ORGANIZAÇÃO EM COLUNAS (Lógica de layout do Código 1)
col1, col2 = st.columns(2)

with col1:
    # --- ITEM B: PESSOAS DIARIAMENTE VACINADAS (Histograma) ---
    st.subheader("B. Vacinação Diária (BRA, IND, USA)")
    fig_hist = px.histogram(
        df_filtrado,
        x="date",
        y="daily_vaccinations",
        color="location",
        barmode="group",
        title="Vacinação Diária por País"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    # --- ITEM C: PESSOAS TOTALMENTE VACINADAS (Gráfico de Pizza) ---
    st.subheader("C. Distribuição de Pessoas Totalmente Vacinadas")
    
    # Removemos as linhas vazias (que antes eram "none") para o cálculo funcionar
    # Isso é idêntico ao df.dropna(subset=['ANO']) que você usou na UFERSA
    df_pizza_limpo = df_filtrado.dropna(subset=['people_fully_vaccinated'])
    
    # Agrupamos por país e pegamos o valor máximo (o acumulado mais recente)
    df_pizza_total = df_pizza_limpo.groupby('location')['people_fully_vaccinated'].max().reset_index()

    fig_pizza = px.pie(
        df_pizza_total,
        values='people_fully_vaccinated',
        names='location',
        title='Total Acumulado de Vacinados'
    )
    st.plotly_chart(fig_pizza, use_container_width=True)
