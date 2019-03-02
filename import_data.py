#!/usr/bin/env python
# -*- coding: utf-8 -*-

def generar_datos():
    # Librerias
    import dash
    import pandas as pd
    import numpy as np
    import xlrd
    import os

    os.system('wget https://datos.madrid.es/egob/catalogo/212531-10515086-calidad-aire-tiempo-real.csv -O horario.csv')
    os.system('wget https://datos.madrid.es/egob/catalogo/212629-0-estaciones-control-aire.xls -O estaciones.xls')

    horario =  pd.read_csv("horario.csv", ";").iloc[:, 2:]
    estaciones = pd.read_excel("estaciones.xls", skiprows = 4).iloc[:24, [1, 2, 3, 4, 5]]

    def dms2dd(degrees, minutes, seconds, direction):
        dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
        if direction == 'S' or direction == 'O':
            dd *= -1
        return pd.to_numeric(dd)

    LATITUD = np.zeros(estaciones.shape[0])
    LONGITUD = np.zeros(estaciones.shape[0])

    for i in range(estaciones.shape[0]):
        a = estaciones.LATITUD[i]
        a = a.replace("\"", "").replace("'", "").replace("º", "").replace(",", ".")
        b = a.split(" ")

        LATITUD[i] = dms2dd(b[0], b[1], b[1], b[-1][-1])

    for i in range(estaciones.shape[0]):
        a = estaciones.LONGITUD[i]
        a = a.replace("\"", "").replace("'", "").replace("º", "").replace(",", ".")
        b = a.split(" ")

        LONGITUD[i] = dms2dd(b[0], b[1], b[1], b[-1][-1])

    estaciones.LATITUD = LATITUD
    estaciones.LONGITUD = LONGITUD
    estaciones.iloc[:, 0] = pd.to_numeric(estaciones.iloc[:, 0])

    df = pd.merge(horario, estaciones, left_on = 'ESTACION', right_on = 'NÚMERO')

    df.columns.values[-2] = "lon"
    df.columns.values[-1] = "lat"

    # compuestos = {"Dióxido de Azufre": 1, "Monóxido de Carbono" : 6, "Monóxido de Nitrógeno": 7, "Dióxido de Nitrógeno": 8, "Partículas < 2.5 µm": 9, "Partículas < 10 µm": 10, "Óxidos de Nitrógeno": 12, "Ozono": 14, "Tolueno": 20, "Benceno": 30, "Etilbenceno": 35, "Metaxileno": 37, "Paraxileno": 38, "Ortoxileno": 39, "Hidrocarburos totales (hexano) ": 42, "Metano": 43, "Hidrocarburos no metánicos (hexano)": 44}

    return(df)




# [{'label': i, "value": compuestos[i]} for i in compuestos]
