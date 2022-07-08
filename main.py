import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import math

class Glicemia:

    def __init__(self):
        #adicionar os resultados dos metodos pra armazenar
        pass

    def lerCSV(self, csv):
        df = pd.read_csv(csv)
        return df
  
    def prePro(self, df, sortBy, *args):
        df = df[list(args)]
        df = df.sort_values(sortBy)
        df = df[df["Glucose"] > 0]
        return df
    
    def metricas(self, df, coluna):
        corte = list(df[coluna].unique())
        total_zero = df.Outcome.value_counts().sort_index()[0]
        total_um = df.Outcome.value_counts().sort_index()[1]
        metricas = []
        indices = []
        for i in corte:
            try:
                TN = df[df[coluna] <= i].Outcome.value_counts().sort_index()[0]
                TP = df[df[coluna] > i].Outcome.value_counts().sort_index()[1]
                FN = total_um - TP
                FP = total_zero - TN
                sensi = TP/(TP+FN)
                especif_um = FP/(FP+TN)
                acuracia = (TP + TN)/(TN+TP+FN+FP)
                metricas.append([sensi, especif_um, acuracia])
                indices.append(i)
            except:
                pass
        metricas = pd.DataFrame(np.vstack(metricas), columns=['sensi', 'especif_um', 'acuracia'], index=indices)
        return metricas

    def area(self, df):
        res = 0
        #print(type(df))
        for i in range(1, len(df)):
            y0 = df.sensi.tolist()[i-1]
            y1 = df.sensi.tolist()[i]
            x0 = df.especif_um.tolist()[i-1]
            x1 = df.especif_um.tolist()[i]
            res += ((y0 + y1) * (x0 - x1))/2
        return res

    def melhor_corte(self, df):
        dist_list = []
        for i in range(len(df)):
            c1 = df.especif_um.tolist()[i]
            c2 = 1 - df.sensi.tolist()[i]
            distance = math.sqrt(c1**2 + c2**2)
            dist_list.append(distance)
        ind = dist_list.index(min(dist_list))
        return [df.iloc[ind].name, df.iloc[ind].especif_um, df.iloc[ind].sensi]