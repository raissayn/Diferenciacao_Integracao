"""
main.py
Plano de Investigação Computacional — Diferenciação e Integração Numéricas
Disciplina: Cálculo Numérico — UNIFAL-MG
Alunos: Ana Flávia Freiria Rodrigues, Raissa Nunes Peret
Professora: Angela Leite Moreno

Este script reproduz os experimentos obrigatórios do roteiro, imprime os
resultados no terminal e salva os gráficos em graficosGerados/.
"""

import os
from math import erf, sqrt
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/derivacao_integracao_matplotlib")

import matplotlib
matplotlib.use("Agg")
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
    trapezios,
    trapezios_tabela,
)


np.random.seed(42)

Path("graficosGerados/secao-1").mkdir(parents=True, exist_ok=True)
Path("graficosGerados/secao-2").mkdir(parents=True, exist_ok=True)
Path("graficosGerados/secao-3").mkdir(parents=True, exist_ok=True)
Path("graficosGerados/secao-4").mkdir(parents=True, exist_ok=True)
Path("graficosGerados/secao-5").mkdir(parents=True, exist_ok=True)


#  Estilo global dos gráficos
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "figure.dpi": 130,
})

def fmt(x, casas=10):
    if isinstance(x, str):
        return x
    if abs(x) != 0 and (abs(x) < 1e-4 or abs(x) >= 1e6):
        return f"{x:.{max(casas - 4, 2)}e}"
    return f"{x:.{casas}f}"


def print_tabela(cabecalho, linhas):
    larguras = [
        max(len(str(cabecalho[i])), *(len(str(linha[i])) for linha in linhas))
        for i in range(len(cabecalho))
    ]
    print("  " + " | ".join(str(cabecalho[i]).ljust(larguras[i]) for i in range(len(cabecalho))))
    print("  " + "-+-".join("-" * largura for largura in larguras))
    for linha in linhas:
        print("  " + " | ".join(str(linha[i]).ljust(larguras[i]) for i in range(len(linha))))


def add_tabela(cabecalho, linhas):
    print_tabela(cabecalho, linhas)


def razoes(erros):
    return [erros[i - 1] / erros[i] for i in range(1, len(erros))]


def menor_n_trapezio(f, a, b, exato, tol, limite=200000):
    for n in range(1, limite + 1):
        if abs(trapezios(f, a, b, n) - exato) < tol:
            return n
    raise RuntimeError("Limite excedido.")


def menor_n_simpson(f, a, b, exato, tol, limite=200000):
    for n in range(2, limite + 1, 2):
        if abs(simpson13(f, a, b, n) - exato) < tol:
            return n
    raise RuntimeError("Limite excedido.")


# ===========================================================================
# SEÇÃO 1 — Fórmulas de Diferenças Finitas
# ===========================================================================
print("\n" + "=" * 60)
print("SEÇÃO 1 — Fórmulas de Diferenças Finitas")
print("=" * 60)

# ============================================================
# Q1.1 — Fórmulas de dois pontos para f(x)=sen(x)
# ============================================================
print("\n" + "=" * 60)
print("Q1.1 — Fórmulas de dois pontos para f(x)=sen(x)")
print("=" * 60)
f = np.sin
x0 = np.pi / 3
exato = np.cos(x0)
linhas = []
erros_q11 = {}

for h in [0.1, 0.01]:
    prog = df_progressiva(f, x0, h)
    regr = df_regressiva(f, x0, h)
    cent = df_central(f, x0, h)
    valores = {"Progressiva": prog, "Regressiva": regr, "Central": cent}
    erros_q11[h] = {nome: abs(valor - exato) for nome, valor in valores.items()}

    print(f"\n  h = {h}")
    print(f"    Progressiva = {prog:.10f} | erro = {abs(prog-exato):.2e}")
    print(f"    Regressiva  = {regr:.10f} | erro = {abs(regr-exato):.2e}")
    print(f"    Central     = {cent:.10f} | erro = {abs(cent-exato):.2e}")

    for nome, valor in valores.items():
        linhas.append([h, nome, fmt(valor), fmt(abs(valor - exato), 8), "O(h²)" if nome == "Central" else "O(h)"])

add_tabela(["h", "Fórmula", "Valor aproximado", "Erro", "Ordem"], linhas)

# (a) A tabela acima mostra os valores aproximados e os erros absolutos.
# (b) Ao reduzir h por fator 10, fórmulas O(h) devem reduzir erro por ~10,
#     enquanto fórmulas O(h²) devem reduzir erro por ~100.
# (c) A fórmula central cancela o termo de primeira ordem da expansão de Taylor.

# ============================================================
# Q1.2 — Fórmulas de três pontos
# ============================================================
print("\n" + "=" * 60)
print("Q1.2 — Fórmulas de três pontos")
print("=" * 60)
linhas = []
erros_q12 = {}

for h in [0.1, 0.01]:
    prog3 = df_prog3(f, x0, h)
    retro3 = df_retro3(f, x0, h)
    cent = df_central(f, x0, h)
    valores = {"Progressiva 3 pts": prog3, "Retroativa 3 pts": retro3, "Central": cent}
    erros_q12[h] = {nome: abs(valor - exato) for nome, valor in valores.items()}

    print(f"\n  h = {h}")
    for nome, valor in valores.items():
        print(f"    {nome:18s} = {valor:.10f} | erro = {abs(valor-exato):.2e}")
        linhas.append([h, nome, fmt(valor), fmt(abs(valor - exato), 8)])

add_tabela(["h", "Fórmula", "Valor aproximado", "Erro"], linhas)

