"""Valida as 16 combinações (item 8 do enunciado).

Compara, linha a linha:
    1. regra original  -> coluna S da tabela-verdade feita pelo grupo (dados/tabela_verdade.csv)
    2. forma canônica  -> soma dos MINTERMOS informados em src/expressao.py
    3. simplificada    -> saida_simplificada() em src/expressao.py
    4. executado       -> S impresso pelo programa src/assistente.py rodando de verdade
Também testa entradas inválidas. Grava resultados/testes.csv e resultados/entradas_invalidas.csv.

Uso: py src/validar.py
"""
import csv
import os
import re
import subprocess
import sys
from itertools import product

import expressao

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABELA = os.path.join(RAIZ, "dados", "tabela_verdade.csv")
ASSISTENTE = os.path.join(RAIZ, "src", "assistente.py")
SAIDA = os.path.join(RAIZ, "resultados")

INVALIDAS = ["", "12", "10a1", "11111", "abc", "1 0 1"]


def ler_tabela() -> dict:
    with open(TABELA, encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    if len(linhas) != 16:
        raise SystemExit(f"A tabela-verdade tem {len(linhas)} linha(s); precisa de 16. "
                         f"Preencha {os.path.relpath(TABELA, RAIZ)}.")
    tabela = {}
    for i, l in enumerate(linhas, start=2):
        try:
            chave = tuple(int(l[k]) for k in "ABCD")
            s = int(l["S"])
        except (KeyError, ValueError):
            raise SystemExit(f"Linha {i} da tabela inválida: {l}")
        if any(x not in (0, 1) for x in (*chave, s)):
            raise SystemExit(f"Linha {i}: use apenas 0 ou 1.")
        if chave in tabela:
            raise SystemExit(f"Linha {i}: combinação {chave} repetida.")
        tabela[chave] = s
    return tabela


def executar(argumento: str):
    r = subprocess.run([sys.executable, ASSISTENTE, argumento], capture_output=True,
                       text=True, encoding="utf-8", env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    m = re.search(r"->\s+S = ([01])", r.stdout)
    return r.returncode, (int(m.group(1)) if m else None), r.stdout


def main() -> int:
    if not expressao.esta_preenchido():
        print("src/expressao.py ainda não foi preenchido pelo grupo "
              "(MINTERMOS, EXPRESSAO_SIMPLIFICADA e saida_simplificada).")
        return 1
    tabela = ler_tabela()
    os.makedirs(SAIDA, exist_ok=True)

    linhas, falhas = [], 0
    print(f"{'m':>3} | A B C D | Tabela Canônica Simplif. Executado | OK")
    print("-" * 56)
    for a, b, c, d in product((0, 1), repeat=4):
        m = a * 8 + b * 4 + c * 2 + d
        t = tabela[(a, b, c, d)]
        can = expressao.saida_canonica(a, b, c, d)
        sim = expressao.saida_simplificada(a, b, c, d)
        _, exe, _ = executar(f"{a}{b}{c}{d}")
        ok = t == can == sim == exe
        falhas += not ok
        linhas.append([m, a, b, c, d, t, can, sim, exe, "OK" if ok else "FALHA"])
        print(f"{m:>3} | {a} {b} {c} {d} |   {t}       {can}        {sim}        {exe}     | {'OK' if ok else 'FALHA'}")

    with open(os.path.join(SAIDA, "testes.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["mintermo", "A", "B", "C", "D", "tabela", "canonica", "simplificada", "executado", "resultado"])
        w.writerows(linhas)

    print("\nEntradas inválidas (o programa deve recusar com código 2):")
    inval, falhas_inv = [], 0
    for e in INVALIDAS:
        codigo, s, saida = executar(e)
        ok = codigo == 2 and s is None
        falhas_inv += not ok
        msg = saida.strip().splitlines()[-1] if saida.strip() else ""
        inval.append([repr(e), codigo, msg, "OK" if ok else "FALHA"])
        print(f"  {repr(e):8} -> código {codigo} | {'OK' if ok else 'FALHA'}")
    with open(os.path.join(SAIDA, "entradas_invalidas.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["entrada", "codigo_saida", "mensagem", "resultado"])
        w.writerows(inval)

    print(f"\nCombinações equivalentes: {16 - falhas}/16 | Entradas inválidas recusadas: "
          f"{len(INVALIDAS) - falhas_inv}/{len(INVALIDAS)}")
    return 0 if falhas == falhas_inv == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
