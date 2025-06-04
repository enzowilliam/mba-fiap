base de dados insurance.csv retirada de: https://www.kaggle.com/datasets/mirichoi0218/insurance?resource=download

=== 1. EXPLORAÇÃO INICIAL DOS DADOS ===

Primeiras 5 linhas do DataFrame:
   age     sex     bmi  children smoker     region      charges
0   19  female  27.900         0    yes  southwest  16884.92400
1   18    male  33.770         1     no  southeast   1725.55230
2   28    male  33.000         3     no  southeast   4449.46200
3   33    male  22.705         0     no  northwest  21984.47061
4   32    male  28.880         0     no  northwest   3866.85520 

Número de linhas: 1338, Número de colunas: 7

Tipos de cada coluna:
age           int64
sex          object
bmi         float64
children      int64
smoker       object
region       object
charges     float64
dtype: object 

Estatísticas descritivas das colunas numéricas:
               age          bmi     children       charges
count  1338.000000  1338.000000  1338.000000   1338.000000
mean     39.207025    30.663397     1.094918  13270.422265
std      14.049960     6.098187     1.205493  12110.011237
min      18.000000    15.960000     0.000000   1121.873900
25%      27.000000    26.296250     0.000000   4740.287150
50%      39.000000    30.400000     1.000000   9382.033000
75%      51.000000    34.693750     2.000000  16639.912515
max      64.000000    53.130000     5.000000  63770.428010 

Contagem de valores ausentes por coluna:
age         0
sex         0
bmi         0
children    0
smoker      0
region      0
charges     0
dtype: int64 


=== 2. VISUALIZAÇÕES INICIAIS ===

2025-06-03 21:25:13.944 Python[7918:14822449] +[IMKClient subclass]: chose IMKClient_Modern
2025-06-03 21:25:13.945 Python[7918:14822449] +[IMKInputSession subclass]: chose IMKInputSession_Modern

=== 3. PRÉ-PROCESSAMENTO DE DADOS ===

Linhas originais: 1338 | Linhas após dropna(): 1338

Colunas após One-Hot Encoding:
['age', 'bmi', 'children', 'charges', 'sex_male', 'smoker_yes', 'region_northwest', 'region_southeast', 'region_southwest'] 


=== 4. DIVISÃO EM TREINO E TESTE ===

Dados de Treino: 1070 linhas
Dados de Teste: 268 linhas


=== 5. CÁLCULO DE VIF (MULTICOLINEARIDADE) ===

           variável        VIF
0             const  35.353322
1               age   1.023084
2               bmi   1.094986
3          children   1.005643
4          sex_male   1.006303
5        smoker_yes   1.011703
6  region_northwest   1.493159
7  region_southeast   1.613285
8  region_southwest   1.515246 


=== 6. TREINAMENTO DO MODELO (OLS) ===

                            OLS Regression Results                            
==============================================================================
Dep. Variable:                charges   R-squared:                       0.742
Model:                            OLS   Adj. R-squared:                  0.740
Method:                 Least Squares   F-statistic:                     380.9
Date:                Tue, 03 Jun 2025   Prob (F-statistic):          1.32e-305
Time:                        21:25:47   Log-Likelihood:                -10845.
No. Observations:                1070   AIC:                         2.171e+04
Df Residuals:                    1061   BIC:                         2.175e+04
Df Model:                           8                                         
Covariance Type:            nonrobust                                         
====================================================================================
                       coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------
const            -1.193e+04   1114.505    -10.705      0.000   -1.41e+04   -9744.335
age                256.9757     13.477     19.067      0.000     230.530     283.421
bmi                337.0926     32.471     10.381      0.000     273.378     400.807
children           425.2788    154.655      2.750      0.006     121.814     728.743
sex_male           -18.5917    376.175     -0.049      0.961    -756.722     719.539
smoker_yes        2.365e+04    466.505     50.699      0.000    2.27e+04    2.46e+04
region_northwest  -370.6773    536.873     -0.690      0.490   -1424.130     682.776
region_southeast  -657.8643    539.791     -1.219      0.223   -1717.043     401.314
region_southwest  -809.7994    535.208     -1.513      0.131   -1859.986     240.387
==============================================================================
Omnibus:                      252.330   Durbin-Watson:                   2.085
Prob(Omnibus):                  0.000   Jarque-Bera (JB):              613.798
Skew:                           1.253   Prob(JB):                    5.19e-134
Kurtosis:                       5.737   Cond. No.                         310.
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified. 


=== 7. AVALIAÇÃO DO MODELO NO CONJUNTO DE TESTE ===

RMSE: 5796.28
MAE: 4181.19
R²: 0.7836


=== PROCESSO CONCLUÍDO COM SUCESSO ===
