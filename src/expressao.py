"""Expressões booleanas do módulo de decisão.

Variáveis de entrada (0 = não, 1 = sim):
    A = tem agendamento confirmado no Poupatempo para a CIN
    B = tem certidão válida (nascimento ou casamento, original ou autenticada,
        do estado civil atual, sem rasura e não plastificada)
    C = a pessoa que vai tirar a CIN é menor de 16 anos
    D = há responsável legal presente OU autorização assinada por ele
Saída:
    S = 1 -> pode comparecer ao atendimento com os documentos
    S = 0 -> ainda falta algum requisito; o assistente explica qual
"""

# --------------------------------------------------------------------------
# 1) Forma canônica (item 2 do enunciado)
#    Lista dos mintermos (linhas da tabela em que S = 1), na ordem A B C D,
#    com A como bit mais significativo. Ex.: linha A=1,B=1,C=0,D=0 -> 12.
MINTERMOS = [12, 13, 15]

#    Texto da expressão canônica, como vai aparecer no relatório.
#    Use ' para negação (A' = não A), justaposição para E e + para OU.
EXPRESSAO_CANONICA = "S = ABC'D' + ABC'D + ABCD"

# --------------------------------------------------------------------------
# 2) Simplificação algébrica (item 3)
#    Cada passo: (expressão obtida, propriedade usada).
PASSOS_ALGEBRA = [
    ("S = ABC'D' + ABC'D + ABCD", "Forma canônica (soma de produtos)"),
    ("S = ABC'(D' + D) + ABCD", "Distributiva: XY + XZ = X(Y + Z), com X = ABC'"),
    ("S = ABC'·1 + ABCD", "Complemento: D' + D = 1"),
    ("S = ABC' + ABCD", "Identidade: X·1 = X"),
    ("S = AB(C' + CD)", "Distributiva: colocando AB em evidência"),
    ("S = AB(C' + D)", "Absorção/simplificação: X' + XY = X' + Y, com X = C e Y = D"),
    ("S = ABC' + ABD", "Distributiva (forma soma de produtos, igual à do Karnaugh)"),
]

#    Transformação por De Morgan, se o grupo usar (o enunciado diz
#    "somente se necessário"). Deixe "" se não usar.
DE_MORGAN = ("De Morgan não foi necessário para chegar à expressão mínima. Como demonstração de equivalência, "
             "o termo (C' + D) pode ser escrito como (CD')', pois, por De Morgan, (XY)' = X' + Y'. Assim, "
             "S = AB(C' + D) = AB·(CD')': 'menor de 16 sem responsável' (CD') é exatamente o caso que bloqueia "
             "o atendimento de quem tem agendamento e certidão.")

# --------------------------------------------------------------------------
# 3) Mapa de Karnaugh (item 4)
#    Descrição de cada agrupamento: (células/mintermos, termo resultante).
GRUPOS_KARNAUGH = [
    ("m12 + m13 (linha AB = 11, colunas CD = 00 e 01)", "ABC'"),
    ("m13 + m15 (linha AB = 11, colunas CD = 01 e 11)", "ABD"),
]

# --------------------------------------------------------------------------
# 4) Expressão simplificada final (itens 3 e 4) — texto e implementação.
EXPRESSAO_SIMPLIFICADA = "S = ABC' + ABD = AB(C' + D)"


def saida_simplificada(A: int, B: int, C: int, D: int) -> int:
    """Implementa EXPRESSAO_SIMPLIFICADA com operadores lógicos.

    Use: (not X) para X', (X and Y) para XY, (X or Y) para X + Y.
    Retorne int(...) do resultado.
    """
    # S = AB(C' + D)
    return int(A and B and ((not C) or D))


# --------------------------------------------------------------------------
# 5) Circuitos (item 5): contagem de portas sob o mesmo critério
#    (ex.: cada porta NOT, AND de 2 entradas e OR de 2 entradas conta 1).
CRITERIO_PORTAS = ("Portas de no máximo 2 entradas; cada NOT, AND e OR conta como 1 porta; "
                   "cada termo produto tem suas próprias portas (sem compartilhar portas entre termos).")
PORTAS_ORIGINAL = {"NOT": 3, "AND": 9, "OR": 2}
PORTAS_SIMPLIFICADO = {"NOT": 1, "AND": 2, "OR": 1}


# --------------------------------------------------------------------------
# Daqui para baixo: funções de apoio (não precisam ser alteradas).
def saida_canonica(A: int, B: int, C: int, D: int) -> int:
    """Avalia a soma de mintermos informada em MINTERMOS."""
    return int(((A << 3) | (B << 2) | (C << 1) | D) in MINTERMOS)


def esta_preenchido() -> bool:
    try:
        saida_simplificada(0, 0, 0, 0)
    except NotImplementedError:
        return False
    return bool(MINTERMOS) and bool(EXPRESSAO_SIMPLIFICADA)
