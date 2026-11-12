# Citizen Assist AI – Módulo de decisão lógica – Global Solution Computer Science

Módulo de decisão do **Citizen Assist AI** com lógica booleana, forma canônica, mapa de Karnaugh e circuitos.
Disciplina **Computer Science** – Ciência da Computação, 1º ano, turma 1CC – GS26_2.

## Integrantes

| Nome completo | RM |
|---|---|
| Lucas Angelo | 569530 |
| Gustavo Guedes | 569779 |
| Gabriel Rodrigues | 569322 |

## Situação de atendimento escolhida

**"Posso comparecer ao Poupatempo para pedir a 1ª via da Carteira de Identidade Nacional (CIN)?"**

| Variável | Significado | 0 | 1 |
|---|---|---|---|
| A | Agendamento confirmado no Poupatempo para a CIN | não tem | tem |
| B | Certidão válida (nascimento/casamento do estado civil atual, original ou autenticada, sem rasura, não plastificada) | não tem | tem |
| C | Quem vai tirar a CIN é menor de 16 anos | 16 ou mais | menor de 16 |
| D | Responsável legal presente ou autorização assinada por ele | não | sim |
| **S** | Orientação ao usuário | ainda falta requisito | pode comparecer |

**Regras** (Poupatempo SP, carta de serviços "Obter Carteira de Identidade Nacional – CIN", consultada em 12/11/2026):
agendamento obrigatório; certidão de nascimento ou casamento original/autenticada, não plastificada;
menores de 16 anos acompanhados do responsável legal ou com autorização assinada por ele; 1ª via gratuita.

Fontes:
* <https://www.poupatempo.sp.gov.br/carta/D97C3844-A2D9-4C9E-B364-CB4FEB26A1FB>
* <https://www.gov.br/gestao/pt-br/identidade-nacional>
* Lei 7.116/1983 – <https://www.planalto.gov.br/ccivil_03/leis/l7116.htm>

## Resultado

* Tabela-verdade: forma canônica **S = ABC'D' + ABC'D + ABCD**
* Simplificada (álgebra e Karnaugh): **S = ABC' + ABD = AB(C' + D)**
* Circuito: 14 portas (canônico) → 4 portas (simplificado), mesmo critério de 2 entradas
* Validação: **16/16** combinações equivalentes (tabela = canônica = simplificada = programa) e 6/6 entradas inválidas recusadas

* Simulador: circuito simplificado montado no [logic.ly](https://logic.ly/demo/), prints em `figuras/print_simulador1..3.png`

**Relatório:** [`relatorio/relatorio_tecnico.pdf`](relatorio/relatorio_tecnico.pdf)

## Estrutura do repositório

```
├── dados/
│   └── tabela_verdade.csv        # tabela-verdade
├── src/
│   ├── expressao.py              # canônica, passos algébricos, Karnaugh, simplificada, portas
│   ├── assistente.py             # programa que implementa a lógica simplificada (item 6)
│   └── validar.py                # testa as 16 combinações e as entradas inválidas (item 8)
├── figuras/                      # Karnaugh, circuitos e prints
├── resultados/                   # CSVs gerados pelo validar.py
├── build/
│   ├── figuras.py                # gera Karnaugh e circuitos (schemdraw/matplotlib)
│   ├── prints.py                 # gera os prints do programa rodando
│   └── relatorio.py              # gera o PDF a partir de tudo acima
└── relatorio/
    └── relatorio_tecnico.pdf     # entregável
```

| Item do enunciado | Onde está |
|---|---|
| 1. Tabela-verdade | `dados/tabela_verdade.csv` → seção 4 do relatório |
| 2. Forma canônica | `MINTERMOS`, `EXPRESSAO_CANONICA` → seção 5 |
| 3. Álgebra booleana / De Morgan | `PASSOS_ALGEBRA`, `DE_MORGAN` → seção 6 |
| 4. Mapa de Karnaugh | `figuras/karnaugh.png`, `GRUPOS_KARNAUGH` → seção 7 |
| 5. Circuitos e contagem de portas | `figuras/circuito_*.png`, `PORTAS_*` → seção 8 |
| 6. Implementação | `src/assistente.py` → seção 9 |
| 7. Simulador | `figuras/print_simulador*.png` → seção 9 |
| 8. Validação das combinações | `src/validar.py`, `resultados/` → seção 10 |
| Fontes, limitações e privacidade | seções 3 e 11 |

## Como executar

Requisito: Python 3.10+ (o programa e a validação usam só a biblioteca padrão). No Linux/macOS use `python3` no lugar de `py`.

```bash
py src/assistente.py          # modo interativo (responda s/n)
py src/assistente.py 1101     # entradas diretas, ordem A B C D
py src/validar.py             # valida as 16 combinações + entradas inválidas
py build/relatorio.py         # gera relatorio/relatorio_tecnico.pdf (usa o Microsoft Edge)
```

Para regenerar as figuras (precisa de `pip install -r requirements.txt`):

```bash
py -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python build/figuras.py
py build/prints.py
```

## Aviso

Protótipo acadêmico. **Não é canal oficial** do Poupatempo nem do governo e não confirma a emissão do documento
nem a concessão de serviços ou direitos. Não coleta dados pessoais: só respostas sim/não, que não são gravadas.
