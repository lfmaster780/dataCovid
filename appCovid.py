import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import utils

# Load Data
df = utils.readCSV()

st.title('Números da COVID-19 no Brasil')

dateEnd = df['data'].iloc[-1].date()
dateStart = df['data'].iloc[0].date()

date = st.date_input('Selecione a Data', dateEnd, dateStart, dateEnd)

# Codigos UF
listUF = [11, 12, 13, 14, 15, 16, 17, 21, 22, 23, 24, 25,26, 27, 28, 29, 31, 32, 33, 35, 41, 42, 43, 50, 51, 53, 76]

dfProcessed = pd.DataFrame(columns=['Data', 'Estado', 'CasosAcumulado', 'MediaMovelCasosAtual', 'MediaMovelCasosAnterior','Situacao', 'Percentual(%)', 'ObitosAcumulado', 'MediaMovelObitosAtual', 'MediaMovelObitosAnterior', 'Situacao', 'Percentual(%)'])

for uf in listUF:
    df_mask = df['coduf'] == uf
    filteredDf = df[df_mask]
    filteredDf = filteredDf.iloc[:, lambda df: [1, 3, 7, 8, 9, 10, 11, 12, 13, 14, 15]]
    filteredDf = filteredDf.sort_values(by=['data'])
    list_data = utils.itensCalculate(filteredDf, date, dateStart, uf)
    dfProcessed.loc[len(dfProcessed)] = list_data

# Divisao dos Dataframes
dfProcessedCasos = dfProcessed.iloc[:, lambda df: [0, 1, 2, 3, 4, 5, 6]]
dfProcessedObitos = dfProcessed.iloc[:, lambda df: [0, 1, 7, 8, 9, 10, 11]]


#Casos
st.write("Data(Dia/Mês/Ano):",str(date.day),"/",str(date.month),"/",str(date.year))
st.header('Número de Casos de COVID-19 no Brasil '+str(date.day)+"/"+str(date.month)+"/"+str(date.year))
st.write("Obs: Número total do Brasil ao final da tabela")
st.dataframe(dfProcessedCasos)

st.header('Casos Acumulados de COVID-19 por Estado')
dfOrdenado = dfProcessedCasos.sort_values(by=['CasosAcumulado'], ascending=True)
fig, ax = plt.subplots()
ax.barh(dfOrdenado['Estado'][:-1],dfOrdenado['CasosAcumulado'][:-1])
st.pyplot(fig)

st.header('Média Móvel de Casos por Estado')
dfOrdenado = dfProcessedCasos.sort_values(by=['MediaMovelCasosAtual'], ascending=True)
fig, ax = plt.subplots()
ax.barh(dfOrdenado['Estado'][:-1],dfOrdenado['MediaMovelCasosAtual'][:-1])
st.pyplot(fig)


#Mortes
st.header('Número de Óbitos por COVID-19 no Brasil '+str(date.day)+"/"+str(date.month)+"/"+str(date.year))
st.write("Obs: Número total do Brasil ao final da tabela")
st.dataframe(dfProcessedObitos)

st.header('Óbitos Acumulados por COVID-19 por Estado')
dfOrdenado = dfProcessedObitos.sort_values(by=['ObitosAcumulado'], ascending=True)
fig, ax = plt.subplots()
ax.barh(dfOrdenado['Estado'][:-1],dfOrdenado['ObitosAcumulado'][:-1])
st.pyplot(fig)

st.header('Média Móvel de Óbitos por Estado')
dfOrdenado = dfProcessedObitos.sort_values(by=['MediaMovelObitosAtual'], ascending=True)
fig, ax = plt.subplots()
ax.barh(dfOrdenado['Estado'][:-1],dfOrdenado['MediaMovelObitosAtual'][:-1])
st.pyplot(fig)
