# -*- coding: utf-8 -*-
"""Healy_Sprint4

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XpxizNqle1omnn3MKf2Aa8lhvPJYybxH

# Healy
#### YOUR HEALTH AI

Já desejou saber os riscos que permeiam sua saúde? Com Healy podemos identificar o padrão que aparece nos seus exames e com ele indicar a porcentagem de propensão à uma patologia levando você a conhecer mais sobre sua saúde.

<br>

[Download do dataset](https://www.kaggle.com/datasets/davidechicco/chronic-kidney-disease-ehrs-abu-dhabi)

*  Pegar informações inputadas no front-end ou fazer as correções de inputs e tratamento de strings
*  Demonstrar que o modelo é capaz de se ajustar a outros datasets
*  Ajustar resultados e tratamentos com base na instituição

# Importando modelo da Logistic Regression
Anteriormente foi realizada uma análise comparativa de modelos distintos com 2 tipos de validação e a melhor performance é oriunda do modelo de Regressão Logística com Stratified Fold.
"""

# imports
import pandas as pd
import numpy as np
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

# import do dataset
kidney = pd.read_csv("/content/ChronicKidneyDisease_EHRs_from_AbuDhabi.csv")

# definindo variáveis preditivas
X = kidney[['Sex', 'HistoryDiabetes', 'HistoryCHD', 'HistoryVascular', 'HistorySmoking', 'HistoryDLD',
        'DLDmeds', 'ACEIARB']]

# definindo variável alvo
y = kidney['EventCKD35']

# separando dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# separando treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# treinando a regresssão logística
regression = LogisticRegression()
regression.fit(X_train, y_train)

# fazendo previsões
y_pred = regression.predict(X_test)

# predição com modelo original
accuracy = accuracy_score(y_test, y_pred)
print("Acurácia:", accuracy)

# predição com validação cruzada stratified fold
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores_stratified = cross_val_score(regression, X, y, cv=skf, scoring='accuracy')

print("Acurácia em cada fold:", scores_stratified)
print("Acurácia média:", scores_stratified.mean())

"""# Importando dados do usuário
Segundo demonstrado na primeira parte, as colunas mais importantes para identificação de uma possível ascensão a um quadro clínico de doença renal são:
<br>
Sex, AgeBaseline, HistoryDiabetes, HistoryCHD, HistoryVascular, HistorySmoking, HistoryHTN, HistoryDLD, DLDmeds, DMmeds, HTNmeds, ACEIARB, CreatinineBaseline e sBPBaseline

"""

display(kidney)

# solicitando inputs
sex = input("Qual o seu sexo? (M/F): ")
historyDiabetes = input("Você tem histórico de diabetes? (S/N): ")
historyCHD = input("Você tem histórico de doença cardíaca? (S/N): ")
historyVascular = input("Você tem histórico de doença vascular? (S/N): ")
historySmoking = input("Você tem histórico de fumo? (S/N): ")
historyDLD = input("Você tem dislipidemia? (S/N): ")
DLDmeds = input("Você consome medicamentos para dislipidemia? (S/N): ")
ACEIARB = input("Você usa medicamentos para tratamento de pressão arterial? (S/N): ")

#  inputs.clear()
inputs = []
print(inputs)

# tratando a variável sex para evitar valores nulos, espaços vazios e converter para letras minúsculas
try:
  sex = (sex or "").strip().lower()
  valid_sexes = {"m", "masculino"}
  if sex in valid_sexes:
    inputs.append(1)
  else:
    inputs.append(0)
except (AttributeError, ValueError):
    print("Houve erro na inserção de dados.")

# a exception trata casos em que o objeto não possui um método lower ou strip
# a exception trata erro caso a string não seja válida

# tratando variáveis históricas
try:
  for history in [historyDiabetes, historyCHD, historyVascular, historySmoking, historyDLD, DLDmeds, ACEIARB]:
    if sex is not None:
      if history.lower() == 'S' or sex.lower() == "Sim":
        inputs.append(1)
      else:
        inputs.append(0)
except:
  print("Houve erro na inserção de dados.")

print(inputs)

# criando o array X_test
X_test = np.array(inputs).reshape(1, -1)

# imprimindo o array
print(X_test)

"""# Aplicando o modelo
Indicando tratamento ao usuário com base na probabilidade de desenvolvimento da enfermidade indicada pelo modelo comparativo Healy.
"""

# fazendo a predição para visualizar a probabilidade de classe 1 (positiva)
prediçao = regression.predict(X_test)[0]
probabilidade = regression.predict_proba(X_test)[0][1]

print(f"Predição: {prediçao}")
print(f"Probabilidade de classe positiva: {probabilidade}")