# (a) As três aproximações são comparadas na tabela.
# (b) A redução esperada é próxima de 100, pois todas são O(h²).
# (c) A central de "três pontos" usa os mesmos pontos da fórmula central.
fatores = ", ".join(f"{nome}: {erros_q12[0.1][nome] / erros_q12[0.01][nome]:.2f}" for nome in erros_q12[0.1])

# ============================================================
# Q1.3 — Passo ótimo: truncamento vs. arredondamento
# ============================================================
print("\n" + "=" * 60)
print("Q1.3 — Passo ótimo: truncamento vs. arredondamento")
print("=" * 60)
g = np.exp
hs = np.logspace(0, -16, 200)
exato_g = np.exp(1.0)
erros_c = np.abs(df_central(g, 1.0, hs) - exato_g)
erros_p = np.abs(df_progressiva(g, 1.0, hs) - exato_g)
idx_c = int(np.argmin(erros_c))
idx_p = int(np.argmin(erros_p))

linhas = [
    ["Central", fmt(hs[idx_c], 8), fmt(erros_c[idx_c], 8), "ε^(1/3) ≈ 1e-5"],
    ["Progressiva", fmt(hs[idx_p], 8), fmt(erros_p[idx_p], 8), "sqrt(ε) ≈ 1e-8"],
]
add_tabela(["Fórmula", "h ótimo experimental", "Erro mínimo", "Estimativa teórica"], linhas)

fig, ax = plt.subplots(figsize=(8, 4))
ax.loglog(hs, erros_c, "b-", lw=1.7, label="Central O(h²)")
ax.loglog(hs, erros_p, "r--", lw=1.7, label="Progressiva O(h)")
hs_ref = np.logspace(-5, -1, 50)
ax.loglog(hs_ref, 0.5 * hs_ref**2, "k:", lw=1.1, label="ref. O(h²)")
ax.loglog(hs_ref, 0.5 * hs_ref, color="0.45", ls=":", lw=1.1, label="ref. O(h)")
ax.axvline(hs[idx_c], color="b", ls=":", alpha=0.7, label="h ótimo central")
ax.axvline(hs[idx_p], color="r", ls=":", alpha=0.7, label="h ótimo progressiva")
ax.set(title="Q1.3 — Passo ótimo: truncamento vs. arredondamento", xlabel="h", ylabel="Erro absoluto")
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig("graficosGerados/secao-1/q1_3_passo_otimo.png", dpi=150)
plt.close(fig)
print("\n  [Gráfico salvo: graficosGerados/secao-1/q1_3_passo_otimo.png]")

# (a) O erro cai por truncamento e depois sobe por arredondamento.
# (b) O h ótimo central fica próximo da escala ε^(1/3).
# (c) O h ótimo progressivo fica próximo da escala sqrt(ε).
# (d) A central atinge erro mínimo menor porque tem ordem superior.

# ============================================================
# Q1.4 — Diferenciação de tabela experimental
# ============================================================
print("\n" + "=" * 60)
print("Q1.4 — Diferenciação de tabela experimental")
print("=" * 60)
t = np.array([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5])
x = np.array([0.0, 1.2, 4.8, 10.6, 18.5, 27.1, 35.8, 43.6])
h = t[1] - t[0]
v = derivada_tabela(t, x)
a = (x[2:] - 2 * x[1:-1] + x[:-2]) / h**2

print("\n  (a) Velocidades estimadas:")
linhas_v = [[fmt(ti, 2), fmt(xi, 2), fmt(vi, 4)] for ti, xi, vi in zip(t, x, v)]
add_tabela(["t", "x(t)", "v(t) estimada"], linhas_v)

print("\n  (b) Acelerações nos pontos interiores:")
linhas_a = [[fmt(t[i], 2), fmt(a[i - 1], 4)] for i in range(1, len(t) - 1)]
add_tabela(["t", "a(t) estimada"], linhas_a)

sinal = np.where(np.diff(np.sign(a)) != 0)[0]
mudanca = "não houve mudança de sinal"
if len(sinal) > 0:
    mudanca = f"entre t={t[sinal[0] + 1]:.1f}s e t={t[sinal[0] + 2]:.1f}s"

# (c) A frenagem começa quando a aceleração fica negativa.
# (d) A incerteza central é δv ≈ 0,2/h.
# (e) Dados ruidosos não combinam com h muito pequeno.

# ============================================================
# Q1.5 — Segunda derivada de ln(x)
# ============================================================
print("\n" + "=" * 60)
print("Q1.5 — Segunda derivada de ln(x)")
print("=" * 60)
f_ln = np.log
x0 = 2.0
exato_d2 = -0.25
linhas = []
erros_q15 = []

for h in [0.1, 0.05, 0.01]:
    aprox = d2f_central(f_ln, x0, h)
    erro = abs(aprox - exato_d2)
    f4max = 6 / (x0 - h) ** 4
    cota = h**2 / 12 * f4max
    erros_q15.append(erro)
    print(f"\n  h = {h} | f'' ≈ {aprox:.10f} | erro = {erro:.2e} | cota = {cota:.2e}")
    linhas.append([h, fmt(aprox), fmt(erro, 8), fmt(cota, 8)])

add_tabela(["h", "f'' aproximada", "Erro", "Cota teórica"], linhas)

# (a) A aproximação para h=0,1 é comparada com -0,25.
# (b) A cota teórica usa max |f⁽⁴⁾(x)| em [2-h, 2+h].
# (c) O erro cai aproximadamente por fator 4 quando h é dividido por 2.

