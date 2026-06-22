"""
Métodos de integração numérica fornecidos no plano de investigação.

"""

import numpy as np
from numpy.polynomial.legendre import leggauss


def ponto_medio(f, a, b, n):
    """Regra do Ponto Médio composta. Erro O(h²)."""
    h = (b - a) / n
    xi = np.linspace(a + h / 2, b - h / 2, n)
    return h * np.sum(f(xi))


def trapezios(f, a, b, n):
    """
    Regra dos Trapézios composta. Erro O(h²).

    Coeficientes: 1, 2, 2, ..., 2, 1.
    """
    xi = np.linspace(a, b, n + 1)
    fi = f(xi)
    h = (b - a) / n

    return h / 2 * (fi[0] + 2 * np.sum(fi[1:-1]) + fi[-1])


def simpson13(f, a, b, n):
    """
    Regra de Simpson 1/3 composta. Erro O(h⁴).

    n deve ser par.
    Coeficientes: 1, 4, 2, 4, ..., 4, 1.
    """
    if n % 2 != 0:
        raise ValueError("n deve ser par para Simpson 1/3")

    xi = np.linspace(a, b, n + 1)
    fi = f(xi)
    h = (b - a) / n

    return h / 3 * (
        fi[0]
        + 4 * np.sum(fi[1:-1:2])
        + 2 * np.sum(fi[2:-2:2])
        + fi[-1]
    )


def trapezios_tabela(xi, fi):
    """
    Regra dos Trapézios para dados tabelados.

    O espaçamento não precisa ser uniforme.
    """
    xi = np.asarray(xi, dtype=float)
    fi = np.asarray(fi, dtype=float)

    return np.sum((fi[:-1] + fi[1:]) * np.diff(xi) / 2)


def simpson13_tabela(xi, fi):
    """Regra de Simpson 1/3 para tabela. n deve ser par."""
    xi = np.asarray(xi, dtype=float)
    fi = np.asarray(fi, dtype=float)

    n = len(fi) - 1
    if n % 2 != 0:
        raise ValueError("n deve ser par")

    h = (xi[-1] - xi[0]) / n

    return h / 3 * (
        fi[0]
        + 4 * np.sum(fi[1:-1:2])
        + 2 * np.sum(fi[2:-2:2])
        + fi[-1]
    )


def cota_trapezio(f2max, a, b, n):
    """Cota superior do erro dos Trapézios compostos."""
    return f2max * (b - a) ** 3 / (12 * n**2)


def cota_simpson(f4max, a, b, n):
    """Cota superior do erro de Simpson 1/3 composto."""
    return f4max * (b - a) ** 5 / (180 * n**4)


def gauss_legendre(f, a, b, n):
    """
    Quadratura de Gauss-Legendre com n pontos.

    Exata para polinômios de grau menor ou igual a 2n - 1.
    """
    t, pesos = leggauss(n)
    x = (b - a) / 2 * t + (b + a) / 2

    return (b - a) / 2 * np.sum(pesos * f(x))


def tabela_comparativa(f, a, b, exato, ns_nc, ns_gauss):
    """
    Gera uma tabela comparando Newton-Cotes e Gauss-Legendre.

    ns_nc: lista de valores de n para Trapézios e Simpson.
    ns_gauss: lista de valores de n para Gauss-Legendre.
    """
    print(f"{'Método':25s} {'n':>5s} {'Resultado':>14s} {'Erro':>12s}")
    print("-" * 60)

    for n in ns_nc:
        resultado = trapezios(f, a, b, n)
        erro = abs(resultado - exato)
        print(f"{'Trapézios':25s} {n:5d} {resultado:14.8f} {erro:12.2e}")

    for n in ns_nc:
        if n % 2 == 0:
            resultado = simpson13(f, a, b, n)
            erro = abs(resultado - exato)
            print(f"{'Simpson 1/3':25s} {n:5d} {resultado:14.8f} {erro:12.2e}")

    for n in ns_gauss:
        resultado = gauss_legendre(f, a, b, n)
        erro = abs(resultado - exato)
        print(f"{'Gauss-Legendre':25s} {n:5d} {resultado:14.8f} {erro:12.2e}")
