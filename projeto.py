# -*- coding: utf-8 -*-
"""
Script Completo para Desenvolvimento de Modelo Preditivo de Regressão
(usando colunas em inglês do “insurance.csv” e calculando VIF corretamente)

Dependências:
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- statsmodels

Instale com:
    pip install pandas numpy matplotlib seaborn scikit-learn statsmodels
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from statsmodels.stats.outliers_influence import variance_inflation_factor

# --- 1. CARREGAR E EXPLORAR A BASE DE DADOS ---
def carregar_e_explorar(caminho_csv="insurance.csv"):
    """
    Carrega o CSV e imprime informações básicas, estatísticas e checa faltantes.
    Retorna o DataFrame carregado.
    """
    df = pd.read_csv(caminho_csv)

    print("\n=== 1. EXPLORAÇÃO INICIAL DOS DADOS ===\n")
    print("Primeiras 5 linhas do DataFrame:")
    print(df.head(), "\n")
    print(f"Número de linhas: {df.shape[0]}, Número de colunas: {df.shape[1]}\n")

    print("Tipos de cada coluna:")
    print(df.dtypes, "\n")

    print("Estatísticas descritivas das colunas numéricas:")
    print(df.describe(), "\n")

    print("Contagem de valores ausentes por coluna:")
    print(df.isna().sum(), "\n")

    return df

# --- 2. VISUALIZAÇÕES INICIAIS ---
def visualizacoes_iniciais(df):
    """
    Gera gráficos univariados e bivariados para entender a distribuição das variáveis.
    Usa as colunas originais: 'age', 'sex', 'bmi', 'children', 'smoker', 'region', 'charges'.
    """
    print("\n=== 2. VISUALIZAÇÕES INICIAIS ===\n")

    # 2.1. Histograma da variável alvo (“charges”)
    plt.figure(figsize=(6, 4))
    sns.histplot(df["charges"], kde=True)
    plt.title("Distribuição dos Custos Médicos (‘charges’)")
    plt.xlabel("Charges (USD)")
    plt.ylabel("Frequência")
    plt.tight_layout()
    plt.show()

    # 2.2. Boxplot de “charges” por “smoker”
    plt.figure(figsize=(6, 4))
    sns.boxplot(x="smoker", y="charges", data=df)
    plt.title("Charges por Status de Smoker")
    plt.xlabel("Smoker")
    plt.ylabel("Charges (USD)")
    plt.tight_layout()
    plt.show()

    # 2.3. Countplot de “region”
    plt.figure(figsize=(6, 4))
    sns.countplot(x="region", data=df)
    plt.title("Contagem de Observações por Region")
    plt.xlabel("Region")
    plt.ylabel("Contagem")
    plt.tight_layout()
    plt.show()

    # 2.4. Dispersão: BMI x charges, colorido por smoker
    plt.figure(figsize=(6, 4))
    sns.scatterplot(x="bmi", y="charges", hue="smoker", data=df, alpha=0.6)
    plt.title("Dispersão: BMI vs. Charges (colorido por Smoker)")
    plt.xlabel("BMI")
    plt.ylabel("Charges (USD)")
    plt.tight_layout()
    plt.show()

# --- 3. PRÉ-PROCESSAMENTO ---
def preprocessamento(df):
    """
    Executa limpeza de dados (dropna) e codificação de variáveis categóricas.
    Retorna X (features) e y (target) prontos para modelagem.
    """
    print("\n=== 3. PRÉ-PROCESSAMENTO DE DADOS ===\n")

    # 3.1. Remover linhas com valores ausentes (normalmente não há no insurance.csv)
    df_clean = df.dropna().copy()
    n_original = df.shape[0]
    n_limpo = df_clean.shape[0]
    print(f"Linhas originais: {n_original} | Linhas após dropna(): {n_limpo}\n")

    # 3.2. One-Hot Encoding para “sex”, “smoker” e “region”
    df_encoded = pd.get_dummies(
        df_clean,
        columns=["sex", "smoker", "region"],
        drop_first=True
    )
    print("Colunas após One-Hot Encoding:")
    print(df_encoded.columns.tolist(), "\n")

    # 3.3. Separar features (X) e target (y)
    X = df_encoded.drop("charges", axis=1)
    y = df_encoded["charges"]

    return X, y

# --- 4. DIVISÃO EM TREINO E TESTE ---
def dividir_treino_teste(X, y, proporcao_teste=0.20, semente=42):
    """
    Divide X e y em conjuntos de treino e teste.
    """
    print("\n=== 4. DIVISÃO EM TREINO E TESTE ===\n")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=proporcao_teste, random_state=semente
    )
    print(f"Dados de Treino: {X_train.shape[0]} linhas")
    print(f"Dados de Teste: {X_test.shape[0]} linhas\n")
    return X_train, X_test, y_train, y_test

# --- 5. CÁLCULO DO VIF (Multicolinearidade) ---
def calcular_vif(X):
    """
    Calcula Variance Inflation Factor (VIF) para detectar multicolinearidade.
    Converte explicitamente para float antes de chamar statsmodels.
    """
    print("\n=== 5. CÁLCULO DE VIF (MULTICOLINEARIDADE) ===\n")

    # Converter todos os preditores para float, garantindo dtype numérico
    X_float = X.astype(float)

    # Adiciona constante (intercepto)
    X_const = sm.add_constant(X_float)

    vif_data = pd.DataFrame({
        "variável": X_const.columns,
        "VIF": [
            variance_inflation_factor(X_const.values, i)
            for i in range(X_const.shape[1])
        ]
    })
    print(vif_data, "\n")
    return vif_data

# --- 6. MODELAGEM: REGRESSÃO LINEAR (Statsmodels OLS) ---
def treinar_modelo_OLS(X_train, y_train):
    """
    Ajusta um modelo de Regressão Linear OLS (statsmodels) nos dados de treino.
    """
    print("\n=== 6. TREINAMENTO DO MODELO (OLS) ===\n")
    # Certificar-se de usar X_train como float também
    X_train_float = X_train.astype(float)
    X_train_sm = sm.add_constant(X_train_float)
    modelo_ols = sm.OLS(y_train, X_train_sm).fit()
    print(modelo_ols.summary(), "\n")
    return modelo_ols

# --- 7. AVALIAÇÃO EM TESTE ---
def avaliar_modelo(modelo_ols, X_test, y_test):
    """
    Gera previsões no conjunto de teste, calcula métricas e gera gráficos de avaliação.
    """
    print("\n=== 7. AVALIAÇÃO DO MODELO NO CONJUNTO DE TESTE ===\n")

    # Converter X_test para float antes de adicionar constante
    X_test_float = X_test.astype(float)
    X_test_sm = sm.add_constant(X_test_float)

    y_pred = modelo_ols.predict(X_test_sm)

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"RMSE: {rmse:.2f}")
    print(f"MAE: {mae:.2f}")
    print(f"R²: {r2:.4f}\n")

    residuos = y_test - y_pred

    # 7.1. Histograma dos resíduos
    plt.figure(figsize=(6, 4))
    sns.histplot(residuos, kde=True)
    plt.title("Histograma dos Resíduos (y_test − y_pred)")
    plt.xlabel("Resíduo")
    plt.ylabel("Frequência")
    plt.tight_layout()
    plt.show()

    # 7.2. Dispersão resíduos vs. valores previstos
    plt.figure(figsize=(6, 4))
    plt.scatter(y_pred, residuos, alpha=0.6)
    plt.axhline(0, color="red", linestyle="--")
    plt.title("Resíduos x Valores Previstos")
    plt.xlabel("Valor Previsto")
    plt.ylabel("Resíduo")
    plt.tight_layout()
    plt.show()

    # 7.3. Gráfico Real × Previsto
    plt.figure(figsize=(6, 6))
    plt.scatter(y_test, y_pred, alpha=0.6)
    minimo = min(y_test.min(), y_pred.min())
    maximo = max(y_test.max(), y_pred.max())
    plt.plot([minimo, maximo], [minimo, maximo], color="red", linestyle="--", linewidth=2)
    plt.xlabel("Valores Reais (y_test)")
    plt.ylabel("Valores Previstos (y_pred)")
    plt.title("Real × Previsto no Conjunto de Teste")
    plt.tight_layout()
    plt.show()

    print("\n=== PROCESSO CONCLUÍDO COM SUCESSO ===\n")

# --- 8. BLOCO PRINCIPAL ---
if __name__ == "__main__":
    # Ajuste o caminho se o CSV estiver em outra pasta
    caminho_csv = "insurance.csv"

    # 1. Carregar e explorar
    df = carregar_e_explorar(caminho_csv=caminho_csv)

    # 2. Visualizações iniciais
    visualizacoes_iniciais(df)

    # 3. Pré-processamento
    X, y = preprocessamento(df)

    # 4. Divisão em treino/teste
    X_train, X_test, y_train, y_test = dividir_treino_teste(X, y)

    # 5. Cálculo de VIF (agora convertendo para float)
    vif_df = calcular_vif(X_train)

    # 6. Treinamento do modelo OLS
    modelo_OLS = treinar_modelo_OLS(X_train, y_train)

    # 7. Avaliação no conjunto de teste
    avaliar_modelo(modelo_OLS, X_test, y_test)