# ===========================================================================
# SEÇÃO 2 — Newton-Cotes: Ponto Médio, Trapézios e Simpson
# ===========================================================================
print("\n" + "=" * 60)
print("SEÇÃO 2 — Newton-Cotes: Ponto Médio, Trapézios e Simpson")
print("=" * 60)

# ============================================================
# Q2.1 — Verificação das regras em x² e x³
# ============================================================
print("\n" + "=" * 60)
print("Q2.1 — Verificação das regras em x² e x³")
print("=" * 60)
linhas = []
for nome, func, exato_int in [("x²", lambda y: y**2, 1 / 3), ("x³", lambda y: y**3, 1 / 4)]:
    pm = ponto_medio(func, 0, 1, 4)
    tr = trapezios(func, 0, 1, 4)
    sp = simpson13(func, 0, 1, 4)
    print(f"\n  Integral de {nome} em [0,1]")
    print(f"    Ponto Médio : {pm:.10f}")
    print(f"    Trapézios   : {tr:.10f}")
    print(f"    Simpson 1/3 : {sp:.10f}")
    linhas.extend([
        [nome, "Ponto Médio", fmt(pm), fmt(abs(pm - exato_int), 8)],
        [nome, "Trapézios", fmt(tr), fmt(abs(tr - exato_int), 8)],
        [nome, "Simpson 1/3", fmt(sp), fmt(abs(sp - exato_int), 8)],
    ])

add_tabela(["Integral", "Método", "Resultado", "Erro"], linhas)

# (a) Simpson deve ser exato para polinômios até grau 3.
# (b) Os resultados confirmam a expectativa.
# (c) Para x³, Simpson continua exato pela precisão algébrica.

# ============================================================
# Q2.2 — Integral de 1/x em [1,2]
# ============================================================
print("\n" + "=" * 60)
print("Q2.2 — Integral de 1/x em [1,2]")
print("=" * 60)
f_inv = lambda y: 1 / y
exato_ln2 = np.log(2)
linhas = []
erros_t = []
erros_s = []

for n in [4, 8, 16]:
    tr = trapezios(f_inv, 1, 2, n)
    sp = simpson13(f_inv, 1, 2, n)
    erros_t.append(abs(tr - exato_ln2))
    erros_s.append(abs(sp - exato_ln2))
    print(f"\n  n = {n}")
    print(f"    Trapézios: {tr:.10f} | erro = {abs(tr-exato_ln2):.2e}")
    print(f"    Simpson  : {sp:.10f} | erro = {abs(sp-exato_ln2):.2e}")
    linhas.append([n, fmt(tr), fmt(abs(tr - exato_ln2), 8), fmt(sp), fmt(abs(sp - exato_ln2), 8)])

add_tabela(["n", "Trapézios", "Erro T", "Simpson", "Erro S"], linhas)

# (a) Tabela comparativa preenchida.
# (b) Trapézios reduz por ~4 e Simpson por ~16 ao dobrar n.
# (c) Simpson pesa os pontos de modo a capturar melhor a curvatura.

# ============================================================
# Q2.3 — Cotas de erro e n mínimo
# ============================================================
print("\n" + "=" * 60)
print("Q2.3 — Cotas de erro e n mínimo")
print("=" * 60)
tol = 1e-5
n_t_teorico = int(np.ceil(np.sqrt(np.pi**3 / (12 * tol))))
n_t_exp = menor_n_trapezio(np.sin, 0, np.pi, 2.0, tol)
n_s_teorico = int(np.ceil((np.e / (180 * tol)) ** 0.25))
if n_s_teorico % 2:
    n_s_teorico += 1
n_s_exp = menor_n_simpson(np.exp, 0, 1, np.e - 1, tol)

linhas = [
    ["∫₀π sen(x) dx", "Trapézios", n_t_teorico, n_t_exp, fmt(cota_trapezio(1, 0, np.pi, n_t_teorico), 8)],
    ["∫₀¹ exp(x) dx", "Simpson", n_s_teorico, n_s_exp, fmt(cota_simpson(np.e, 0, 1, n_s_teorico), 8)],
]
add_tabela(["Integral", "Método", "n teórico", "n experimental", "Cota"], linhas)

# As cotas garantem precisão, mas geralmente são conservadoras.

# ============================================================
# Q2.4 — Erro log-log para x² sen(x)
# ============================================================
print("\n" + "=" * 60)
print("Q2.4 — Erro log-log para x² sen(x)")
print("=" * 60)
f_q24 = lambda y: y**2 * np.sin(y)
exato_q24 = np.pi**2 - 4
ns = np.array([4, 8, 16, 32])
linhas = []
erros_t_q24 = []
erros_s_q24 = []

for n in ns:
    tr = trapezios(f_q24, 0, np.pi, int(n))
    sp = simpson13(f_q24, 0, np.pi, int(n))
    erros_t_q24.append(abs(tr - exato_q24))
    erros_s_q24.append(abs(sp - exato_q24))
    print(f"\n  n = {n}")
    print(f"    Trapézios: erro = {abs(tr-exato_q24):.2e}")
    print(f"    Simpson  : erro = {abs(sp-exato_q24):.2e}")
    linhas.append([n, fmt(tr), fmt(abs(tr - exato_q24), 8), fmt(sp), fmt(abs(sp - exato_q24), 8)])

add_tabela(["n", "Trapézios", "Erro T", "Simpson", "Erro S"], linhas)

