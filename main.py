"""
main.py

Plano de Investigação:
Diferenciação e Integração Numéricas — Análise, Comparação e Aplicações em Python.
Disciplina: Cálculo Numérico — UNIFAL-MG
Professora: Angela Leite Moreno
Alunos: Ana Flávia Freiria Rodrigues, Raissa Nunes Peret


Este arquivo será usado posteriormente para executar os experimentos,
gerar tabelas, produzir gráficos e responder às questões do trabalho.
"""

import matplotlib.pyplot as plt
import numpy as np

from diferencas import (
    d2f_central,
    derivada_tabela,
    df_central,
    df_prog3,
    df_progressiva,
    df_regressiva,
    df_retro3,
)
from integracao import (
    cota_simpson,
    cota_trapezio,
    gauss_legendre,
    ponto_medio,
    simpson13,
    simpson13_tabela,
    tabela_comparativa,
    trapezios,
    trapezios_tabela,
)


np.random.seed(42)
plt.rcParams.update({"font.size": 11, "figure.dpi": 120})


def main():
    """Ponto de entrada da investigação."""

    # TODO: Seção 1 — Fórmulas de Diferenças Finitas
    # Q1.1
    # Q1.2
    # Q1.3
    # Q1.4
    # Q1.5

    # TODO: Seção 2 — Newton-Cotes: Trapézios e Simpson
    # Q2.1
    # Q2.2
    # Q2.3
    # Q2.4
    # Q2.5

    # TODO: Seção 3 — Quadratura Gaussiana e comparação
    # Q3.1
    # Q3.2
    # Q3.3

    # TODO: Seção 4 — Análise comparativa global
    # Q4.1
    # Q4.2

    # TODO: Seção 5 — Projeto integrador
    # Q5.1
    # Q5.2
    # Q5.3

    # TODO opcional: Seção 6 — Desafios
    # Q6.1
    # Q6.2
    # Q6.3

    pass


if __name__ == "__main__":
    main()
