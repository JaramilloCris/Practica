import pandas as pd
import pyodbc
import numpy as np

server = '172.16.1.38'
username = 'sa'
password = 'qwerty123'
driver = '{ODBC Driver 17 for SQL Server}'
cn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';UID=' + username + ';PWD=' + password)


def seleccionar_accion(nemotecnico):

    accion = "SELECT * FROM [dbPortFolio].[dbo].[TdPlanvitalCartera] WHERE TipoLva = 'EXT' AND Nemotecnico = '"+ str(nemotecnico) +"'"
    accion = pd.read_sql(accion, cn)

    return accion

def historico(nemotecnico, n = 60):

    accion_actual = seleccionar_accion(nemotecnico)

    nominales = accion_actual["Nominales"]
    monto = accion_actual["ValorizacionCLP"]
    largo = len(nominales)
    if largo < n : 
        ## Hay que ir a buscar el IPSA
    else:
        largo_final = n
        arreglo_valores = []

        for i in range(largo_final):

            calculo = monto[i]/nominales[i]
            arreglo_valores.append(calculo)


        df1 = pd.DataFrame()
        df1["Moneda"] = ["CLP"]
        df1["Nombre"] = [nemotecnico]
        df1["Inversion"] = [accion_actual["ValorizacionCLP"][0]]
        df1["Historico"] = [[arreglo_valores]]
    return df1