"""Gera figuras/karnaugh.png, figuras/circuito_original.png e figuras/circuito_simplificado.png.

Uso: .venv/Scripts/python build/figuras.py
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402
import schemdraw  # noqa: E402
from schemdraw.parsing import logicparse  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(RAIZ, "figuras")
GRAY = ["00", "01", "11", "10"]

# Expressões com parênteses explícitos para que cada porta tenha no máximo 2 entradas
ORIGINAL = ("((((A and B) and (not C)) and (not D)) or (((A and B) and (not C)) and D))"
            " or (((A and B) and C) and D)")
SIMPLIFICADO = "(A and B) and ((not C) or D)"


def karnaugh(mintermos):
    fig, ax = plt.subplots(figsize=(6.2, 5.2), dpi=200)
    ax.set_xlim(-1.2, 4.2)
    ax.set_ylim(-0.4, 6.7)
    ax.invert_yaxis()
    ax.axis("off")
    for i, ab in enumerate(GRAY):
        ax.text(-0.35, i + 1.5, ab, ha="center", va="center", fontsize=13, family="monospace")
        for j, cd in enumerate(GRAY):
            m = int(ab + cd, 2)
            v = int(m in mintermos)
            ax.add_patch(plt.Rectangle((j, i + 1), 1, 1, fill=False, lw=1.2))
            ax.text(j + 0.5, i + 1.5, str(v), ha="center", va="center", fontsize=18,
                    weight="bold" if v else "normal")
            ax.text(j + 0.06, i + 1.08, f"m{m}", ha="left", va="top", fontsize=7, color="#666")
    for j, cd in enumerate(GRAY):
        ax.text(j + 0.5, 0.7, cd, ha="center", va="center", fontsize=13, family="monospace")
    ax.text(-0.35, 0.7, "AB \\ CD", ha="center", va="center", fontsize=11)
    # grupos na linha AB = 11 (índice 2): m12+m13 (colunas 0-1) e m13+m15 (colunas 1-2)
    ax.add_patch(FancyBboxPatch((0.08, 3.24), 1.84, 0.66, boxstyle="round,pad=0,rounding_size=0.3",
                                fill=False, ec="#1f6fd1", lw=2.4))
    ax.add_patch(FancyBboxPatch((1.14, 3.31), 1.78, 0.48, boxstyle="round,pad=0,rounding_size=0.25",
                                fill=False, ec="#d1491f", lw=2.4, ls="--"))
    ax.text(1.5, 5.45, "Grupo 1: m12 + m13 → ABC'", color="#1f6fd1", ha="center", fontsize=10)
    ax.text(1.5, 5.85, "Grupo 2: m13 + m15 → ABD", color="#d1491f", ha="center", fontsize=10)
    ax.text(1.5, 6.4, "S = ABC' + ABD", ha="center", fontsize=13, weight="bold")
    fig.savefig(os.path.join(FIG, "karnaugh.png"), bbox_inches="tight")
    plt.close(fig)


def circuito(expr, nome):
    with schemdraw.Drawing(show=False) as d:
        d.config(fontsize=13)
        logicparse(expr, outlabel="S", gateH=1.1, gateW=1.9)
    d.save(os.path.join(FIG, nome), dpi=180)


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.join(RAIZ, "src"))
    from expressao import MINTERMOS
    os.makedirs(FIG, exist_ok=True)
    karnaugh(MINTERMOS)
    circuito(ORIGINAL, "circuito_original.png")
    circuito(SIMPLIFICADO, "circuito_simplificado.png")
    print("Figuras geradas em figuras/")
