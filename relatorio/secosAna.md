
# Resultados — Diferenciação e Integração Numéricas

Texto escrito separadamente a partir dos resultados executados em `main.py`, para servir de base ao relatório em LaTeX. O arquivo `main.py` apenas executa os códigos, imprime os resultados e gera os gráficos.

# ===========================================================================
# CONFERÊNCIA DOS CÓDIGOS-BASE
# ===========================================================================

Os arquivos `diferencas.py` e `integracao.py` conferem com os blocos fornecidos no PDF da atividade. As diferenças observadas são apenas de estilo e organização: nomes de variáveis mais descritivos, acentuação nas docstrings e inclusão das funções de cota e de Gauss-Legendre no mesmo arquivo `integracao.py`, como o roteiro solicita. As fórmulas implementadas são as mesmas do enunciado.

# ===========================================================================
# SEÇÃO 1 — Fórmulas de Diferenças Finitas
# ===========================================================================

# ============================================================
# Q1.1 — Fórmulas de dois pontos para f(x)=sen(x)
# ============================================================

Valor exato usado: \(f'(\pi/3)=\cos(\pi/3)=0,5\).

## (a) Tabela com h = 0,1

| Fórmula | Valor aproximado | Erro absoluto | Ordem esperada |
| --- | --- | --- | --- |
| Progressiva | 0.4559018854 | 0.04409811 | O(h) |
| Regressiva | 0.5424322811 | 0.04243228 | O(h) |
| Central | 0.4991670832 | 0.00083292 | O(h²) |

Com \(h=0,1\), a fórmula central foi muito mais precisa que as fórmulas progressiva e regressiva. Isso acontece porque ela usa pontos simétricos em torno de \(x_0\), o que cancela o termo principal de erro de primeira ordem. As fórmulas progressiva e regressiva usam informação de apenas um lado do ponto, por isso mantêm erro dominante proporcional a \(h\).

## (b) Repetição com h = 0,01 e fatores de redução

| Fórmula | Valor aproximado | Erro absoluto | Fator de redução do erro |
| --- | --- | --- | --- |
| Progressiva | 0.4956615758 | 0.00433842 | 10.16 |
| Regressiva | 0.5043217576 | 0.00432176 | 9.82 |
| Central | 0.4999916667 | 8.3333e-06 | 99.95 |

Ao reduzir \(h\) de 0,1 para 0,01, o passo foi dividido por 10. As fórmulas de ordem \(O(h)\) tiveram redução de erro próxima de 10, enquanto a fórmula central, de ordem \(O(h^2)\), teve redução próxima de 100. Portanto, o comportamento observado confirma a ordem teórica de cada fórmula.

## (c) Por que a fórmula central tem erro O(h²)?

A fórmula central tem erro \(O(h^2)\) porque é construída de forma simétrica:

\[
\frac{f(x+h)-f(x-h)}{2h}.
\]

Ao expandir \(f(x+h)\) e \(f(x-h)\) em série de Taylor, os termos pares e ímpares se combinam de modo que o erro de primeira ordem se cancela. Assim, mesmo usando apenas dois pontos ao redor de \(x_0\), a aproximação fica com erro dominante de segunda ordem. A vantagem não vem da quantidade de pontos, mas da simetria da fórmula.

# ============================================================
# Q1.2 — Fórmulas de três pontos
# ============================================================

## (a) Tabela com df_prog3, df_retro3 e df_central

| h | Fórmula | Valor aproximado | Erro absoluto |
| --- | --- | --- | --- |
| 0.1 | Progressiva 3 pts | 0.5014446937 | 0.00144469 |
| 0.1 | Retroativa 3 pts | 0.5018769853 | 0.00187699 |
| 0.1 | Central | 0.4991670832 | 0.00083292 |
| 0.01 | Progressiva 3 pts | 0.5000164496 | 1.6450e-05 |
| 0.01 | Retroativa 3 pts | 0.5000168826 | 1.6883e-05 |
| 0.01 | Central | 0.4999916667 | 8.3333e-06 |

Todas as fórmulas de três pontos apresentaram erro menor que as fórmulas progressiva e regressiva simples da questão anterior. Isso ocorre porque o ponto adicional permite cancelar termos de erro de ordem mais baixa.

## (b) Fatores de redução do erro

Ao reduzir \(h\) de 0,1 para 0,01, os fatores de redução foram:

| Fórmula | Fator de redução |
| --- | --- |
| Progressiva 3 pts | 87.83 |
| Retroativa 3 pts | 111.18 |
| Central | 99.95 |

Como as três fórmulas têm erro de ordem \(O(h^2)\), esperava-se uma redução próxima de 100. Os valores observados ficam em torno desse comportamento. As pequenas diferenças em relação a 100 aparecem porque o erro real também depende da função avaliada, do ponto escolhido e de termos de ordem superior.

## (c) Por que a central de três pontos produz o mesmo resultado que a central de dois pontos?

A chamada “central de três pontos” usa os valores \(f(x-h)\), \(f(x)\) e \(f(x+h)\), mas a fórmula da primeira derivada central é:

\[
\frac{f(x+h)-f(x-h)}{2h}.
\]

O valor \(f(x)\) não aparece no numerador. Por isso, na prática, ela coincide com a fórmula central usual de dois pontos ao redor de \(x_0\). A diferença está apenas na forma de classificar a fórmula dentro do conjunto de pontos da malha.

# ============================================================
# Q1.3 — Passo ótimo: truncamento vs. arredondamento
# ============================================================

## (a) Comportamento do erro em escala log-log

O gráfico foi gerado em:

`graficosGerados/secao-1/q1_3_passo_otimo.png`

No gráfico, o erro inicialmente diminui quando \(h\) diminui. Essa primeira região é dominada pelo erro de truncamento: quanto menor o passo, melhor a aproximação da derivada. Porém, depois de certo ponto, o erro volta a crescer. Esse crescimento ocorre porque valores muito próximos de \(f(x+h)\) e \(f(x-h)\) passam a ser subtraídos, amplificando erros de arredondamento da máquina.

Portanto, o experimento mostra que não basta escolher \(h\) cada vez menor. Existe um equilíbrio entre erro de truncamento e erro de arredondamento.

## (b) Passo ótimo da fórmula central

| Fórmula | h ótimo experimental | Erro mínimo | Estimativa teórica |
| --- | --- | --- | --- |
| Central | 1.6258e-06 | 1.4344e-13 | \(\varepsilon^{1/3}\approx 10^{-5}\) |

O valor experimental ficou na mesma ordem de grandeza da estimativa teórica. A diferença exata é esperada, pois a estimativa \(h_{opt}\approx\varepsilon^{1/3}\) ignora constantes que dependem da função e do ponto analisado.

## (c) Passo ótimo da fórmula progressiva

| Fórmula | h ótimo experimental | Erro mínimo | Estimativa teórica |
| --- | --- | --- | --- |
| Progressiva | 9.1159e-09 | 5.1880e-10 | \(\sqrt{\varepsilon}\approx 10^{-8}\) |

O \(h_{opt}\) da progressiva foi menor que o da central e ficou próximo da estimativa \(\sqrt{\varepsilon}\). Isso é coerente com a teoria, pois a progressiva tem erro de truncamento de ordem menor e precisa de um passo menor para equilibrar truncamento e arredondamento.

## (d) Comparação do erro mínimo

A fórmula central atingiu erro mínimo aproximadamente 3616.82 vezes menor que a progressiva. Isso confirma a vantagem prática de uma fórmula de ordem mais alta: além de convergir mais rapidamente na região dominada por truncamento, ela também alcança uma precisão mínima melhor antes que o arredondamento passe a dominar.

# ============================================================
# Q1.4 — Diferenciação de tabela experimental
# ============================================================

## (a) Estimativa da velocidade

| t (s) | x(t) (m) | v(t) estimada (m/s) |
| --- | --- | --- |
| 0.00 | 0.00 | 0.0000 |
| 0.50 | 1.20 | 4.8000 |
| 1.00 | 4.80 | 9.4000 |
| 1.50 | 10.60 | 13.7000 |
| 2.00 | 18.50 | 16.5000 |
| 2.50 | 27.10 | 17.3000 |
| 3.00 | 35.80 | 16.5000 |
| 3.50 | 43.60 | 14.7000 |

A velocidade cresce até aproximadamente \(t=2,5s\), atingindo cerca de 17,3 m/s. Depois disso, a velocidade estimada começa a diminuir.

## (b) Estimativa da aceleração nos pontos interiores

| t (s) | a(t) estimada (m/s²) |
| --- | --- |
| 0.50 | 9.6000 |
| 1.00 | 8.8000 |
| 1.50 | 8.4000 |
| 2.00 | 2.8000 |
| 2.50 | 0.4000 |
| 3.00 | -3.6000 |

A aceleração começa positiva e diminui ao longo do tempo. No último ponto interior calculado, ela já aparece negativa.

## (c) O veículo freia? Onde a aceleração muda de sinal?

Sim. O veículo passa a apresentar frenagem quando a aceleração fica negativa. Pela tabela, a mudança de sinal ocorre entre \(t=2,5s\) e \(t=3,0s\). A interpretação física é que o veículo ainda estava aumentando a velocidade até perto de 2,5s, mas depois começou a perder aceleração e entrar em regime de desaceleração.

## (d) Incerteza na velocidade estimada

Os dados de posição têm erro de \(\pm 0,1m\). Para a fórmula central, a incerteza aproximada é:

\[
\delta v \approx \frac{0,2}{h}.
\]

Como \(h=0,5s\):

\[
\delta v \approx \frac{0,2}{0,5}=0,40m/s.
\]

Essa incerteza não é desprezível, principalmente quando se comparam variações pequenas entre velocidades consecutivas.

## (e) Faz sentido usar h muito pequeno em dados ruidosos?

Não. Em diferenciação numérica, ruídos nos dados são amplificados. Se \(h\) for muito pequeno, pequenas imprecisões de medição podem produzir grandes oscilações na derivada estimada. Por isso, com dados experimentais, não se deve buscar apenas o menor passo possível; é preciso equilibrar resolução temporal e sensibilidade ao ruído.

# ============================================================
# Q1.5 — Segunda derivada de ln(x)
# ============================================================

## (a) Estimativa de \(f''(2)\) com h = 0,1

Valor exato:

\[
f''(2)=-\frac{1}{4}=-0,25.
\]

Com \(h=0,1\), obteve-se:

| h | f'' aproximada | Erro |
| --- | --- | --- |
| 0.1 | -0.2503130218 | 0.00031302 |

A aproximação ficou muito próxima do valor exato, com erro da ordem de \(10^{-4}\).

## (b) Cota teórica e comparação com o erro real

Para \(f(x)=\ln(x)\), tem-se:

\[
f^{(4)}(x)=\frac{6}{x^4}.
\]

No intervalo \([1,9,2,1]\), o maior valor ocorre próximo de \(x=1,9\). A cota calculada para \(h=0,1\) foi:

| h | Erro real | Cota teórica |
| --- | --- | --- |
| 0.1 | 0.00031302 | 0.00038367 |

A cota ficou acima do erro real, como esperado. Ela é uma garantia de erro máximo, não uma previsão exata do erro observado.

## (c) Repetição com h = 0,05 e h = 0,01

| h | f'' aproximada | Erro | Cota teórica |
| --- | --- | --- | --- |
| 0.1 | -0.2503130218 | 0.00031302 | 0.00038367 |
| 0.05 | -0.2500781576 | 7.8158e-05 | 8.6451e-05 |
| 0.01 | -0.2500031251 | 3.1251e-06 | 3.1883e-06 |

Ao reduzir \(h\) de 0,1 para 0,05, o erro foi dividido por aproximadamente 4,01, o que confirma o comportamento \(O(h^2)\). A redução de \(h=0,05\) para \(h=0,01\) é ainda maior porque o passo foi dividido por 5.

# ===========================================================================
# SEÇÃO 2 — Newton-Cotes: Ponto Médio, Trapézios e Simpson
# ===========================================================================

# ============================================================
# Q2.1 — Verificação das regras em x² e x³
# ============================================================

## (a) Expectativa antes do cálculo

Para a integral de \(x^2\) em \([0,1]\), espera-se que Simpson seja exato, pois a regra de Simpson 1/3 tem grau de exatidão 3. Assim, ela integra exatamente polinômios de grau até 3. Ponto Médio e Trapézios não possuem essa mesma precisão algébrica para polinômios quadráticos e cúbicos.

## (b) Resultados para \(\int_0^1 x^2 dx = 1/3\)

| Método | Resultado | Erro |
| --- | --- | --- |
| Ponto Médio | 0.3281250000 | 0.00520833 |
| Trapézios | 0.3437500000 | 0.01041667 |
| Simpson 1/3 | 0.3333333333 | 0.00000000 |

Os resultados confirmam a expectativa: Simpson foi exato para \(x^2\), enquanto Ponto Médio e Trapézios apresentaram erro.

## (c) Resultados para \(\int_0^1 x^3 dx = 1/4\)

| Método | Resultado | Erro |
| --- | --- | --- |
| Ponto Médio | 0.2421875000 | 0.00781250 |
| Trapézios | 0.2656250000 | 0.01562500 |
| Simpson 1/3 | 0.2500000000 | 0.00000000 |

Simpson continua sendo exato para \(x^3\), pois cúbicas ainda estão dentro do grau de exatidão da regra. Esse teste confirma que o desempenho de uma regra de integração depende não apenas de \(n\), mas também do grau do polinômio que ela integra exatamente.

# ============================================================
# Q2.2 — Integral de 1/x em [1,2]
# ============================================================

## (a) Tabela comparativa

Valor exato usado:

\[
\int_1^2 \frac{1}{x}dx=\ln(2)\approx0,693147.
\]

| n | Trapézios | Erro T | Simpson | Erro S |
| --- | --- | --- | --- | --- |
| 4 | 0.6970238095 | 0.00387663 | 0.6932539683 | 0.00010679 |
| 8 | 0.6941218504 | 0.00097467 | 0.6931545307 | 7.3501e-06 |
| 16 | 0.6933912022 | 0.00024402 | 0.6931476528 | 4.7226e-07 |

## (b) Fatores de redução ao dobrar n

| Método | Fatores observados |
| --- | --- |
| Trapézios | 3.98 e 3.99 |
| Simpson | 14.53 e 15.56 |

Ao dobrar \(n\), o passo \(h\) é dividido por 2. Como Trapézios tem erro \(O(h^2)\), o erro deve cair por um fator próximo de \(2^2=4\). Simpson tem erro \(O(h^4)\), então a queda esperada é próxima de \(2^4=16\). Os resultados estão de acordo com a teoria.

## (c) Comparação com n = 4

Com \(n=4\), Simpson foi aproximadamente 36,30 vezes mais preciso que Trapézios. Ambos usam 5 pontos de avaliação, mas Simpson combina esses pontos com pesos que capturam melhor a curvatura da função. Por isso, com o mesmo número de pontos, Simpson entrega precisão muito maior.

# ============================================================
# Q2.3 — Cotas de erro e n mínimo
# ============================================================

## (a) \(\int_0^\pi \sin(x)dx=2\) por Trapézios

| Método | n teórico | n experimental | Cota no n teórico |
| --- | --- | --- | --- |
| Trapézios | 509 | 406 | 9.9732e-06 |

A cota teórica exigiu \(n=509\), enquanto o menor \(n\) experimental que atingiu o erro pedido foi 406. A diferença indica que a cota é conservadora.

## (b) \(\int_0^1 e^x dx=e-1\) por Simpson

| Método | n teórico | n experimental | Cota no n teórico |
| --- | --- | --- | --- |
| Simpson | 8 | 6 | 3.6869e-06 |

Também neste caso, o \(n\) teórico foi maior que o experimental. Isso ocorre porque a cota usa o máximo da derivada de quarta ordem no intervalo e garante a precisão para o pior caso.

## Discussão sobre a discrepância

A discrepância entre \(n\) teórico e \(n\) experimental não é um problema do método. Ela mostra que cotas de erro são ferramentas de garantia: servem para assegurar que o erro ficará abaixo de uma tolerância, mas geralmente superestimam o erro real. Na prática, quando é possível testar numericamente, o número de subintervalos necessário pode ser menor.

# ============================================================
# Q2.4 — Erro log-log para \(x^2\sin(x)\)
# ============================================================

## (a) Tabela e gráfico dos erros

Gráfico gerado:

`graficosGerados/secao-2/q2_4_erros_newton_cotes.png`

| n | Trapézios | Erro T | Simpson | Erro S |
| --- | --- | --- | --- | --- |
| 4 | 5.3636342456 | 0.50597016 | 5.8595841325 | 0.01002027 |
| 8 | 5.7428437029 | 0.12676070 | 5.8692468553 | 0.00035755 |
| 16 | 5.8379001678 | 0.03170423 | 5.8695856560 | 1.8745e-05 |
| 32 | 5.8616775047 | 0.00792690 | 5.8696032837 | 1.1174e-06 |

No gráfico log-log, o erro dos Trapézios segue comportamento próximo de inclinação \(-2\), enquanto Simpson se aproxima de inclinação \(-4\), especialmente conforme \(n\) aumenta.

## (b) Fatores de redução ao dobrar n

| Método | Fatores observados |
| --- | --- |
| Trapézios | 3.99, 4.00, 4.00 |
| Simpson | 28.03, 19.07, 16.78 |

Trapézios se comporta praticamente como o esperado para erro \(O(n^{-2})\). Simpson tende ao fator 16, compatível com erro \(O(n^{-4})\), mas nos primeiros refinamentos apresenta fatores maiores por influência das constantes e termos superiores do erro.

## (c) Comparação de Simpson com Trapézios n = 100

Simpson supera a precisão dos Trapézios com \(n=100\) já com \(n=8\), usando apenas 9 avaliações de função. Trapézios com \(n=100\) usa 101 avaliações. Isso mostra que um método de ordem maior pode ser muito mais eficiente do que simplesmente aumentar muito a quantidade de subintervalos em um método de ordem menor.

# ============================================================
# Q2.5 — Integração de dados experimentais de potência
# ============================================================

## (a) Energia por Trapézios

| Método | Energia (J) |
| --- | --- |
| Trapézios tabela | 110.5750000000 |

## (b) Simpson com número ímpar de subintervalos

Como há 10 pontos, existem 9 subintervalos. Simpson 1/3 composto exige número par de subintervalos, então ele não pode ser aplicado diretamente em todo o intervalo. A solução usada foi aplicar Simpson nos 8 primeiros subintervalos e Trapézios no último.

| Método | Energia (J) |
| --- | --- |
| Simpson nos 8 primeiros + trapézio final | 111.4166666667 |

## (c) Qual estimativa é mais confiável?

A estimativa mista é mais confiável na parte suave dos dados, porque Simpson tem ordem maior. Porém, como o último intervalo precisa ser tratado por Trapézios, o método final continua dependendo da qualidade dos dados experimentais. A diferença entre as estimativas foi:

\[
111,4167 - 110,5750 \approx 0,8417J.
\]

Essa diferença dá uma noção do erro numérico, mas não deve ser interpretada como erro total.

## (d) Limitação por método numérico ou por incerteza dos dados?

Com erro de medição de \(\pm0,5W\), a incerteza acumulada nos dados ao longo do intervalo é da ordem de joules. Portanto, exigir precisão de \(\pm0,1J\) não é realista apenas escolhendo uma regra numérica melhor. A limitação principal vem da incerteza experimental, não do método de integração.

# ===========================================================================
# SEÇÃO 3 — Quadratura Gaussiana e Comparação de Métodos
# ===========================================================================

# ============================================================
# Q3.1 — Eficiência da Quadratura Gaussiana em 1/x
# ============================================================

## Resultados comparativos

| Método | n | Avaliações | Resultado | Erro |
| --- | --- | --- | --- | --- |
| Trapézios | 2 | 3 | 0.7083333333 | 0.01518615 |
| Trapézios | 4 | 5 | 0.6970238095 | 0.00387663 |
| Trapézios | 8 | 9 | 0.6941218504 | 0.00097467 |
| Trapézios | 16 | 17 | 0.6933912022 | 0.00024402 |
| Trapézios | 32 | 33 | 0.6932082083 | 6.1028e-05 |
| Simpson | 2 | 3 | 0.6944444444 | 0.00129726 |
| Simpson | 4 | 5 | 0.6932539683 | 0.00010679 |
| Simpson | 8 | 9 | 0.6931545307 | 7.3501e-06 |
| Simpson | 16 | 17 | 0.6931476528 | 4.7226e-07 |
| Simpson | 32 | 33 | 0.6931472103 | 2.9730e-08 |
| Gauss-Legendre | 2 | 2 | 0.6923076923 | 0.00083949 |
| Gauss-Legendre | 3 | 3 | 0.6931216931 | 2.5487e-05 |
| Gauss-Legendre | 4 | 4 | 0.6931464174 | 7.6311e-07 |
| Gauss-Legendre | 5 | 5 | 0.6931471579 | 2.2707e-08 |
| Gauss-Legendre | 6 | 6 | 0.6931471799 | 6.7342e-10 |

## (a) Gauss-Legendre n = 2 é mais preciso que Simpson n = 4?

Não. Gauss-Legendre com \(n=2\) teve erro \(8,3949\times10^{-4}\), enquanto Simpson com \(n=4\) teve erro \(1,0679\times10^{-4}\). Portanto, neste caso, Simpson com 5 avaliações foi mais preciso que Gauss-Legendre com 2 avaliações.

## (b) Quantos pontos de Gauss-Legendre superam Simpson n = 32?

Simpson com \(n=32\) teve erro \(2,9730\times10^{-8}\). Gauss-Legendre superou esse erro com \(n=5\), usando apenas 5 avaliações da função. Esse resultado mostra a eficiência da escolha otimizada dos nós gaussianos.

## (c) Por que Gauss-Legendre converge mais rápido?

A Quadratura de Gauss-Legendre com \(n\) pontos integra exatamente polinômios de grau até \(2n-1\). Isso é mais eficiente do que Newton-Cotes com nós igualmente espaçados, pois os nós gaussianos são escolhidos para maximizar a precisão algébrica. Para funções suaves, essa escolha otimizada produz erro muito pequeno com poucas avaliações.

# ============================================================
# Q3.2 — Integral de exp(-x²) e erro por custo
# ============================================================

## (a) Aplicação dos métodos

| Método | n | Avaliações | Erro |
| --- | --- | --- | --- |
| Trapézios | 2 | 3 | 0.01545388 |
| Simpson | 2 | 3 | 0.00035630 |
| Gauss-Legendre | 2 | 2 | 0.00022944 |
| Trapézios | 4 | 5 | 0.00384004 |
| Simpson | 4 | 5 | 3.1247e-05 |
| Gauss-Legendre | 4 | 4 | 3.3532e-07 |
| Trapézios | 8 | 9 | 0.00095852 |
| Simpson | 8 | 9 | 1.9877e-06 |
| Gauss-Legendre | 8 | 8 | 6.5503e-15 |
| Trapézios | 16 | 17 | 0.00023954 |
| Simpson | 16 | 17 | 1.2462e-07 |
| Gauss-Legendre | 16 | 16 | 0.00000000 |
| Trapézios | 32 | 33 | 5.9878e-05 |
| Simpson | 32 | 33 | 7.7946e-09 |
| Gauss-Legendre | 32 | 32 | 0.00000000 |

## (b) Gráfico erro vs. número de avaliações

Gráfico gerado:

`graficosGerados/secao-3/q3_2_erro_por_custo.png`

O gráfico mostra que Gauss-Legendre tem a melhor relação precisão por custo. Com poucas avaliações, seu erro cai muito mais rapidamente que o dos métodos compostos de Newton-Cotes.

## (c) Método com menos avaliações para erro < 10⁻⁸

| Método | Avaliações necessárias |
| --- | --- |
| Trapézios | 2478 |
| Simpson | 33 |
| Gauss-Legendre | 5 |

Gauss-Legendre foi o método mais eficiente, atingindo erro menor que \(10^{-8}\) com apenas 5 avaliações.

## (d) Por que o gráfico de Gauss-Legendre não é uma reta log-log?

Trapézios e Simpson têm erros que seguem potências de \(h\), por isso aparecem aproximadamente como retas em escala log-log. Já Gauss-Legendre, para funções analíticas suaves, pode apresentar convergência muito mais rápida, próxima de exponencial. Assim, sua curva não precisa seguir uma inclinação fixa no gráfico log-log.

# ============================================================
# Q3.3 — Função não suave |x−0,5|
# ============================================================

## (a) Erros calculados

| Método | n | Erro |
| --- | --- | --- |
| Trapézios | 2 | 0.00000000 |
| Simpson | 2 | 0.08333333 |
| Gauss-Legendre | 2 | 0.03867513 |
| Trapézios | 4 | 0.00000000 |
| Simpson | 4 | 0.00000000 |
| Gauss-Legendre | 4 | 0.01063371 |
| Trapézios | 8 | 0.00000000 |
| Simpson | 8 | 0.00000000 |
| Gauss-Legendre | 8 | 0.00288202 |
| Trapézios | 16 | 0.00000000 |
| Simpson | 16 | 0.00000000 |
| Gauss-Legendre | 16 | 0.00075776 |

## (b) Qual método converge mais rápido? Isso contradiz o caso anterior?

Neste exemplo, Trapézios e Simpson têm desempenho melhor que Gauss-Legendre para vários valores de \(n\). Isso não contradiz a questão anterior, porque a função \(|x-0,5|\) não é suave: ela possui uma quina em \(x=0,5\). A alta eficiência de Gauss-Legendre depende fortemente da suavidade do integrando.

## (c) Por que a taxa de Gauss-Legendre cai?

Gauss-Legendre aproxima muito bem funções suaves por meio da escolha ótima de nós e pesos. Quando a função tem uma não suavidade, a aproximação polinomial global perde eficiência. Além disso, os nós gaussianos não estão necessariamente alinhados com o ponto da quina, então o método não captura perfeitamente a mudança de inclinação.

## (d) Lição prática

O experimento mostra que a escolha do método deve considerar a regularidade da função. Métodos de alta ordem podem perder eficiência em funções não suaves, enquanto métodos mais simples podem funcionar muito bem quando a malha representa adequadamente a estrutura do problema.

# ===========================================================================
# SEÇÃO 4 — Análise Comparativa Global
# ===========================================================================

# ============================================================
# Q4.1 — Tabela comparativa global
# ============================================================

| Aspecto | Trapézios | Simpson 1/3 | Gauss-Legendre | Dif. Central |
| --- | --- | --- | --- | --- |
| Erro global | O(h²) | O(h⁴) | exata até grau 2n-1 | O(h²) |
| Avaliações de f | n+1 | n+1 | n | 2 por ponto |
| Exato para grau | 1 | 3 | 2n-1 | aproxima derivadas |
| Requer n especial? | não | n par | não | malha ao redor do ponto |
| Funciona com tabela? | sim | sim, se n par | não diretamente | sim, malha uniforme |
| Melhor cenário | dados tabelados | funções suaves/tabelas pares | funções suaves analíticas | pontos interiores |
| Pior cenário | alta curvatura | n ímpar/descontinuidades | dados fixos ou não suaves | dados ruidosos |

# ============================================================
# Q4.2 — Escolha de método para sinal amostrado
# ============================================================

## (a) Qual proposta é viável? Qual tem problema conceitual?

As propostas A e B são viáveis. O sinal tem 201 pontos, portanto 200 subintervalos, e Simpson 1/3 pode ser aplicado porque 200 é par. A proposta C tem problema conceitual: Gauss-Legendre com \(n=5\) exige avaliar a função em cinco nós específicos, mas os dados experimentais só estão disponíveis nos pontos amostrados.

## (b) Qual método recomendar?

Para dados experimentais suaves, recomenda-se Simpson 1/3 usando todos os 200 subintervalos, pois ele tem ordem maior que Trapézios e aproveita a malha disponível. Se houver ruído considerável, Trapézios pode ser mais robusto por não introduzir pesos alternados tão fortes.

## (c) E se o sinal tiver descontinuidades?

Se houver descontinuidades ou chaveamento elétrico, a recomendação muda. Nesse caso, Trapézios tende a ser mais seguro, especialmente se os pontos de amostragem capturam as transições. Simpson pode sofrer mais com oscilações ou suavizações artificiais, pois presume maior regularidade da função.

# ===========================================================================
# SEÇÃO 5 — Projeto Integrador: Cálculo Variacional e Física
# ===========================================================================

# ============================================================
# Q5.1 — Comprimento de curva
# ============================================================

## (a) Derivação analítica com n = 10

Foi usado \(f(x)=x^2\), então \(f'(x)=2x\). O comprimento foi calculado por Simpson em:

\[
L=\int_0^2\sqrt{1+(2x)^2}\,dx.
\]

| n | L com f' analítica | Erro |
| --- | --- | --- |
| 10 | 4.6467907645 | 7.0020e-06 |

O valor exato coerente com \(f(x)=x^2\) em \([0,2]\) é:

\[
L=\sqrt{17}+\frac{1}{4}\ln(4+\sqrt{17}).
\]

## (b) Derivada numérica a partir dos valores da malha

| n | L com f' numérica | Erro |
| --- | --- | --- |
| 10 | 4.6467907645 | 7.0020e-06 |

Neste caso, o resultado com derivada numérica coincidiu com o resultado usando derivada analítica. Isso acontece porque a função é quadrática e as fórmulas de diferença usadas capturam exatamente a derivada desse tipo de polinômio na malha.

## (c) O erro do passo (b) é maior?

Não neste experimento. Em geral, a diferenciação numérica introduz erro adicional, mas aqui a escolha de uma parábola torna o caso especialmente favorável. Para funções menos regulares ou dados experimentais ruidosos, o erro da derivada numérica poderia aumentar o erro final do comprimento.

## (d) Repetição com n = 20 e n = 40

| n | L com f' analítica | Erro | L com f' numérica | Erro |
| --- | --- | --- | --- | --- |
| 10 | 4.6467907645 | 7.0020e-06 | 4.6467907645 | 7.0020e-06 |
| 20 | 4.6467837189 | 4.3501e-08 | 4.6467837189 | 4.3501e-08 |
| 40 | 4.6467837596 | 2.7939e-09 | 4.6467837596 | 2.7939e-09 |

Gráfico gerado:

`graficosGerados/secao-5/q5_1_comprimento_curva.png`

O erro cai rapidamente com o aumento de \(n\). Os fatores de redução observados foram 160,96 e 15,57. O primeiro fator é maior que o padrão assintótico porque ainda há influência de termos superiores; depois, o comportamento se aproxima do esperado para Simpson.

# ============================================================
# Q5.2 — Trabalho de força variável
# ============================================================

## (a) Trabalho por Trapézios e Simpson

| Método | Trabalho (J) |
| --- | --- |
| Trapézios | 100.5000000000 |
| Simpson 1/3 | 101.0000000000 |

A diferença entre os métodos é pequena em relação ao valor total do trabalho, sugerindo que a tabela de força descreve uma curva relativamente suave.

## (b) Ponto de força máxima

A força máxima observada foi:

\[
F_{max}=27N \quad \text{em} \quad x=3,0m.
\]

A derivada tabelada ajuda a identificar onde a força deixa de crescer e começa a diminuir. O máximo está no ponto em que a tendência muda de crescimento para decrescimento.

## (c) Onde a força cresce ou decresce mais rapidamente?

A maior magnitude estimada para \(F'(x)\) foi:

\[
17,00N/m \quad \text{em} \quad x=0,00m.
\]

Isso indica crescimento mais rápido no início do trilho. Depois do máximo, a força passa a decrescer de forma mais intensa na parte final do percurso. Como derivadas numéricas em tabela são sensíveis a espaçamento e ruído, essa leitura deve ser interpretada como tendência aproximada.

## (d) Velocidade final para massa de 2 kg

Usando o trabalho calculado por Simpson:

\[
W=\Delta KE=\frac{1}{2}mv^2.
\]

Com \(W=101J\) e \(m=2kg\):

\[
v=\sqrt{\frac{2W}{m}}=\sqrt{101}\approx 10,0499m/s.
\]

# ============================================================
# Q5.3 — Distribuição Normal e probabilidade
# ============================================================

## (a) Simpson 1/3 com n = 100

| x | Valor tabelado | Simpson n=100 | Erro em relação à tabela |
| --- | --- | --- | --- |
| 1.96 | 0.9750 | 0.9750020822 | 2.0822e-06 |
| 2.58 | 0.9951 | 0.9950599426 | 4.0057e-05 |
| 3.00 | 0.9987 | 0.9986500719 | 4.9928e-05 |

Os valores obtidos por Simpson ficam muito próximos dos valores tabelados. As pequenas diferenças também refletem o arredondamento dos valores de tabela.

## (b) Gauss-Legendre com n = 5, 10 e 20

| x | GL n=5 | GL n=10 | GL n=20 | n que supera Simpson |
| --- | --- | --- | --- | --- |
| 1.96 | 0.9786370720 | 0.9749978791 | 0.9750021039 | 20 |
| 2.58 | 0.9479814446 | 0.9949852579 | 0.9950599833 | 20 |
| 3.00 | 0.9084485442 | 0.9985427722 | 0.9986501010 | 20 |

Com \(n=20\), Gauss-Legendre supera Simpson com \(n=100\) nos três valores testados. Isso mostra que, para uma função suave como a densidade normal, a quadratura gaussiana é muito eficiente quando se aumenta o número de nós.

## (c) A cauda da distribuição dificulta a integração?

A cauda poderia dificultar se fosse necessário integrar até \(-\infty\). Porém, truncar o intervalo em \(-6\) é adequado porque a densidade normal já é praticamente nula nessa região. Assim, o erro introduzido pela substituição de \(-\infty\) por \(-6\) é desprezível para a precisão desejada.

## (d) Estimativa do valor crítico

A interpolação inversa usando os valores calculados forneceu:

\[
z_{0,025}\approx 1,95996.
\]

Esse valor é praticamente igual ao valor crítico usual \(1,96\) para teste bicaudal com \(\alpha=5\%\). Portanto, a integração numérica reproduziu corretamente a probabilidade acumulada necessária para o teste de hipótese.

# ===========================================================================
# CONCLUSÃO GERAL
# ===========================================================================

Os experimentos confirmam que a escolha de um método numérico depende de três fatores principais: ordem de convergência, custo computacional e natureza dos dados. Nas fórmulas de diferenciação, as diferenças centrais se destacaram por cancelar termos de erro de primeira ordem, mas também ficou claro que reduzir \(h\) indefinidamente não é uma estratégia segura por causa do erro de arredondamento.

Em integração, Simpson apresentou grande ganho sobre Trapézios para funções suaves, enquanto Gauss-Legendre foi o método mais eficiente quando a função podia ser avaliada livremente em nós otimizados. Por outro lado, os testes com dados experimentais mostram uma limitação prática importante: quando a informação vem de uma tabela, não podemos escolher novos pontos nem diminuir \(h\) arbitrariamente.

Assim, não existe um método universalmente melhor. O método adequado é aquele compatível com a regularidade da função, a forma dos dados disponíveis, o custo das avaliações e a precisão realmente necessária.

# ===========================================================================
# GRÁFICOS GERADOS
# ===========================================================================

- `graficosGerados/secao-1/q1_3_passo_otimo.png`
- `graficosGerados/secao-2/q2_4_erros_newton_cotes.png`
- `graficosGerados/secao-3/q3_2_erro_por_custo.png`
- `graficosGerados/secao-5/q5_1_comprimento_curva.png`

Os desafios opcionais da Seção 6 não foram incluídos porque o PDF os marca como pontuação extra.