fig, ax = plt.subplots(figsize=(8, 4))
ax.loglog(ns, erros_t_q24, "o-", lw=2, label="Trapézios")
ax.loglog(ns, erros_s_q24, "s-", lw=2, label="Simpson")
ax.loglog(ns, erros_t_q24[0] * (ns / ns[0]) ** -2, "k:", lw=1.2, label="ref. n⁻²")
ax.loglog(ns, erros_s_q24[0] * (ns / ns[0]) ** -4, color="0.45", ls=":", lw=1.2, label="ref. n⁻⁴")
ax.set(title="Q2.4 — Erro em ∫₀π x² sen(x) dx", xlabel="n", ylabel="Erro absoluto")
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig("graficosGerados/secao-2/q2_4_erros_newton_cotes.png", dpi=150)
plt.close(fig)
print("\n  [Gráfico salvo: graficosGerados/secao-2/q2_4_erros_newton_cotes.png]")

alvo_t100 = abs(trapezios(f_q24, 0, np.pi, 100) - exato_q24)
n_s_supera = next(n for n in range(2, 200, 2) if abs(simpson13(f_q24, 0, np.pi, n) - exato_q24) < alvo_t100)


# ============================================================
# Q2.5 — Integração de dados experimentais de potência
# ============================================================
print("\n" + "=" * 60)
print("Q2.5 — Integração de dados experimentais de potência")
print("=" * 60)
tempo = np.arange(0, 5.0, 0.5)
potencia = np.array([0.0, 12.4, 22.8, 30.1, 34.2, 35.0, 32.8, 27.5, 20.3, 12.1])
e_trap = trapezios_tabela(tempo, potencia)
e_misto = simpson13_tabela(tempo[:9], potencia[:9]) + trapezios_tabela(tempo[8:], potencia[8:])

linhas = [
    ["Trapézios tabela", fmt(e_trap)],
    ["Simpson nos 8 primeiros + trapézio final", fmt(e_misto)],
]
add_tabela(["Método", "Energia (J)"], linhas)


# ===========================================================================
# SEÇÃO 3 — Quadratura Gaussiana e Comparação de Métodos
# ===========================================================================
print("\n" + "=" * 60)
print("SEÇÃO 3 — Quadratura Gaussiana e Comparação de Métodos")
print("=" * 60)

# ============================================================
# Q3.1 — Eficiência da Quadratura Gaussiana em 1/x
# ============================================================
print("\n" + "=" * 60)
print("Q3.1 — Eficiência da Quadratura Gaussiana em 1/x")
print("=" * 60)
linhas = []
for n in [2, 4, 8, 16, 32]:
    val = trapezios(f_inv, 1, 2, n)
    linhas.append(["Trapézios", n, n + 1, fmt(val), fmt(abs(val - exato_ln2), 8)])
for n in [2, 4, 8, 16, 32]:
    val = simpson13(f_inv, 1, 2, n)
    linhas.append(["Simpson", n, n + 1, fmt(val), fmt(abs(val - exato_ln2), 8)])
for n in [2, 3, 4, 5, 6]:
    val = gauss_legendre(f_inv, 1, 2, n)
    linhas.append(["Gauss-Legendre", n, n, fmt(val), fmt(abs(val - exato_ln2), 8)])

add_tabela(["Método", "n", "Avaliações", "Resultado", "Erro"], linhas)

erro_gl2 = abs(gauss_legendre(f_inv, 1, 2, 2) - exato_ln2)
erro_s4 = abs(simpson13(f_inv, 1, 2, 4) - exato_ln2)
erro_s32 = abs(simpson13(f_inv, 1, 2, 32) - exato_ln2)
n_gl_supera = next(n for n in range(2, 20) if abs(gauss_legendre(f_inv, 1, 2, n) - exato_ln2) < erro_s32)


# ============================================================
# Q3.2 — Integral de exp(-x²) e erro por custo
# ============================================================
print("\n" + "=" * 60)
print("Q3.2 — Integral de exp(-x²) e erro por custo")
print("=" * 60)
f_exp2 = lambda y: np.exp(-(y**2))
exato_exp2 = sqrt(np.pi) / 2 * erf(1)
linhas = []
dados_plot = {"Trapézios": [], "Simpson": [], "Gauss-Legendre": []}

for n in [2, 4, 8, 16, 32]:
    erro_t = abs(trapezios(f_exp2, 0, 1, n) - exato_exp2)
    erro_s = abs(simpson13(f_exp2, 0, 1, n) - exato_exp2)
    erro_g = abs(gauss_legendre(f_exp2, 0, 1, n) - exato_exp2)
    linhas.append(["Trapézios", n, n + 1, fmt(erro_t, 8)])
    linhas.append(["Simpson", n, n + 1, fmt(erro_s, 8)])
    linhas.append(["Gauss-Legendre", n, n, fmt(erro_g, 8)])
    dados_plot["Trapézios"].append((n + 1, erro_t))
    dados_plot["Simpson"].append((n + 1, erro_s))
    dados_plot["Gauss-Legendre"].append((n, erro_g))

add_tabela(["Método", "n", "Avaliações", "Erro"], linhas)

fig, ax = plt.subplots(figsize=(8, 4))
for nome, pares in dados_plot.items():
    xs, ys = zip(*pares)
    ax.loglog(xs, ys, "o-", lw=2, label=nome)
xs_ref = np.array([3, 33], dtype=float)
ax.loglog(xs_ref, 1.5e-2 * (xs_ref / xs_ref[0]) ** -2, "k:", lw=1.2, label="ref. N⁻²")
ax.loglog(xs_ref, 3.5e-4 * (xs_ref / xs_ref[0]) ** -4, color="0.45", ls=":", lw=1.2, label="ref. N⁻⁴")
ax.set(title="Q3.2 — Erro para ∫₀¹ exp(-x²) dx", xlabel="Avaliações de f", ylabel="Erro absoluto")
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig("graficosGerados/secao-3/q3_2_erro_por_custo.png", dpi=150)
plt.close(fig)
print("\n  [Gráfico salvo: graficosGerados/secao-3/q3_2_erro_por_custo.png]")

