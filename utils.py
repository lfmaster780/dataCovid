import pandas as pd
import glob
from datetime import datetime, timedelta

# read all csv in folder 'dataset'


def read_csv():
    list_csv = []
    name_path = 'dataset'
    # Select all csv in folder selected
    names_files = glob.glob(name_path + "/*.csv")
    # join all them
    for filename in names_files:
        df = pd.read_csv(filename, sep=';')
        df_mask = df['codmun'].isnull()
        filtered_df = df[df_mask]
        list_csv.append(filtered_df)

    frame = pd.concat(list_csv, axis=0, ignore_index=True)
    frame['data'] = pd.to_datetime(frame['data'])  # .dt.strftime('%d/%m/%Y')
    return frame

# Calculate all itens


def itens_calculate(df, date, date_start, uf):
    list_all = []
    mask = df['data'] == date.strftime('%Y-%m-%d')
    df_aux = df[mask]
    # Date
    list_all.append(date)

    # State
    if uf == 76:
        list_all.append('Brasil')
    else:
        list_all.append(df['estado'].iloc[0])

    # CasosAcumulado
    list_all.append(int(df_aux['casosAcumulado'].iloc[0]))
    # MediaMovelCasosAtual, MediaMovelCasosAnterior, Situação, Porcentagem
    for i in moving_average(df, date, date_start, 0):
        list_all.append(i)

    # ObitosAcumulados
    list_all.append(df_aux['obitosAcumulado'].iloc[0])
    # MediaMovelObtitosAtual, MediaMovelObitosAnterior, Situação, Porcentagem
    for j in moving_average(df, date, date_start, 1):
        list_all.append(j)

    return list_all


# number = 0 -> Casos or number != 0 -> Óbitos


def moving_average(df, date, date_start, number):
    list_all = []
    if number == 0:
        df_aux = df[['data', 'casosAcumulado']]
    else:
        df_aux = df[['data', 'obitosAcumulado']]

    # MediaMovelAtual
    mean_today = average_call(df, date, date_start, number)
    # MediaMovelAnterior
    mean_before = average_call(
        df, date - timedelta(days=1), date_start, number)

    list_all.append(int(mean_today))
    list_all.append(int(mean_before))

    # Situação e Porcentagem of each moving-average
    if mean_before == 0:
        if mean_today != 0:
            list_all.append('Aumento')
            list_all.append(100)
        else:
            list_all.append('Estabilidade')
            list_all.append('-')
    elif mean_today/mean_before > 1:
        list_all.append('Aumento')
        list_all.append(round(((mean_today/mean_before - 1)*100), 4))
    elif mean_today/mean_before < 1:
        list_all.append('Diminuicao')
        list_all.append(round(abs(mean_today/mean_before - 1)*100, 4))
    else:
        list_all.append('Estabilidade')
        list_all.append(round((mean_today/mean_before - 1)*100, 4))

    return list_all


# Calculate Average Moving


def average_call(df, date, date_start, number):
    colum = ''
    if number == 0:
        colum = 'casosAcumulado'
    else:
        colum = 'obitosAcumulado'

    # First 7 days
    if date.strftime('%Y-%m-%d') < (date_start + timedelta(days=7)).strftime('%Y-%m-%d'):
        mask = (df['data'] <= date.strftime('%Y-%m-%d'))
        df_aux = df[mask]
        return df_aux[colum].sum()/7

    # After
    else:
        # Select part of dataframe that need to calculate mean
        mask = (df['data'] <= date.strftime(
            '%Y-%m-%d')) & (df['data'] > (date - timedelta(days=7)).strftime('%Y-%m-%d'))
        df_aux = df[mask]
        return df_aux[colum].mean()
