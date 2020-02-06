from Activo import Activo
import datetime
import pandas as pd
import numpy as np
from UtilesValorizacion import parsear_curva
from Matematica import interpolacion_log_escalar


class Derivado(Activo):

    def __init__(self, derivado_generico, monedaCartera, fecha_valorizacion, cn):

        super(Derivado, self).__init__(monedaCartera, fecha_valorizacion, cn)

        self.derivado_generico = derivado_generico
        self.derivado_generico.genera_flujos()
        self.derivado_generico.valoriza_flujos()



    def get_derivado_generico(self):

        return self.derivado_generico

    def get_flujos(self):

        return self.get_derivado_generico().flujos_valorizados[["ID","ActivoPasivo", "Fecha"\
            , "FechaFixing", "FechaFlujo", "FechaPago", "Flujo", "ValorPresenteMonFlujo", "Moneda", "MonedaBase"]]

    def seleccionar_curva_derivados(self, moneda, n, fecha=datetime.date(2018, 1, 22)):

        monedas = moneda
        cnn = self.get_cn()

        if moneda == "UF": #Funciona para el error de CLF
            monedas = "CLF"

        curva = ("SELECT TOP(" + str(n) + ")* FROM [dbDerivados].[dbo].[TdCurvasDerivados] WHERE Tipo = 'CurvaEfectiva_"+ str(monedas) +"' AND Hora = '1500' AND Fecha > '" + str(fecha) + "'")
        curva = pd.read_sql(curva, cnn)
        return curva


    def set_historico(self):

        n = 200
        moneda = self.get_flujos()["Moneda"][0]
        curvas = self.seleccionar_curva_derivados(moneda, n)[::-1]

        largo = len(self.get_plazos())
        cantidad_curvas = len(curvas["Curva"])
        pivotes = self.get_plazos()

        matriz = np.zeros([cantidad_curvas, largo])

        # Por cada plazo
        for i in range(largo):
            
            # Por cada curva
            for j in range(cantidad_curvas):

                valor_dia = pivotes[i]
                curva = curvas["Curva"][j]
                fecha_curva = curvas["Fecha"][j]
                curva_parseada = parsear_curva(curva, fecha_curva)
                matriz[j][i] = interpolacion_log_escalar(valor_dia, curva_parseada)
                
        self.historicos = pd.DataFrame(matriz)

    def corregir_moneda(self):

        pass


