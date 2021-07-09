import pandas as pd
import glob
from datetime import datetime, timedelta

# Leitura dos arquivos da pasta dataset

def readCSV():
    listCSV = []
    namePath = 'dataset'
    # Select all csv in folder selected
    namesFiles = glob.glob(namePath + "/*.csv")
    # join all them
    for filename in namesFiles:
        df = pd.read_csv(filename, sep=';')
        dfMask = df['codmun'].isnull()
        filtered_df = df[dfMask]
        listCSV.append(filtered_df)

    frame = pd.concat(listCSV, axis=0, ignore_index=True)
    frame['data'] = pd.to_datetime(frame['data'])  # .dt.strftime('%d/%m/%Y')
    return frame

def itensCalculate(df, date, dateStart, uf):
    all = []
    mask = df['data'] == date.strftime('%Y-%m-%d')
    dfAux = df[mask]
    # Date
    all.append(date)

    # State
    if uf == 76:
        all.append('Brasil')
    else:
        all.append(df['estado'].iloc[0])

    # CasosAcumulado
    all.append(int(dfAux['casosAcumulado'].iloc[0]))
    # MediaMovelCasosAtual, MediaMovelCasosAnterior, Situação, Porcentagem
    for i in movingAverage(df, date, dateStart, 0):
        all.append(i)

    # ObitosAcumulados
    all.append(dfAux['obitosAcumulado'].iloc[0])
    # MediaMovelObtitosAtual, MediaMovelObitosAnterior, Situação, Porcentagem
    for j in movingAverage(df, date, dateStart, 1):
        all.append(j)

    return all


# number = 0 -> Casos or number != 0 -> Óbitos


def movingAverage(df, date, dateStart, number):
    all = []
    if number == 0:
        dfAux = df[['data', 'casosAcumulado']]
    else:
        dfAux = df[['data', 'obitosAcumulado']]

    # MediaMovelAtual
    mean_today = averageCall(df, date, dateStart, number)
    # MediaMovelAnterior
    mean_before = averageCall(df, date - timedelta(days=1), dateStart, number)

    all.append(int(mean_today))
    all.append(int(mean_before))

    # Situação e Porcentagem of each moving-average
    if mean_before == 0:
        if mean_today != 0:
            all.append('Aumento')
            all.append(100)
        else:
            all.append('Estabilidade')
            all.append('-')
    elif mean_today/mean_before > 1:
        all.append('Aumento')
        all.append(round(((mean_today/mean_before - 1)*100), 4))
    elif mean_today/mean_before < 1:
        all.append('Diminuicao')
        all.append(round(abs(mean_today/mean_before - 1)*100, 4))
    else:
        all.append('Estabilidade')
        all.append(round((mean_today/mean_before - 1)*100, 4))

    return all

def averageCall(df, date, dateStart, number):
    colum = ''
    if number == 0:
        colum = 'casosNovos'
    else:
        colum = 'obitosNovos'

    # First 7 days
    if date.strftime('%Y-%m-%d') < (dateStart + timedelta(days=7)).strftime('%Y-%m-%d'):
        mask = (df['data'] <= date.strftime('%Y-%m-%d'))
        dfAux = df[mask]
        return dfAux[colum].sum()/7

    # After
    else:
        # Select part of dataframe that need to calculate mean
        mask = (df['data'] <= date.strftime('%Y-%m-%d')) & (df['data'] > (date - timedelta(days=7)).strftime('%Y-%m-%d'))
        dfAux = df[mask]
        return dfAux[colum].mean()
