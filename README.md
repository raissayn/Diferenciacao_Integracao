# Diferenciação e Integração Numéricas

Atividade de investigação computacional da disciplina de **Cálculo Numérico** — UNIFAL-MG.

**Tema:** análise, comparação e aplicação de métodos numéricos para diferenciação e integração.

## Objetivo

Este projeto implementa e executa os experimentos das seções obrigatórias do roteiro:

- fórmulas de diferenças finitas progressiva, regressiva e central;
- segunda derivada numérica;
- diferenciação de dados tabelados;
- regras do Ponto Médio, Trapézios e Simpson 1/3;
- cotas de erro e determinação experimental de subintervalos;
- Quadratura de Gauss-Legendre;
- comparação global entre métodos;
- aplicações em comprimento de curva, trabalho de força variável e distribuição normal.

## Estrutura do Projeto

```text
Derivacao_Integracao/
├── diferencas.py
├── integracao.py
├── main.py
├── requirements.txt
├── README.md
├── graficosGerados/
│   ├── secao-1/
│   ├── secao-2/
│   ├── secao-3/
│   └── secao-5/
│   └── secao-6/
└── relatorio/
```

## Arquivos Principais

- `diferencas.py`: implementa as fórmulas de diferenças finitas fornecidas no roteiro.
- `integracao.py`: implementa Ponto Médio, Trapézios, Simpson 1/3, integração por tabela, cotas de erro e Gauss-Legendre.
- `main.py`: executa os experimentos, imprime tabelas/resultados no terminal e gera os gráficos.
- `graficosGerados/`: contém as figuras geradas em formato `.png` para uso no relatório.
- `requirements.txt`: lista as dependências necessárias para executar o projeto.

## Dependências

O projeto utiliza:

- `numpy`
- `matplotlib`
- `scipy`

## Preparação do Ambiente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Execução

Para executar todos os experimentos:

```bash
python3 main.py
```

A execução imprime os resultados no terminal e salva os gráficos em:

```text
graficosGerados/
```

## Gráficos Gerados

Os principais gráficos produzidos são:

- `graficosGerados/secao-1/q1_3_passo_otimo.png`
- `graficosGerados/secao-2/q2_4_erros_newton_cotes.png`
- `graficosGerados/secao-3/q3_2_erro_por_custo.png`
- `graficosGerados/secao-5/q5_1_comprimento_curva.png`
- `graficosGerados/secao-6/q6_2_comparacao_2d.png`
- `graficosGerados/secao-6/q6_2_monte_carlo_1d.png`
- `graficosGerados/secao-6/q6_3_gradient_check`