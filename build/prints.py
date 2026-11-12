"""Roda src/assistente.py em alguns cenários e salva prints (PNG) da saída do terminal.

Gera figuras/print_programa1..4.png com o Edge headless.
Uso: py build/prints.py
"""
import html
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(RAIZ, "figuras")
TMP = os.path.join(RAIZ, "relatorio")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
ASSISTENTE = os.path.join(RAIZ, "src", "assistente.py")

# (nome, argumentos, texto digitado no modo interativo, comando mostrado)
CENARIOS = [
    ("print_programa1", [], "s\ns\nn\nn\n", "py src/assistente.py"),
    ("print_programa2", ["1110"], None, "py src/assistente.py 1110"),
    ("print_programa3", [], "talvez\ns\nn\nsim\nnao\n", "py src/assistente.py"),
    ("print_programa4", ["10x1"], None, "py src/assistente.py 10x1"),
]


def rodar(args, entrada):
    r = subprocess.run([sys.executable, ASSISTENTE, *args], input=entrada or "", capture_output=True,
                       text=True, encoding="utf-8", env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    saida = r.stdout
    if entrada:  # mostra as respostas digitadas logo após cada pergunta, como num terminal
        respostas = iter(entrada.splitlines())
        partes = saida.split("(s/n, ou 'sair'): ")
        saida = "".join(p + "(s/n, ou 'sair'): " + next(respostas, "") + "\n" for p in partes[:-1]) + partes[-1]
    return saida


def png(nome, comando, texto):
    linhas = texto.count("\n") + 3
    doc = f"""<!doctype html><meta charset="utf-8"><style>
body {{ margin: 0; background: #0c0c0c; }}
.bar {{ background: #2d2d2d; color: #ddd; font: 13px Segoe UI, sans-serif; padding: 6px 12px; }}
pre {{ margin: 0; padding: 10px 14px; color: #cccccc; font: 14px/1.35 Consolas, monospace; white-space: pre-wrap; }}
.p {{ color: #6fc36f; }}
</style><div class="bar">Windows PowerShell — gs-cs-citizen-assist</div>
<pre><span class="p">PS C:\\gs-cs-citizen-assist&gt;</span> {html.escape(comando)}
{html.escape(texto)}</pre>"""
    caminho_html = os.path.join(TMP, f"_{nome}.html")
    with open(caminho_html, "w", encoding="utf-8") as f:
        f.write(doc)
    altura = 40 + linhas * 19
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--hide-scrollbars", f"--window-size=900,{altura}",
                    f"--screenshot={os.path.join(FIG, nome + '.png')}",
                    "file:///" + caminho_html.replace("\\", "/")], check=True, capture_output=True)
    os.remove(caminho_html)


if __name__ == "__main__":
    for nome, args, entrada, comando in CENARIOS:
        png(nome, comando, rodar(args, entrada))
    print("Prints gerados em figuras/")