tol = 1e-8
avals = {
    "Trapézios": next(n + 1 for n in range(1, 100000) if abs(trapezios(f_exp2, 0, 1, n) - exato_exp2) < tol),
    "Simpson": next(n + 1 for n in range(2, 10000, 2) if abs(simpson13(f_exp2, 0, 1, n) - exato_exp2) < tol),
    "Gauss-Legendre": next(n for n in range(2, 100) if abs(gauss_legendre(f_exp2, 0, 1, n) - exato_exp2) < tol),
}

# ============================================================
# Q3.3 — Função não suave |x−0,5|
# ============================================================
print("\n" + "=" * 60)
print("Q3.3 — Função não suave |x−0,5|")
print("=" * 60)
f_abs = lambda y: np.abs(y - 0.5)
exato_abs = 0.25
linhas = []

for n in [2, 4, 8, 16]:
    linhas.append(["Trapézios", n, fmt(abs(trapezios(f_abs, 0, 1, n) - exato_abs), 8)])
    linhas.append(["Simpson", n, fmt(abs(simpson13(f_abs, 0, 1, n) - exato_abs), 8)])
    linhas.append(["Gauss-Legendre", n, fmt(abs(gauss_legendre(f_abs, 0, 1, n) - exato_abs), 8)])

add_tabela(["Método", "n", "Erro"], linhas)


# ===========================================================================
# SEÇÃO 4 — Análise Comparativa Global
# ===========================================================================
print("\n" + "=" * 60)
print("SEÇÃO 4 — Análise Comparativa Global")
print("=" * 60)

# ============================================================
# Q4.1 — Tabela comparativa global
# ============================================================
print("\n" + "=" * 60)
print("Q4.1 — Tabela comparativa global")
print("=" * 60)
linhas = [
    ["Erro global", "O(h²)", "O(h⁴)", "exata até grau 2n-1", "O(h²)"],
    ["Avaliações de f", "n+1", "n+1", "n", "2 por ponto"],
    ["Exato para grau", "1", "3", "2n-1", "aproxima derivadas"],
    ["Requer n especial?", "não", "n par", "não", "malha ao redor do ponto"],
    ["Funciona com tabela?", "sim", "sim, se n par", "não diretamente", "sim, malha uniforme"],
    ["Melhor cenário", "dados tabelados", "funções suaves/tabelas pares", "funções suaves analíticas", "pontos interiores"],
    ["Pior cenário", "alta curvatura", "n ímpar/descontinuidades", "dados fixos ou não suaves", "dados ruidosos"],
]
add_tabela(["Aspecto", "Trapézios", "Simpson 1/3", "Gauss-Legendre", "Dif. Central"], linhas)


# ============================================================
# Q4.2 — Escolha de método para sinal amostrado
# ============================================================
print("\n" + "=" * 60)
print("Q4.2 — Escolha de método para sinal amostrado")
print("=" * 60)

# ===========================================================================
# SEÇÃO 5 — Projeto Integrador: Cálculo Variacional e Física
# ===========================================================================
print("\n" + "=" * 60)
print("SEÇÃO 5 — Projeto Integrador: Cálculo Variacional e Física")
print("=" * 60)

# ============================================================
# Q5.1 — Comprimento de curva
# ============================================================
print("\n" + "=" * 60)
print("Q5.1 — Comprimento de curva")
print("=" * 60)
exato_l = sqrt(17) + 0.25 * np.log(4 + sqrt(17))
linhas = []
erros_l = []

for n in [10, 20, 40]:
    xs = np.linspace(0, 2, n + 1)
    ys = xs**2
    integrando = lambda y: np.sqrt(1 + (2 * y) ** 2)
    l_analitico = simpson13(integrando, 0, 2, n)
    dy_num = derivada_tabela(xs, ys)
    l_num = simpson13_tabela(xs, np.sqrt(1 + dy_num**2))
    erros_l.append(abs(l_num - exato_l))
    print(f"\n  n = {n} | L analítico = {l_analitico:.10f} | L numérico = {l_num:.10f}")
    linhas.append([n, fmt(l_analitico), fmt(abs(l_analitico - exato_l), 8), fmt(l_num), fmt(abs(l_num - exato_l), 8)])

add_tabela(["n", "L com f' analítica", "Erro", "L com f' numérica", "Erro"], linhas)

fig, ax = plt.subplots(figsize=(8, 4))
ax.loglog(np.array([10, 20, 40]), erros_l, "o-", lw=2, label="Erro com derivada numérica")
ns_l = np.array([10, 20, 40], dtype=float)
ax.loglog(ns_l, erros_l[0] * (ns_l / ns_l[0]) ** -4, "k:", lw=1.2, label="ref. n⁻⁴")
ax.set(title="Q5.1 — Comprimento de curva: erro vs. n", xlabel="n", ylabel="Erro absoluto")
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig("graficosGerados/secao-5/q5_1_comprimento_curva.png", dpi=150)
plt.close(fig)
print("\n  [Gráfico salvo: graficosGerados/secao-5/q5_1_comprimento_curva.png]")


# ============================================================
# Q5.2 — Trabalho de força variável
# ============================================================
print("\n" + "=" * 60)
print("Q5.2 — Trabalho de força variável")
print("=" * 60)
x_forca = np.arange(0, 6.5, 0.5)
forca = np.array([0, 8, 15, 20, 24, 26, 27, 26, 22, 17, 11, 5, 0], dtype=float)
w_t = trapezios_tabela(x_forca, forca)
w_s = simpson13_tabela(x_forca, forca)
dfdx = derivada_tabela(x_forca, forca)
idx_max = int(np.argmax(forca))
idx_var = int(np.argmax(np.abs(dfdx)))
v_final = sqrt(2 * w_s / 2)

