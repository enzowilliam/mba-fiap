# Análise de Seguros de Saúde - Modelo de Regressão Linear


## 📊 Visão Geral dos Dados

### Dataset
- **Fonte**: https://www.kaggle.com/datasets/mirichoi0218/insurance?resource=download
- **Total de registros**: 1.338 observações
- **Variáveis**: 7 colunas (6 preditoras + 1 variável alvo)
- **Dados ausentes**: Nenhum valor faltante detectado

### Variáveis do Dataset
| Variável | Tipo | Descrição |
|----------|------|-----------|
| `age` | Numérica | Idade do segurado |
| `sex` | Categórica | Sexo (male/female) |
| `bmi` | Numérica | Índice de Massa Corporal |
| `children` | Numérica | Número de filhos dependentes |
| `smoker` | Categórica | Status de fumante (yes/no) |
| `region` | Categórica | Região geográfica (northwest, southeast, southwest, northeast) |
| `charges` | Numérica | **Variável alvo** - Custos do seguro de saúde |

## 📈 Estatísticas Descritivas

### Variáveis Numéricas
| Estatística | Idade | BMI | Filhos | Custos (USD) |
|-------------|--------|-----|--------|--------------|
| **Média** | 39.2 anos | 30.7 | 1.1 | $13,270.42 |
| **Mediana** | 39.0 anos | 30.4 | 1.0 | $9,382.03 |
| **Desvio Padrão** | 14.0 anos | 6.1 | 1.2 | $12,110.01 |
| **Mínimo** | 18 anos | 16.0 | 0 | $1,121.87 |
| **Máximo** | 64 anos | 53.1 | 5 | $63,770.43 |

## 🔧 Pré-processamento

### Transformações Realizadas
1. **Codificação One-Hot** para variáveis categóricas
2. **Divisão dos dados**: 80% treino (1.070 obs.) / 20% teste (268 obs.)
3. **Análise de multicolinearidade** usando Variance Inflation Factor (VIF)

### Variáveis Finais do Modelo
- `age` - Idade
- `bmi` - Índice de Massa Corporal
- `children` - Número de filhos
- `sex_male` - Sexo masculino (dummy)
- `smoker_yes` - Fumante (dummy)
- `region_northwest` - Região noroeste (dummy)
- `region_southeast` - Região sudeste (dummy)
- `region_southwest` - Região sudoeste (dummy)

## 📊 Análise de Multicolinearidade (VIF)

| Variável | VIF |
|----------|-----|
| age | 1.02 |
| bmi | 1.09 |
| children | 1.01 |
| sex_male | 1.01 |
| smoker_yes | 1.01 |
| region_northwest | 1.49 |
| region_southeast | 1.61 |
| region_southwest | 1.52 |

> **Nota**: Todos os valores de VIF estão abaixo de 5, indicando ausência de multicolinearidade significativa.

## 🎯 Resultados do Modelo

### Performance Geral
- **R² (Coeficiente de Determinação)**: 0.742
- **R² Ajustado**: 0.740
- **F-statistic**: 380.9 (p < 0.001)

### Coeficientes Significativos

| Variável | Coeficiente | p-valor | Interpretação |
|----------|-------------|---------|---------------|
| **age** | +$256.98 | < 0.001 | Cada ano adicional aumenta o custo em ~$257 |
| **bmi** | +$337.09 | < 0.001 | Cada ponto de BMI adicional aumenta o custo em ~$337 |
| **children** | +$425.28 | 0.006 | Cada filho adicional aumenta o custo em ~$425 |
| **smoker_yes** | +$23,650 | < 0.001 | **Fumantes pagam ~$23,650 a mais** |

### Variáveis Não Significativas
- **sex_male**: Não há diferença significativa entre sexos (p = 0.961)
- **Regiões**: Nenhuma região apresentou diferença significativa nos custos

## 📏 Avaliação no Conjunto de Teste

### Métricas de Performance
- **RMSE (Root Mean Square Error)**: $5,796.28
- **MAE (Mean Absolute Error)**: $4,181.19
- **R² no teste**: 0.7836

## 🔍 Principais Insights

### 1. **Impacto do Tabagismo** 🚬
- Fumantes pagam aproximadamente **$23,650 a mais** em seguros
- Esta é, de longe, a variável mais impactante no modelo

### 2. **Fatores Demográficos** 👥
- **Idade**: Cada ano adicional representa +$257 no custo
- **BMI**: Obesidade tem impacto significativo (+$337 por ponto)
- **Filhos**: Cada dependente adicional custa +$425

### 3. **Fatores Sem Impacto Significativo** ❌
- **Sexo**: Não influencia significativamente os custos
- **Região geográfica**: Sem diferenças estatisticamente significativas

## 📋 Qualidade do Modelo

### Pontos Fortes
- ✅ **Alta capacidade explicativa**: R² = 74.2%
- ✅ **Baixa multicolinearidade**: Todos VIF < 2
- ✅ **Boa generalização**: R² teste (78.4%) > R² treino (74.2%)
- ✅ **Variáveis estatisticamente significativas**

### Considerações
- 📊 **Distribuição residual**: Indica possível não-normalidade (Jarque-Bera significativo)
- 🎯 **Erro médio**: RMSE de ~$5,796 é razoável considerando a faixa de valores

## 🛠️ Tecnologias Utilizadas

- **Python** - Linguagem principal
- **Pandas** - Manipulação de dados
- **Statsmodels** - Modelagem estatística (OLS)
- **Scikit-learn** - Divisão de dados e métricas
- **Matplotlib/Seaborn** - Visualizações

## 📝 Conclusões

Este modelo de regressão linear múltipla demonstra que:

1. **O tabagismo é o fator mais crítico** para determinar custos de seguro de saúde
2. **Idade, BMI e número de filhos** são preditores secundários importantes
3. **Sexo e região geográfica** não influenciam significativamente os custos
4. **O modelo explaining 74.2% da variabilidade** nos custos, indicando boa performance
