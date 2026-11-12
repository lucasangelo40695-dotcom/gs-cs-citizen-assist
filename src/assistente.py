"""Citizen Assist AI — módulo de decisão lógica (Computer Science).

Pergunta ao cidadão quatro condições (sim/não), calcula a saída S com a
expressão simplificada do grupo (src/expressao.py) e mostra a orientação.

Uso:
    py src/assistente.py              modo interativo
    py src/assistente.py 1101         entradas diretas na ordem A B C D
"""
import sys

from expressao import saida_simplificada

AVISO = (
    "AVISO: este é um protótipo acadêmico (FIAP – Global Solution). Não é um canal\n"
    "oficial do Poupatempo nem do governo e não confirma a emissão do documento.\n"
    "Confira sempre as regras em www.poupatempo.sp.gov.br antes de ir.\n"
    "Nenhum dado pessoal é pedido ou guardado: só respostas sim/não."
)

FONTE = ("Poupatempo SP – Carta de Serviços 'Obter Carteira de Identidade Nacional – CIN' "
         "(consultado em 12/11/2026).")

PERGUNTAS = [
    ("A", "Você já tem agendamento confirmado no Poupatempo para a CIN?"),
    ("B", "Você tem a certidão de nascimento ou de casamento (do estado civil atual),\n"
          "   original ou autenticada, sem rasura e não plastificada?"),
    ("C", "A pessoa que vai tirar a CIN tem menos de 16 anos?"),
    ("D", "Haverá um responsável legal presente OU uma autorização assinada por ele?"),
]

SIM = {"s", "sim", "1", "y", "yes"}
NAO = {"n", "nao", "não", "0", "no"}
SAIR = {"sair", "q", "exit"}
MAX_TENTATIVAS = 3


class EntradaInvalida(ValueError):
    pass


def interpretar(resposta: str) -> int:
    """Converte uma resposta de texto em 0/1 ou lança EntradaInvalida."""
    r = resposta.strip().lower()
    if r in SIM:
        return 1
    if r in NAO:
        return 0
    raise EntradaInvalida(resposta)


def ler_bits(texto: str) -> dict:
    """Valida entradas diretas como '1101' (A B C D)."""
    t = texto.replace(" ", "").replace(",", "")
    if len(t) != 4 or any(ch not in "01" for ch in t):
        raise EntradaInvalida(texto)
    return dict(zip("ABCD", (int(ch) for ch in t)))


def perguntar(entrada=input, saida=print) -> dict:
    valores = {}
    for var, texto in PERGUNTAS:
        for tentativa in range(1, MAX_TENTATIVAS + 1):
            resposta = entrada(f"\n[{var}] {texto}\n   (s/n, ou 'sair'): ")
            if resposta.strip().lower() in SAIR:
                raise SystemExit("\nAtendimento encerrado pelo usuário.")
            try:
                valores[var] = interpretar(resposta)
                break
            except EntradaInvalida:
                restantes = MAX_TENTATIVAS - tentativa
                saida(f"   Resposta inválida: '{resposta.strip()}'. Responda 's' para sim ou 'n' para não."
                      + (f" ({restantes} tentativa(s) restante(s))" if restantes else ""))
        else:
            raise SystemExit("\nMuitas respostas inválidas. Tente de novo mais tarde.")
    return valores


def orientacao(v: dict) -> str:
    """Monta o texto da resposta. S vem só da expressão simplificada do grupo."""
    s = saida_simplificada(v["A"], v["B"], v["C"], v["D"])
    linhas = [f"\nEntradas: A={v['A']} B={v['B']} C={v['C']} D={v['D']}  ->  S = {s}", ""]
    if s == 1:
        linhas += [
            "RESULTADO: você pode comparecer ao Poupatempo no dia agendado.",
            "Leve: certidão original ou autenticada + cópia simples e o número do CPF.",
        ]
        if v["C"] == 1:
            linhas.append("Como é menor de 16 anos: responsável com documento e CPF (original e cópia)\n"
                          "ou a autorização assinada por ele, com documento e CPF do responsável.")
    else:
        linhas.append("RESULTADO: ainda falta algum requisito antes de ir ao atendimento.")
        dicas = []
        if v["A"] == 0:
            dicas.append("- Agende pelo site, app Poupatempo SP.GOV.BR ou WhatsApp (o agendamento é gratuito).")
        if v["B"] == 0:
            dicas.append("- Providencie a certidão de nascimento/casamento atualizada no cartório de registro civil.")
        if v["C"] == 1 and v["D"] == 0:
            dicas.append("- Menores de 16 anos precisam do responsável legal presente ou de autorização assinada.")
        linhas += dicas or ["- Revise as respostas e confira os requisitos no site oficial."]
    linhas += ["", f"Fonte: {FONTE}"]
    return "\n".join(linhas)


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    print("=" * 70)
    print("Citizen Assist AI — Posso pedir a 1ª via da Carteira de Identidade Nacional?")
    print("=" * 70)
    print(AVISO)
    try:
        valores = ler_bits(argv[0]) if argv else perguntar()
    except EntradaInvalida as e:
        print(f"\nEntrada inválida: '{e}'. Informe 4 dígitos 0/1 na ordem A B C D, ex.: 1101.")
        return 2
    except (EOFError, KeyboardInterrupt):
        print("\nAtendimento encerrado.")
        return 1
    print(orientacao(valores))
    return 0


if __name__ == "__main__":
    sys.exit(main())
