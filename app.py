from main import *

glicemia = Glicemia()

df = glicemia.lerCSV('diabetes.csv')

df = glicemia.prePro(df, 'Glucose', 'Glucose', 'Outcome')

metricas = glicemia.metricas(df, 'Glucose')

area = glicemia.area(metricas)

corte = glicemia.melhor_corte(metricas)
print(corte)

x=y=[0, 0.25, 0.5, 0.75, 1]
plt.figure()
plt.title(f'CURVA ROC \n Area: {area}')
sns.lineplot(data=metricas, x='especif_um', y='sensi', label=f'melhor glicemia {corte[0]}')
sns.lineplot(data=x, x=x, y=y)
plt.scatter(x=[corte[1]], y=[corte[2]])
plt.xlabel(f'1-Espec')
plt.legend()
plt.savefig('Curva_Roc.png')