linhas = [
    ["W por Trapézios", fmt(w_t)],
    ["W por Simpson", fmt(w_s)],
    ["Força máxima", f"{forca[idx_max]:.2f} N em x={x_forca[idx_max]:.2f} m"],
    ["Maior |F'(x)| estimado", f"{dfdx[idx_var]:.2f} N/m em x={x_forca[idx_var]:.2f} m"],
    ["Velocidade final (m=2 kg)", fmt(v_final)],
]
add_tabela(["Grandeza", "Resultado"], linhas)


# ============================================================
# Q5.3 — Distribuição Normal e probabilidade
# ============================================================
print("\n" + "=" * 60)
print("Q5.3 — Distribuição Normal e probabilidade")
print("=" * 60)
normal = lambda y: np.exp(-(y**2) / 2) / np.sqrt(2 * np.pi)
z_vals = [1.96, 2.58, 3.00]
tabelados = [0.9750, 0.9951, 0.9987]
linhas = []

for z, tab in zip(z_vals, tabelados):
    s = simpson13(normal, -6, z, 100)
    gls = [gauss_legendre(normal, -6, z, n) for n in [5, 10, 20]]
    phi_exata = 0.5 * (1 + erf(z / sqrt(2)))
    erro_s = abs(s - phi_exata)
    melhor_n = next((n for n, gval in zip([5, 10, 20], gls) if abs(gval - phi_exata) < erro_s), "nenhum até 20")
    linhas.append([z, tab, fmt(s), fmt(abs(s - tab), 8), fmt(gls[0]), fmt(gls[1]), fmt(gls[2]), melhor_n])

add_tabela(["x", "Tabela", "Simpson n=100", "Erro S", "GL n=5", "GL n=10", "GL n=20", "n GL supera S"], linhas)

z_grid = np.linspace(1.8, 2.1, 301)
phi_grid = np.array([gauss_legendre(normal, -6, z, 20) for z in z_grid])
z_crit = np.interp(0.975, phi_grid, z_grid)

# ===========================================================================
# SEÇÃO 6 — Desafios Computacionais
# ===========================================================================
print("\n" + "=" * 60)
print("SEÇÃO 6 — Desafios Computacionais")
print("=" * 60)
Path("graficosGerados/secao-6").mkdir(parents=True, exist_ok=True)

# ============================================================
# Q6.1 — Extrapolação de Richardson e tabela de Romberg
# ============================================================
print("\n" + "=" * 60)
print("Q6.1 — Extrapolação de Richardson e tabela de Romberg")
print("=" * 60)


def richardson_trapezio(f, a, b, n):
    t_h = trapezios(f, a, b, n)
    t_h2 = trapezios(f, a, b, 2 * n)
    return (4 * t_h2 - t_h) / 3


def romberg(f, a, b, n_inicial, niveis):
    tabela = np.full((niveis, niveis), np.nan)
    ns_romberg = []

    for i in range(niveis):
        n = n_inicial * 2**i
        ns_romberg.append(n)
        tabela[i, 0] = trapezios(f, a, b, n)

        for j in range(1, i + 1):
            tabela[i, j] = tabela[i, j - 1] + (
                tabela[i, j - 1] - tabela[i - 1, j - 1]
            ) / (4**j - 1)

    return np.array(ns_romberg), tabela


n_base = 2
r_h = richardson_trapezio(f_inv, 1, 2, n_base)
s_equivalente = simpson13(f_inv, 1, 2, 2 * n_base)

linhas = [
    ["Richardson", n_base, 2 * n_base, fmt(r_h), fmt(abs(r_h - exato_ln2), 8)],
    ["Simpson 1/3", "-", 2 * n_base, fmt(s_equivalente), fmt(abs(s_equivalente - exato_ln2), 8)],
    ["Diferença R - S", "-", "-", fmt(abs(r_h - s_equivalente), 8), "-"],
]
add_tabela(["Método", "n em T(h)", "n final", "Resultado", "Erro"], linhas)

ns_romberg, tabela_romberg = romberg(f_inv, 1, 2, 2, 3)
linhas = []
for i, n in enumerate(ns_romberg):
    linha = [fmt(1 / n, 6), n]
    for j in range(3):
        linha.append(fmt(tabela_romberg[i, j]) if j <= i else "-")
    linhas.append(linha)

print("\n  Tabela de Romberg para h = 0,5; 0,25; 0,125:")
add_tabela(["h", "n", "R(i,0)", "R(i,1)", "R(i,2)"], linhas)

tol_romberg = 1e-10
for niveis_romberg in range(1, 15):
    ns_romberg_tol, tabela_romberg_tol = romberg(f_inv, 1, 2, 2, niveis_romberg)
    valor_romberg = tabela_romberg_tol[-1, -1]
    erro_romberg = abs(valor_romberg - exato_ln2)
    if erro_romberg < tol_romberg:
        break

n_final_romberg = int(ns_romberg_tol[-1])
avaliacoes_romberg = n_final_romberg + 1
n_gauss_romberg = next(
    n for n in range(1, 30)
    if abs(gauss_legendre(f_inv, 1, 2, n) - exato_ln2) < tol_romberg
)
valor_gauss_romberg = gauss_legendre(f_inv, 1, 2, n_gauss_romberg)

