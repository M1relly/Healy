# -*- coding: utf-8 -*-
"""Healy_Sprint2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PijctIUNkB8jkJLlOmOFWX40JvVbQ0eE

# Healy
#### YOUR HEALTH AI

Já desejou saber os riscos que permeiam sua saúde? Com Healy podemos identificar o padrão que aparecem nos seus exames e com ele indicar a porcentagem de propensão à uma patologia levando você a conhecer mais sobre sua saúde.

<br>

[Download do dataset](https://www.kaggle.com/datasets/davidechicco/chronic-kidney-disease-ehrs-abu-dhabi)

# Análise inicial
"""

# imports
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold

# importando o dataset
kidney = pd.read_csv('/content/ChronicKidneyDisease_EHRs_from_AbuDhabi.csv')

# visualizando informações dos dados
kidney.info()

# visualizando tamanho do dataset
kidney.shape

# visualizando valores duplicados e faltantes
print(f'Número total de dados duplicados: {kidney.duplicated().sum()}')
print('-------------------------------------')
print(f'Número total de valores faltantes: {kidney.isnull().sum().sum()}')

# visualizando correlação entre as variáveis
correlation_matrix = kidney.corr()
plt.figure(figsize=(30, 8))
sns.set(font_scale=1.2)
sns.heatmap(correlation_matrix, annot=True, cmap='RdPu', fmt=".2f", linewidths=0.5)
plt.title('Correlation Matrix', fontsize=30)
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.show()

"""**ANÁLISE DE VARIÁVEIS POSSIVELMENTE IMPACTANTES**
<br>
A variável-alvo será o EventCKD35 visto que indica a incidência de enfermidades renais. Com base na observação e tomando por valor de correlação resultados de acima de 0.1 para determinar impacto significativo temos as variáveis:
<br>
Sex, AgeBaseline, HistoryDiabetes, HistoryCHD, HistoryVascular, HistorySmoking, HistoryHTN, HistoryDLD, DLDmeds, DMmeds, HTNmeds, ACEIARB, CreatinineBaseline e sBPBaseline

"""

# visualizando as primeiras e últimas linhas do dataset
display(kidney)

warnings.filterwarnings("ignore")

# listando variávies categóricas
lista_categoricas = ['Sex', 'HistoryDiabetes', 'HistoryCHD', 'HistoryVascular', 'HistorySmoking', 'HistoryDLD',
        'DLDmeds', 'ACEIARB']

# distribuição das variávies categóricas
plt.figure(figsize=(12,65))
sns.set(rc={'axes.facecolor':'lightgrey', 'figure.facecolor':'white'}, font_scale=0.8)

i = 0
j = 0
for col in lista_categoricas:
    feature = kidney.groupby(col)[col].count()
    plt.subplot(15, 2, i+1)
    sns.barplot(x=feature.index, y=feature.values, palette = 'RdPu')
    plt.title(col, fontsize=15)


    plt.subplot(15, 2, j+2)
    plt.pie(x=feature.values, autopct="%.1f%%", pctdistance=0.8, labels=feature.index)
    plt.title(col, fontsize=15)
    i += 2
    j += 2
plt.show()

# relacionamento das variáveis com risco de ataque cardíaco
kidney_probability = kidney.corr()['EventCKD35']
kidney_probability = kidney_probability.drop('EventCKD35', axis=0).sort_values(ascending=False)

# plot no gráfico
plt.figure(figsize=(10,5))
sns.set(font_scale=0.8)
sns.barplot(x=kidney_probability.index, y=kidney_probability, color='pink')
plt.xticks(rotation=90)
plt.ylim(-0.02, 0.05)
plt.title('Relacionamento entre as variáveis com probabilidade de doença renal', fontsize=15)
plt.show()

"""# Modelos de classificação
Metade dos dados é do tipo booleana e a outra metade é do tipo numérico. A fim de classsificar grupos de risco para o desenvolvimento de problemas no rim, faremos diferentes modelos para observar a acurácia.
"""

# definindo variáveis preditivas
X = kidney[['Sex', 'HistoryDiabetes', 'HistoryCHD', 'HistoryVascular', 'HistorySmoking', 'HistoryDLD',
        'DLDmeds', 'ACEIARB']]

# definindo variável alvo
y = kidney['EventCKD35']

# separando dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

"""## Logistic Regression"""

# separando treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# treinando a regresssão logística
regression = LogisticRegression()
regression.fit(X_train, y_train)

# fazendo previsões
y_pred = regression.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Acurácia:", accuracy)

cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='RdPu')
plt.xlabel('Previsões')
plt.ylabel('Valores Reais')
plt.title('Matriz de Confusão')
plt.show()

"""## Decision Tree"""

# treinando o modelo
decision = DecisionTreeClassifier(random_state=42)
decision.fit(X_train, y_train)

# acurácia
y_pred = decision.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f'Acurácia: {accuracy}')

"""## Random Forest"""

# criando e treinando o modelo
random = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
random.fit(X_train, y_train)

# acurácia
y_pred = random.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f'Acurácia: {accuracy}')

# avaliando importância das variáveis
importances = random.feature_importances_

for i, importance in enumerate(importances):
    print(f'Variável {i+1}: {importance:.2f}')

# visualização em matriz de confusão
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='RdPu')
plt.xlabel('Previsões')
plt.ylabel('Valores Reais')
plt.title('Matriz de Confusão')
plt.show()

"""# Validação cruzada
A fim de analisar a performance do modelo será realizada uma validação cruzada com base em duas estratégias: KFold e StratifiedKFold.
A primeira é recomendada para datasets balanceados mas para problemas de regressão e a outra para datasets desbalanceados para problemas de classificação.
Cada uma das estratégias supre uma necessidade do dataset mas com o objetivo de observar a performance haverá uma comparação de resultados no final.

## Logistic Regression
"""

# acurácia separando o modelo em folhas
kf = KFold(n_splits=5, shuffle=True, random_state=42)
scores_kfold = cross_val_score(regression, X, y, cv=kf, scoring='accuracy')

print("Acurácia em cada fold:", scores_kfold)
print("Acurácia média:", scores_kfold.mean())

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores_stratified = cross_val_score(regression, X, y, cv=skf, scoring='accuracy')

print("Acurácia em cada fold:", scores_stratified)
print("Acurácia média:", scores_stratified.mean())

"""## Decision Tree"""

# kfold
kf = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(decision, X, y, cv=kf, scoring='accuracy')

print("Acurácia em cada fold:", scores)
print("Acurácia média:", scores.mean())

# stratified
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(decision, X, y, cv=skf, scoring='accuracy')
print("Acurácia em cada fold:", scores)
print("Acurácia média:", scores.mean())

"""## Random Forest"""

# kfold
kf = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(random, X, y, cv=kf, scoring='accuracy')

print("Acurácia em cada fold:", scores)
print("Acurácia média:", scores.mean())

# stratified
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(random, X, y, cv=skf, scoring='accuracy')
print("Acurácia em cada fold:", scores)
print("Acurácia média:", scores.mean())

"""# Conclusões



**Logistic Regression:** 0.878
<br>
**Decision Tree:** 0.858
<br>
**Random Forest:** 0.868
<br>
<br>
**KFold da Logistic:** 0.883
<br>
**KFold da Decision:** 0.877
<br>
**KFold da Random:** 0.871
<br>
<br>
**SKF da Logistic:** 0.894
<br>
**SKF da Decision:** 0.867
<br>
**SKF da Random:** 0.871
"""