"""
Fórmulas de diferenças finitas fornecidas no plano de investigação.

"""

import numpy as np


# Fórmulas de dois pontos (ordem 1)
def df_progressiva(f, x, h):
    """Diferença progressiva: [f(x+h) - f(x)] / h. Erro O(h)."""
    return (f(x + h) - f(x)) / h


def df_regressiva(f, x, h):
    """Diferença regressiva: [f(x) - f(x-h)] / h. Erro O(h)."""
    return (f(x) - f(x - h)) / h


def df_central(f, x, h):
    """Diferença central: [f(x+h) - f(x-h)] / (2h). Erro O(h²)."""
    return (f(x + h) - f(x - h)) / (2 * h)


# Fórmulas de três pontos (ordem 2)
def df_prog3(f, x, h):
    """
    Progressiva de 3 pontos:
    [-3f(x) + 4f(x+h) - f(x+2h)] / (2h).
    Erro O(h²).
    """
    return (-3 * f(x) + 4 * f(x + h) - f(x + 2 * h)) / (2 * h)


def df_retro3(f, x, h):
    """
    Retroativa de 3 pontos:
    [f(x-2h) - 4f(x-h) + 3f(x)] / (2h).
    Erro O(h²).
    """
    return (f(x - 2 * h) - 4 * f(x - h) + 3 * f(x)) / (2 * h)


# Segunda derivada (ordem 2)
def d2f_central(f, x, h):
    """
    Segunda derivada central:
    [f(x-h) - 2f(x) + f(x+h)] / h².
    Erro O(h²).
    """
    return (f(x - h) - 2 * f(x) + f(x + h)) / h**2


# Derivada de tabela de pontos
def derivada_tabela(xi, fi):
    """
    Calcula f'(x_k) para todos os pontos de uma tabela.

    Interior: fórmula central, O(h²).
    Bordas: fórmulas de 3 pontos de segunda ordem.
    """
    xi = np.asarray(xi, dtype=float)
    fi = np.asarray(fi, dtype=float)

    n = len(xi)
    h = xi[1] - xi[0]
    df = np.zeros(n)

    # Borda esquerda: progressiva de segunda ordem
    df[0] = (-3 * fi[0] + 4 * fi[1] - fi[2]) / (2 * h)

    # Interior: central de 3 pontos
    df[1:-1] = (fi[2:] - fi[:-2]) / (2 * h)

    # Borda direita: retroativa de segunda ordem
    df[-1] = (fi[-3] - 4 * fi[-2] + 3 * fi[-1]) / (2 * h)

    return df
