import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import utils

# Load Data
df = utils.read_csv()

st.title('Números da COVID-19 no Brasil')

date_end = df['data'].iloc[-1].date()
date_start = df['data'].iloc[0].date()

date = st.date_input('Selecione a Data', date_end, date_start,
                     date_end, help='Coloque a data que queira gerar o relatório.')

# Codigos UF
list_uf = [11, 12, 13, 14, 15, 16, 17, 21, 22, 23, 24, 25,
           26, 27, 28, 29, 31, 32, 33, 35, 41, 42, 43, 50, 51, 53, 76]

df_processed = pd.DataFrame(columns=['Data', 'Estado', 'CasosAcumulado', 'MediaMovelCasosAtual', 'MediaMovelCasosAnterior',
                                     'Situacao', 'Percentual', 'ObitosAcumulado', 'MediaMovelObitosAtual', 'MediaMovelObitosAnterior', 'Situacao', 'Percentual'])

for uf in list_uf:
    df_mask = df['coduf'] == uf
    filtered_df = df[df_mask]
    filtered_df = filtered_df.iloc[:, lambda df: [
        1, 3, 7, 8, 9, 10, 11, 12, 13, 14, 15]]
    filtered_df = filtered_df.sort_values(by=['data'])
    list_data = utils.itens_calculate(
        filtered_df, date, date_start, uf)
    df_processed.loc[len(df_processed)] = list_data

# Divisao dos Dataframes 
df_processed_casos = df_processed.iloc[:, lambda df: [0, 1, 2, 3, 4, 5, 6]]
df_processed_obitos = df_processed.iloc[:, lambda df: [0, 1, 7, 8, 9, 10, 11]]


#Casos
st.header('Número de Casos de COVID-19 no Brasil')
st.dataframe(df_processed_casos)

st.header('Casos de COVID-19 x Estado')
df_ordenado = df_processed_casos.sort_values(
    by=['CasosAcumulado'], ascending=True)
fig, ax = plt.subplots()
ax.barh(df_ordenado['Estado'][:-1],
        df_ordenado['CasosAcumulado'][:-1])
st.pyplot(fig)

st.header('Média Móvel de Casos x Estado')
df_ordenado = df_processed_casos.sort_values(
    by=['MediaMovelCasosAtual'], ascending=True)
fig, ax = plt.subplots()
ax.barh(df_ordenado['Estado'][:-1],
        df_ordenado['MediaMovelCasosAtual'][:-1])
st.pyplot(fig)


#Mortes
st.header('Número de Mortes de COVID-19 no Brasil')
st.dataframe(df_processed_obitos)

st.header('Óbitos por COVID-19 x Estado')
df_ordenado = df_processed_obitos.sort_values(
    by=['ObitosAcumulado'], ascending=True)
fig, ax = plt.subplots()
ax.barh(df_ordenado['Estado'][:-1],
        df_ordenado['ObitosAcumulado'][:-1])
st.pyplot(fig)

st.header('Média Móvel de Óbitos x Estado')
df_ordenado = df_processed_obitos.sort_values(
    by=['MediaMovelObitosAtual'], ascending=True)
fig, ax = plt.subplots()
ax.barh(df_ordenado['Estado'][:-1],
        df_ordenado['MediaMovelObitosAtual'][:-1])
st.pyplot(fig)
