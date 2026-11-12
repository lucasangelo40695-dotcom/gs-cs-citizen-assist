"""Gera relatorio/relatorio_tecnico.pdf (HTML -> PDF pelo Edge headless).

O texto descritivo é fixo aqui. Tudo o que o grupo faz à mão vem de:
    dados/tabela_verdade.csv     tabela-verdade
    src/expressao.py             canônica, passos algébricos, De Morgan, Karnaugh, portas
    figuras/*.png                Karnaugh, circuitos e prints (nomes abaixo)
    resultados/*.csv             gerados por src/validar.py
O que ainda não foi preenchido aparece em vermelho como [A PREENCHER PELO GRUPO].

Uso: py build/relatorio.py
"""
import csv
import glob
import html
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "src"))
import expressao as ex  # noqa: E402

REL = os.path.join(RAIZ, "relatorio")
FIG = os.path.join(RAIZ, "figuras")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

INTEGRANTES = [("Gabriel Rodrigues", "569322"), ("Gustavo Guedes", "569779"), ("Lucas Angelo", "569530")]

CSS = """
@page { size: A4; margin: 3cm 2cm 2cm 3cm;
        @bottom-right { content: counter(page); font: 10pt "Times New Roman", serif; } }
body { font-family: "Times New Roman", Times, serif; font-size: 12pt; line-height: 1.5; margin: 0; color: #000; }
p { margin: 0 0 6pt; text-align: justify; text-indent: 1.25cm; }
p.sem { text-indent: 0; }
h1 { font-size: 12pt; text-transform: uppercase; margin: 18pt 0 10pt; break-after: avoid; }
h2 { font-size: 12pt; font-weight: normal; text-transform: uppercase; margin: 12pt 0 8pt; break-after: avoid; }
.cab { text-align: center; margin-bottom: 18pt; }
.cab .t { font-weight: bold; text-transform: uppercase; font-size: 14pt; }
.ilus { margin: 10pt 0; break-inside: avoid; text-align: center; }
.ilus .leg { font-size: 10pt; line-height: 1.1; margin-bottom: 4pt; }
.ilus .fonte { font-size: 10pt; line-height: 1.1; text-align: left; margin-top: 4pt; }
.ilus img { max-width: 100%; max-height: 11cm; }
table { border-collapse: collapse; margin: 0 auto; font-size: 10pt; line-height: 1.2; }
th { border-top: 1px solid #000; border-bottom: 1px solid #000; padding: 2pt 7pt; }
td { padding: 1.5pt 7pt; text-align: center; }
tr:last-child td { border-bottom: 1px solid #000; }
td.e { text-align: left; }
.eq { text-align: center; font-family: "Cambria Math", "Times New Roman", serif; margin: 6pt 0; }
.falta { color: #c00000; font-weight: bold; }
.vaga { border: 1.5px dashed #c00000; color: #c00000; padding: 28pt 10pt; font-weight: bold; }
.aviso { border: 1px solid #000; padding: 6pt 10pt; font-size: 11pt; line-height: 1.3; margin: 8pt 0; }
pre { font-family: Consolas, monospace; font-size: 9.5pt; line-height: 1.25; background: #f3f3f3;
      padding: 6pt 8pt; white-space: pre-wrap; text-align: left; }
.ref p { text-indent: 0; text-align: left; line-height: 1.15; margin-bottom: 10pt; }
"""

FALTA = '<span class="falta">[A PREENCHER PELO GRUPO]</span>'
_n = {"fig": 0, "tab": 0}


def esc(t):
    return html.escape(str(t))


def ou_falta(valor):
    return esc(valor) if valor not in ("", None, [], {}) else FALTA


def figura(titulo, padrao, largura="15cm"):
    arquivos = sorted(glob.glob(os.path.join(FIG, padrao)))
    blocos = []
    for arq in arquivos or [None]:
        _n["fig"] += 1
        corpo = (f'<img src="file:///{arq.replace(os.sep, "/")}" style="width:{largura}">' if arq
                 else f'<div class="vaga">Inserir figura: figuras/{esc(padrao)}</div>')
        blocos.append(f'<div class="ilus"><div class="leg">Figura {_n["fig"]} – {esc(titulo)}</div>'
                      f'{corpo}</div>')
    return "".join(blocos)


def tabela(titulo, cab, linhas, esquerda=()):
    _n["tab"] += 1
    th = "".join(f"<th>{esc(c)}</th>" for c in cab)
    trs = "".join("<tr>" + "".join(
        f'<td class="{"e" if j in esquerda else ""}">{c}</td>' for j, c in enumerate(l)) + "</tr>" for l in linhas)
    return (f'<div class="ilus"><div class="leg">Tabela {_n["tab"]} – {esc(titulo)}</div>'
            f'<table><tr>{th}</tr>{trs}</table></div>')