# fazendo a recomendação
if probabilidade > 0.3:
  print("""
  O tratamento para DRC tem como objetivo prevenir a progressão da doença, impedindo que seja desenvolvida uma falência renal, além de ser útil para aliviar os sintomas. O tratamento indicado pelo nefrologista pode variar de acordo com o estado geral de saúde da pessoa e o estágio da DRC
1. uso de remédios
2. mudar a alimentação
3. diálise
4. transplante renal
  """)
else:
  print(
      """
1. Controle a pressão arterial
    a. dieta com baixo teor de sal, exercícios físicos, controle do peso, moderação no consumo de bebidas ou medicamentos
2. Controlar níveis de glicose
3. Evitar medicamentos que fazem mal aos rins
    b. medicamentos, como anti-inflamatórios, usados de forma crônica podem danificar os rins ou o consumo
4. Controlar os valores do ácido úrico
5. Evitar o cigarro
6. Fazer exames de sangue e urina frequentemente
  """)

"""# Embedding com Gemini
As dúvidas podem ser frequentes em quesitos médicos mas com uma pesquisa inteligente habilitada e capacitada por uma busca semântica em documentos com o Gemini, a inteligência artifificial do Google, a devolutiva para questões rápidas e pontuais pode economizar o tempo do médico e do paciente evitando esperas por respostas.
Os documentos inseridos para busca semântica substituem um chatbot especializado e garantem que o paciente compreenda mais sobre o cenário oferecido visto que a instituição de saúde que utiliza o sistema pode inputar as informações que deseja que sejam conhecidas pelo paciente.

<br>

## Um projeto de futuro
Incluir ao app a AMELIA, a Assistente Médica Legal Ligada à Inteligência Aritificial, é um dos planos de desenvolvimento da equipe. Um chatbot inteligente irá atender mais do que as necessidades de consultar resultados dos paciente, mas também ofertará a eles mais segurança em suas pesquisas, não precisando recorrer a buscas insastisfatórias sobre saúde na internet.
Essa é mais uma forma de Healy atender às necessidades específicas de cada paciente.
"""

! pip install -U -q google-generativeai

# importando as configurações inicias
import numpy as np
import pandas as pd
import google.generativeai as genai

GOOGLE_API_KEY = ('AIzaSyDKLlDNrQ3cOT5cfnc3Z2tt0-lh3bgqN8U')
genai.configure(api_key=GOOGLE_API_KEY)

# listando modelos disponíveis
for m in genai.list_models():
  if 'embedContent' in m.supported_generation_methods:
    print(m.name)

# armazenando o modelo a ser utilizado em uma variável
model = 'models/embedding-001'

"""**DOCUMENTOS**

Os documentos listados abaixo são simulações de inputs médicos para tiradas de dúvidas. A documentação e procedimento para cada enfermidade podem ser especificados em dataframes personalizados.

"""

# definindo os documentos para embedding
pressao_arterial = {
    'Tratamento': 'Controle adequado da pressão arterial',
    'Definição': 'essa é uma medida fundamental para retardar a progressão da doença renal crônica. O ideal geralmente é que a pressão seja mantida abaixo de 130/80 mmHg. A restrição de sal (sódio) é muito importante, para isso deve-se evitar o uso de temperos prontos; saleiro à mesa; alimentos enlatados; sucos em pó; embutidos como salames, salsicha, presunto, mortadela, copa; e queijos.'
}

glicemia = {
    'Tratamento': 'Controle adequado da glicemia',
    'Definição': 'para os pacientes com diabetes esse é um passo fundamental, sendo recomendado, de forma geral, manter a hemoglobina glicada (HbA1c), um exame de sangue, menor que 7%. Uma dieta adequada é aquela com redução de carboidratos (massas, pães, batata, arroz), preferindo o uso de alimentos integrais. O açúcar livre é proibido e deve ser substituído por adoçantes.'
}

tabagismo = {
    'Tratamento': 'Interrupção do tabagismo',
    'Definição': 'atualmente existem várias formas de tratamento para parar de fumar, incluindo tratamento psicológico e medicamentos. Parar de fumar traz benefícios não só para os rins, mas também para o coração, pulmões e para os vasos sanguíneos.'
}

dislipidemia = {
    'Tratamento': 'Tratamento da dislipidemia',
    'Definição': 'reduzir os níveis de colesterol apresenta benefícios não só para os rins, mas também para o coração e vasos sanguíneos. Você deve evitar frituras, molhos e carnes gordurosas.'
}

proteina = {
    'Tratamento': 'Controle da perda de proteína da urina',
    'Definição': 'a proteinúria (perda de proteína na urina) significa que há lesão no rim, então reduzir a perda de proteínas é fundamental para diminuir a progressão da doença renal crônica. Há medicações disponíveis hoje que auxiliam na redução da perda de proteína na urina. Converse com seu médico clínico sobre isso ou procure um nefrologista.'
}