linhas = [
    ["Romberg", niveis_romberg, avaliacoes_romberg, fmt(valor_romberg), fmt(erro_romberg, 8)],
    ["Gauss-Legendre", n_gauss_romberg, n_gauss_romberg, fmt(valor_gauss_romberg), fmt(abs(valor_gauss_romberg - exato_ln2), 8)],
]
print("\n  Eficiência para erro menor que 1e-10:")
add_tabela(["Método", "Nível/n", "Avaliações de f", "Resultado", "Erro"], linhas)

# ============================================================
# Q6.2 — Integração de Monte Carlo
# ============================================================
print("\n" + "=" * 60)
print("Q6.2 — Integração de Monte Carlo")
print("=" * 60)


def monte_carlo_1d(f, a, b, n_amostras, rng):
    pontos = rng.uniform(a, b, n_amostras)
    return (b - a) * np.mean(f(pontos))


def monte_carlo_2d(f, ax, bx, ay, by, n_amostras, rng):
    x_mc = rng.uniform(ax, bx, n_amostras)
    y_mc = rng.uniform(ay, by, n_amostras)
    return (bx - ax) * (by - ay) * np.mean(f(x_mc, y_mc))


ns_mc = np.array([10**2, 10**3, 10**4, 10**5], dtype=int)
repeticoes_mc = 20
rng_mc_1d = np.random.default_rng(42)
erros_medios_mc = []
desvios_erros_mc = []
medias_estimativas_mc = []
linhas = []

for n_mc in ns_mc:
    estimativas = np.array([
        monte_carlo_1d(f_exp2, 0, 1, int(n_mc), rng_mc_1d)
        for _ in range(repeticoes_mc)
    ])
    erros = np.abs(estimativas - exato_exp2)
    media_erro = float(np.mean(erros))
    desvio_erro = float(np.std(erros, ddof=1))
    media_estimativa = float(np.mean(estimativas))
    erros_medios_mc.append(media_erro)
    desvios_erros_mc.append(desvio_erro)
    medias_estimativas_mc.append(media_estimativa)
    linhas.append([
        int(n_mc),
        fmt(media_estimativa),
        fmt(media_erro, 8),
        fmt(desvio_erro, 8),
    ])

add_tabela(["N", "Estimativa média", "Erro absoluto médio", "Desvio dos erros"], linhas)

erros_medios_mc = np.array(erros_medios_mc)
inclinacao_mc = np.polyfit(np.log10(ns_mc), np.log10(erros_medios_mc), 1)[0]

fig, ax = plt.subplots(figsize=(8, 4))
ax.loglog(ns_mc, erros_medios_mc, "o-", lw=2, label="Erro médio — Monte Carlo")
ax.loglog(
    ns_mc,
    erros_medios_mc[0] * (ns_mc / ns_mc[0]) ** -0.5,
    "k:",
    lw=1.3,
    label="referência N⁻¹ᐟ²",
)
ax.set(
    title="Q6.2 — Monte Carlo em ∫₀¹ exp(-x²) dx",
    xlabel="Número de amostras N",
    ylabel="Erro absoluto médio (20 execuções)",
)
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig("graficosGerados/secao-6/q6_2_monte_carlo_1d.png", dpi=150)
plt.close(fig)
print("\n  [Gráfico salvo: graficosGerados/secao-6/q6_2_monte_carlo_1d.png]")
print(f"  Inclinação experimental no gráfico log-log: {inclinacao_mc:.4f}")

segundo_momento = sqrt(np.pi) / (2 * sqrt(2)) * erf(sqrt(2))
desvio_integrando = sqrt(segundo_momento - exato_exp2**2)
constante_erro_medio = desvio_integrando * sqrt(2 / np.pi)
tol_mc = 1e-4
n_mc_estimado = int(np.ceil((constante_erro_medio / tol_mc) ** 2))
n_gauss_1e4 = next(
    n for n in range(1, 30)
    if abs(gauss_legendre(f_exp2, 0, 1, n) - exato_exp2) < tol_mc
)
dimensao_cruzamento = int(np.floor(np.log(n_mc_estimado) / np.log(n_gauss_1e4))) + 1

linhas = [
    ["Monte Carlo", n_mc_estimado, n_mc_estimado, "estimativa assintótica"],
    ["Gauss-Legendre 1D", n_gauss_1e4, n_gauss_1e4, "erro verificado"],
    ["Gauss-Legendre tensorial", f"d = {dimensao_cruzamento}", n_gauss_1e4**dimensao_cruzamento, "primeiro custo acima do MC"],
]
print("\n  Custo estimado para erro menor que 1e-4:")
add_tabela(["Método", "n/dimensão", "Avaliações", "Critério"], linhas)

f_exp2_2d = lambda x_mc, y_mc: np.exp(-(x_mc**2 + y_mc**2))
exato_exp2_2d = exato_exp2**2
rng_mc_2d = np.random.default_rng(2026)
erros_medios_mc_2d = []
linhas_mc_2d = []

for n_mc in ns_mc:
    estimativas = np.array([
        monte_carlo_2d(f_exp2_2d, 0, 1, 0, 1, int(n_mc), rng_mc_2d)
        for _ in range(repeticoes_mc)
    ])
    erros = np.abs(estimativas - exato_exp2_2d)
    erro_medio = float(np.mean(erros))
    erros_medios_mc_2d.append(erro_medio)
    linhas_mc_2d.append([
        "Monte Carlo",
        int(n_mc),
        int(n_mc),
        fmt(np.mean(estimativas)),
        fmt(erro_medio, 8),
    ])