def ler_csv(caminho):
    if not os.path.exists(caminho):
        return []
    with open(caminho, encoding="utf-8") as f:
        return list(csv.reader(f))[1:]


def foto(nome):
    """Caminho da foto do caderno (jpg/png/webp) em figuras/, ou None."""
    for ext in ("jpg", "jpeg", "png", "webp"):
        if os.path.exists(os.path.join(FIG, f"{nome}.{ext}")):
            return f"{nome}.{ext}"
    return None


def secao_tabela_verdade():
    if foto("foto_tabela_verdade"):
        return figura("Tabela-verdade do módulo de decisão", foto("foto_tabela_verdade"), "10cm")
    linhas = ler_csv(os.path.join(RAIZ, "dados", "tabela_verdade.csv"))
    if len(linhas) != 16:
        return f'<p class="sem">{FALTA} – preencher <code>dados/tabela_verdade.csv</code> com as 16 combinações.</p>'
    linhas = sorted(linhas, key=lambda l: int("".join(l[:4]), 2))
    return tabela("Tabela-verdade do módulo de decisão",
                  ["m", "A", "B", "C", "D", "S"],
                  [[int("".join(l[:4]), 2), *l[:5]] for l in linhas])


def secao_algebra():
    if not ex.PASSOS_ALGEBRA:
        return f'<p class="sem">{FALTA} – passos em <code>PASSOS_ALGEBRA</code> (src/expressao.py).</p>'
    return tabela("Simplificação algébrica passo a passo", ["Passo", "Expressão", "Propriedade aplicada"],
                  [[i, esc(e), esc(p)] for i, (e, p) in enumerate(ex.PASSOS_ALGEBRA, 1)], esquerda=(1, 2))


def secao_karnaugh():
    grupos = (tabela("Agrupamentos no mapa de Karnaugh", ["Grupo", "Células", "Termo"],
                     [[i, esc(c), esc(t)] for i, (c, t) in enumerate(ex.GRUPOS_KARNAUGH, 1)], esquerda=(1,))
              if ex.GRUPOS_KARNAUGH else f'<p class="sem">{FALTA} – agrupamentos em <code>GRUPOS_KARNAUGH</code>.</p>')
    arq = foto("foto_karnaugh") or "karnaugh.png"
    return figura("Mapa de Karnaugh de S(A, B, C, D)", arq, "11cm") + grupos


def secao_portas():
    def total(d):
        return sum(v for v in d.values() if v is not None) if all(v is not None for v in d.values()) else None
    lin = [[k, ou_falta(ex.PORTAS_ORIGINAL[k]), ou_falta(ex.PORTAS_SIMPLIFICADO[k])] for k in ex.PORTAS_ORIGINAL]
    lin.append(["<b>Total</b>", ou_falta(total(ex.PORTAS_ORIGINAL)), ou_falta(total(ex.PORTAS_SIMPLIFICADO))])
    return tabela("Quantidade de portas: circuito original × simplificado",
                  ["Porta", "Original (canônico)", "Simplificado"], lin)


def secao_testes():
    t = ler_csv(os.path.join(RAIZ, "resultados", "testes.csv"))
    inv = ler_csv(os.path.join(RAIZ, "resultados", "entradas_invalidas.csv"))
    if len(t) != 16:
        return f'<p class="sem">{FALTA} – rodar <code>py src/validar.py</code> depois de preencher a tabela e a expressão.</p>'
    ok = sum(l[-1] == "OK" for l in t)
    out = (f'<p>O script <code>src/validar.py</code> percorreu as 16 combinações e comparou a regra original '
           f'(tabela-verdade do grupo), a forma canônica, a expressão simplificada e a saída impressa pelo programa '
           f'em execução real. Resultado: <b>{ok} de 16</b> combinações equivalentes nas quatro representações.</p>')
    out += tabela("Validação das 16 combinações",
                  ["m", "A", "B", "C", "D", "Tabela", "Canônica", "Simplificada", "Executado", "Resultado"], t)
    if inv:
        out += tabela("Tratamento de entradas inválidas", ["Entrada", "Código", "Mensagem exibida", "Resultado"],
                      [[esc(l[0]), l[1], esc(l[2]), l[3]] for l in inv], esquerda=(2,))
    return out