anemia = {
    'Tratamento': 'Tratamento da anemia',
    'Definição': 'anemia é a diminuição da quantidade de glóbulos vermelhos no sangue. Os glóbulos vermelhos (hemácias) são responsáveis pelo transporte de oxigênio para todas as células do nosso corpo. Quando o paciente tem anemia, dependendo da gravidade, ele pode sentir desânimo, falta de apetite, fraqueza nas pernas, sonolência, falta de ar quando caminha, entre outros.'
}

osseos = {
    'Tratamento': 'Tratamento dos distúrbios ósseos e minerais associados à doença renal crônica: ',
    'Definição': 'é comum ocorrer uma queda dos níveis de cálcio, de vitamina D e/ou um aumento do fósforo e do hormônio produzido pelas glândulas paratireoides (paratormônio-PTH). Para cada uma dessas condições existe um tratamento específico a ser instituído.'
}

acidose = {
    'Tratamento': 'Tratamento da acidose no sangue',
    'Definição': 'acidose é a condição de acidez que se desenvolve no sangue porque os rins não conseguem colocar para fora o excesso de ácido que se forma continuamente com o funcionamento do nosso organismo. Às vezes, é necessário o uso do bicarbonato de sódio para ajudar a corrigir esta situação. A acidose pode contribuir para o aumento do potássio no sangue. É importante que o uso do bicarbonato seja feito apenas se o seu médico orientar esse tratamento.'
}

potassio = {
    'Tratamento': 'Tratamento do aumento do potássio no sangue (hipercalemia)',
    'Definição': 'o potássio é um mineral que tem como fontes principais as frutas e os vegetais. No paciente que tem doença renal crônica, ele tende a se acumular no sangue, pois o rim deixa de eliminá-lo. Quando os níveis de potássio no sangue ficam muito altos, pode ocorrer fraqueza muscular intensa, arritmias e até parada cardíaca. '
}

dieta = {
    'Tratamento': 'Dieta adequada',
    'Definição': 'não existe uma dieta única para todos os pacientes. Cada paciente deverá ser avaliado de forma individual e ter sua dieta elaborada com o auxílio de um(a) nutricionista. Em geral, a restrição alimentar aumenta na medida em que a doença progride e na medida em que medicamentos não são capazes de manter os níveis de potássio, cálcio, fósforo e ácidos dentro do desejado.'
}

dialise = {
    'Tratamento': 'Preparo do paciente para terapia de diálise ou transplante renal',
    'Definição': 'a abordagem sobre essas terapias inicia-se quando o paciente evolui para função renal ao redor de 20%. É explicado as diferenças entre hemodiálise e diálise peritoneal e averiguada a possibilidade de transplante com doador vivo. O início de umas das 3 terapias irá depender das condições físicas, dos sintomas e dos exames laboratoriais.'
}

# convertendo os dicionários em um único documento
documentos = [pressao_arterial, glicemia, tabagismo, dislipidemia, proteina, anemia, osseos, acidose, potassio, dieta, dialise]

# convertendo o documento em um dataframe
df = pd.DataFrame(documentos)
df

# automatizando o embedding
def embed_fn(title, text):
  return genai.embed_content(model = model,
                                 content = text,
                                 title = title,
                                 task_type = 'RETRIEVAL_DOCUMENT')['embedding']

# criando a nova coluna embedding
df['Embeddings'] = df.apply(lambda row: embed_fn(row['Tratamento'], row['Definição']), axis = 1)
df

# configurando os padrões de resposta
def generate_search(query, base, model):
  queryEmbedding = genai.embed_content(model = model, content = query, task_type = 'RETRIEVAL_QUERY')

  # criando as stacks do embedding
  scalar_products = np.dot(np.stack(df['Embeddings']), queryEmbedding['embedding'])
  index = np.argmax(scalar_products)
  return df.iloc[index]['Definição']

# definindo geração de métodos
generation_config = {
    'candidate_count': 1,
    'temperature': 0.5
}

# selecionando o modelo de resposta da IA
modelo_ia = genai.GenerativeModel('gemini-1.0-pro',
                                  generation_config = generation_config)

# criando a pesquisa no dataframse
pergunta = input("Digite sua pergunta: ")

resposta = (generate_search(pergunta, df, model))

'''
Embeddings são apenas consultas mas uma resposta reformulada será capaz de adicionar humanidade e
personalização nas respostas. Aqui podem ser acrescentadas formas de conduzir a resposta sendo selecionadas
a critério do agente de saúde
'''
resposta_reformulada = f'Reformule essa sentença mas não adicione nenhuma informação extra. Seja educado, dê respostas de fácil compreensão e diretas: {resposta}'

modelo_ia = genai.GenerativeModel('gemini-1.0-pro',
                                  generation_config = generation_config)

# gerando a resposta humanizada
resposta2 = modelo_ia.generate_content(resposta_reformulada)
print(resposta2.text)