erros_gauss_2d = []
avaliacoes_gauss_2d = []
for n_gauss_2d in [2, 3, 4, 5, 6]:
    valor_gauss_2d = gauss_legendre(f_exp2, 0, 1, n_gauss_2d) ** 2
    erro_gauss_2d = abs(valor_gauss_2d - exato_exp2_2d)
    avaliacoes = n_gauss_2d**2
    erros_gauss_2d.append(max(erro_gauss_2d, np.finfo(float).eps))
    avaliacoes_gauss_2d.append(avaliacoes)
    linhas_mc_2d.append([
        "Gauss tensorial",
        n_gauss_2d,
        avaliacoes,
        fmt(valor_gauss_2d),
        fmt(erro_gauss_2d, 8),
    ])

print("\n  Integral bidimensional em [0,1] × [0,1]:")
add_tabela(["Método", "N/n", "Avaliações", "Resultado", "Erro"], linhas_mc_2d)

fig, ax = plt.subplots(figsize=(8, 4))
ax.loglog(ns_mc, erros_medios_mc_2d, "o-", lw=2, label="Monte Carlo 2D")
ax.loglog(avaliacoes_gauss_2d, erros_gauss_2d, "s-", lw=2, label="Gauss-Legendre tensorial")
ax.set(
    title="Q6.2 — Comparação em duas dimensões",
    xlabel="Avaliações do integrando",
    ylabel="Erro absoluto",
)
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig("graficosGerados/secao-6/q6_2_comparacao_2d.png", dpi=150)
plt.close(fig)
print("  [Gráfico salvo: graficosGerados/secao-6/q6_2_comparacao_2d.png]")

# ============================================================
# Q6.3 — Gradient check por diferenças centrais
# ============================================================
print("\n" + "=" * 60)
print("Q6.3 — Gradient check por diferenças centrais")
print("=" * 60)

rng_grad = np.random.default_rng(2026)
x_grad = rng_grad.normal(size=(20, 3))
theta = rng_grad.normal(size=3)
theta_referencia = rng_grad.normal(size=3)
y_grad = x_grad @ theta_referencia + 0.05 * rng_grad.normal(size=20)


def perda_quadratica(theta_atual):
    residuos = x_grad @ theta_atual - y_grad
    return np.sum(residuos**2)


def gradiente_numerico(theta_atual, epsilon):
    grad = np.zeros_like(theta_atual, dtype=float)

    for i in range(len(theta_atual)):
        def perda_coordenada(valor, indice=i):
            theta_teste = theta_atual.copy()
            theta_teste[indice] = valor
            return perda_quadratica(theta_teste)

        grad[i] = df_central(perda_coordenada, theta_atual[i], epsilon)

    return grad


grad_analitico = 2 * x_grad.T @ (x_grad @ theta - y_grad)
epsilon_grad = 1e-5
grad_numerico = gradiente_numerico(theta, epsilon_grad)
diferenca_relativa = np.linalg.norm(grad_analitico - grad_numerico) / np.linalg.norm(grad_analitico)

linhas = []
for i in range(3):
    linhas.append([
        i,
        fmt(theta[i]),
        fmt(grad_analitico[i]),
        fmt(grad_numerico[i]),
        fmt(abs(grad_analitico[i] - grad_numerico[i]), 8),
    ])

add_tabela(["i", "θᵢ", "Gradiente analítico", "Gradiente numérico", "Diferença"], linhas)
print(f"\n  Diferença relativa = {diferenca_relativa:.6e}")
print(f"  Gradient check: {'APROVADO' if diferenca_relativa < 1e-5 else 'REPROVADO'}")

epsilons_grad = np.logspace(-1, -16, 100)
erros_grad = []
for epsilon_teste in epsilons_grad:
    grad_teste = gradiente_numerico(theta, epsilon_teste)
    erro_relativo = np.linalg.norm(grad_analitico - grad_teste) / np.linalg.norm(grad_analitico)
    erros_grad.append(max(float(erro_relativo), np.finfo(float).eps))

erros_grad = np.array(erros_grad)
idx_melhor_epsilon = int(np.argmin(erros_grad))

linhas = []
for epsilon_teste in [1e-1, 1e-3, 1e-5, 1e-7, 1e-9, 1e-11, 1e-13, 1e-15]:
    grad_teste = gradiente_numerico(theta, epsilon_teste)
    erro_relativo = np.linalg.norm(grad_analitico - grad_teste) / np.linalg.norm(grad_analitico)
    linhas.append([fmt(epsilon_teste, 8), fmt(erro_relativo, 8)])

print("\n  Sensibilidade do gradient check ao valor de ε:")
add_tabela(["ε", "Diferença relativa"], linhas)
print(
    f"\n  Melhor ε no intervalo testado = {epsilons_grad[idx_melhor_epsilon]:.6e} "
    f"| diferença relativa = {erros_grad[idx_melhor_epsilon]:.6e}"
)

fig, ax = plt.subplots(figsize=(8, 4))
ax.loglog(epsilons_grad, erros_grad, lw=2, label="Diferença relativa")
ax.axvline(epsilon_grad, color="0.35", ls=":", label="ε = 1e-5")
ax.set(
    title="Q6.3 — Sensibilidade do gradient check",
    xlabel="ε",
    ylabel="Diferença relativa entre gradientes",
)
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig("graficosGerados/secao-6/q6_3_gradient_check.png", dpi=150)
plt.close(fig)
print("  [Gráfico salvo: graficosGerados/secao-6/q6_3_gradient_check.png]")



# ===========================================================================
# GRÁFICOS GERADOS
# ===========================================================================

print("\n" + "=" * 60)
print("Concluído.")
print("Gráficos salvos em: graficosGerados/")
print("=" * 60)