def simulador():
    if not glob.glob(os.path.join(FIG, "print_simulador*.png")):
        return ""
    casos = [
        ("print_simulador1.png", "Simulador logic.ly – A=1, B=1, C=0, D=0: maior de 16 anos com agendamento e certidão (S = 1)"),
        ("print_simulador2.png", "Simulador logic.ly – A=1, B=1, C=1, D=0: menor de 16 anos sem responsável (S = 0)"),
        ("print_simulador3.png", "Simulador logic.ly – A=1, B=1, C=1, D=1: menor de 16 anos com responsável (S = 1)"),
    ]
    figs = "".join(figura(t, arq, "11cm") for arq, t in casos if os.path.exists(os.path.join(FIG, arq)))
    return ("<p>O circuito simplificado, S = AB(C' + D), também foi montado no simulador logic.ly. As chaves "
            "representam, de cima para baixo, as entradas A, B, C e D, e a lâmpada representa a saída S. Os casos "
            "abaixo reproduzem o resultado da tabela-verdade.</p>" + figs)


def corpo():
    integrantes = "<br>".join(f"{n} – RM {rm}" for n, rm in INTEGRANTES)
    return f"""
<div class="cab"><div class="t">Citizen Assist AI – Módulo de decisão lógica</div>
<div>Orientação para a 1ª via da Carteira de Identidade Nacional (CIN)</div>
<div style="margin-top:8pt">Global Solution GS26_2 – Computer Science – Ciência da Computação, 1CC – FIAP</div>
<div style="margin-top:8pt">{integrantes}</div></div>

<h1>1 Descrição do problema</h1>
<p>Muitos cidadãos vão ao posto de atendimento para pedir a primeira via da Carteira de Identidade Nacional
(CIN) e voltam sem o documento porque falta um requisito: o agendamento, a certidão adequada ou, no caso de
menores de 16 anos, o acompanhamento do responsável legal. O módulo de decisão do Citizen Assist AI responde à
pergunta “posso comparecer ao Poupatempo para pedir a 1ª via da CIN?” a partir de quatro condições do tipo
sim/não e, quando a resposta é negativa, indica o que falta.</p>

<h1>2 Definição das variáveis</h1>
{tabela("Variáveis de entrada e saída", ["Variável", "Significado", "Valor 0", "Valor 1"], [
    ["A", "Agendamento confirmado no Poupatempo para a CIN", "Não tem", "Tem"],
    ["B", "Certidão válida (nascimento ou casamento do estado civil atual, original ou autenticada, sem rasura, não plastificada)", "Não tem", "Tem"],
    ["C", "Quem vai tirar a CIN é menor de 16 anos", "16 anos ou mais", "Menor de 16"],
    ["D", "Responsável legal presente ou autorização assinada por ele", "Não", "Sim"],
    ["S", "Orientação apresentada ao usuário", "Ainda falta requisito", "Pode comparecer"],
], esquerda=(1,))}

<h1>3 Regras</h1>
<p class="sem">R1. O atendimento presencial exige agendamento prévio, feito pelo site, aplicativo ou WhatsApp do Poupatempo.<br>
R2. Para a 1ª via é obrigatória a certidão de nascimento (solteiros) ou de casamento com averbação do estado civil
atual, original ou autenticada, com cópia simples; certidões plastificadas, rasuradas ou ilegíveis não são aceitas.<br>
R3. Menores de 16 anos devem estar acompanhados do responsável legal, com documento de identificação e CPF; se o
responsável não puder comparecer, é obrigatória a autorização assinada por ele.<br>
R4. A 1ª via é gratuita; o CPF deve ser informado ou apresentado em documento oficial.</p>
<p>Assim, o cidadão pode comparecer (S = 1) quando tem agendamento, tem certidão válida e, se for menor de 16
anos, tem o responsável presente ou a autorização.</p>
<div class="eq">S = 1 &nbsp;⇔&nbsp; A · B · (C' + D)</div>
<p>Exemplos: quem tem agendamento e certidão e tem 16 anos ou mais (A = 1, B = 1, C = 0) pode comparecer;
um menor de 16 anos com agendamento e certidão, mas sem responsável nem autorização (A = 1, B = 1, C = 1, D = 0),
ainda não pode. Quando C = 0, o valor de D não altera a saída, porque a exigência do responsável vale só para
menores de 16 anos.</p>

<h1>4 Tabela-verdade</h1>
{secao_tabela_verdade()}

<h1>5 Expressão canônica</h1>
<div class="eq">{ou_falta(ex.EXPRESSAO_CANONICA)}</div>

<h1>6 Simplificação por álgebra booleana</h1>
{secao_algebra()}
<h2>6.1 Teoremas de De Morgan</h2>
<p>{esc(ex.DE_MORGAN) if ex.DE_MORGAN else "O enunciado pede De Morgan somente se necessário. " + FALTA + " – justificar se foi usado ou por que não foi necessário (campo DE_MORGAN)."}</p>
<p class="sem">Expressão simplificada: </p><div class="eq">{ou_falta(ex.EXPRESSAO_SIMPLIFICADA)}</div>

<h1>7 Mapa de Karnaugh</h1>
{secao_karnaugh()}
<p>Comparação com a simplificação algébrica: {FALTA if not ex.GRUPOS_KARNAUGH else "cada grupo junta dois 1s vizinhos e elimina a variável que muda dentro dele (D no grupo 1 e C no grupo 2). A célula m13 participa dos dois grupos, o que é permitido. O resultado, S = ABC' + ABD, é exatamente a forma obtida no último passo da Seção 6, e a validação da Seção 10 confirma a equivalência."}</p>

<h1>8 Circuitos lógicos</h1>
<p>Critério de contagem: {esc(ex.CRITERIO_PORTAS)}</p>
{figura("Circuito original (forma canônica)", "circuito_original*.png")}
{figura("Circuito simplificado", "circuito_simplificado*.png")}
{secao_portas()}
<p>Sob o mesmo critério, o circuito simplificado usa 4 portas contra 14 do circuito canônico, uma redução de
cerca de 71%, com a mesma saída para as 16 combinações (Seção 10). Menos portas significam menor custo, menor
atraso de propagação e menos pontos de falha.</p>

<h1>9 Implementação</h1>
<p>A lógica simplificada foi implementada em Python 3, sem bibliotecas externas, no programa
<code>src/assistente.py</code>. A saída S é calculada exclusivamente pela função <code>saida_simplificada</code>
(arquivo <code>src/expressao.py</code>), que contém a expressão obtida pelo grupo. O programa faz as quatro perguntas,
aceita “s/sim/1” e “n/não/0”, recusa qualquer outra resposta com mensagem explicativa (até três tentativas) e
também aceita as entradas diretas na linha de comando (ex.: <code>1101</code>), validando que sejam quatro dígitos 0/1.
Quando S = 0, a resposta indica qual requisito falta e onde resolvê-lo.</p>
{figura("Modo interativo: maior de 16 anos com agendamento e certidão (S = 1)", "print_programa1.png", "14cm")}
{figura("Entrada direta 1110: menor de 16 anos sem responsável (S = 0)", "print_programa2.png", "14cm")}
{figura("Resposta inválida recusada e orientação com dois requisitos faltando", "print_programa3.png", "14cm")}
{figura("Entrada direta inválida recusada", "print_programa4.png", "14cm")}
{simulador()}

<h1>10 Resultados dos testes</h1>
{secao_testes()}

<h1>11 Instruções de execução</h1>
<p>Requisito: Python 3.10 ou superior. O programa e a validação usam só a biblioteca padrão, sem instalar nada.
No Linux ou macOS, troque <code>py</code> por <code>python3</code>. Os comandos são executados na pasta do projeto.</p>
<pre># 1. Baixar o projeto
git clone https://github.com/lucasangelo40695-dotcom/gs-cs-citizen-assist.git
cd gs-cs-citizen-assist

# 2. Assistente interativo (responda s/n a cada pergunta)
py src/assistente.py

# 3. Entradas diretas, na ordem A B C D (ex.: A=1, B=1, C=0, D=1)
py src/assistente.py 1101

# 4. Validação das 16 combinações e das entradas inválidas
py src/validar.py</pre>
<p><b>Simulador:</b> o circuito simplificado pode ser remontado em https://logic.ly/demo/ com 4 chaves (A, B, C e D),
1 porta NOT, 1 OR, 2 AND e 1 lâmpada (S), ligados conforme a Figura 3. Ao alternar as chaves, a lâmpada acende
somente nas combinações 1100, 1101 e 1111.</p>

"""


def main():
    os.makedirs(REL, exist_ok=True)
    doc = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{corpo()}</body></html>'
    caminho_html = os.path.join(REL, "relatorio_tecnico.html")
    caminho_pdf = os.path.join(REL, "relatorio_tecnico.pdf")
    with open(caminho_html, "w", encoding="utf-8") as f:
        f.write(doc)
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={caminho_pdf}", "file:///" + caminho_html.replace("\\", "/")],
                   check=True, capture_output=True)
    print("PDF gerado:", os.path.relpath(caminho_pdf, RAIZ))


if __name__ == "__main__":
    main()
