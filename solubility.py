from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score

composto1 = [1,1,1]
composto2 = [0,0,0]
composto3 = [1,0,1]
composto4 = [0,1,0]
composto5 = [1,1,0]
composto6 = [0,0,1]

dados_treino = [composto1, composto2, composto3, composto4, composto5, composto6]
rotulos_treino = ['S', 'N', 'S', 'N', 'S', 'S']

modelo = LinearSVC()
modelo.fit(dados_treino, rotulos_treino)
#fit pega os dados do treino, com os rotulos e começa a aprender

teste1 = [1,0,0]
teste2 = [0,1,1]
teste3 = [1,0,1]

dados_teste = [teste1, teste2, teste3]
rotulo_teste = ['S','S','S']

previsoes = modelo.predict(dados_teste)

mapeamento_previsoes = {'S': 'Soluvel', 'N': 'Não soluvel'}

taxa_acerto = accuracy_score(rotulo_teste, previsoes)
print('taxa de acerto: ', taxa_acerto * 100)