'''
Evandro Diniz - Github: evdiniz
Henrique Colle Marinozzi - Github: HenriqueMarinozzi
'''

def parseExpressao(linha):
  # Função principal do analisador léxico (AFD)
  # Percorre a linha e gera uma lista de tokens válidos

  i = 0
  tokens = []
  parenteses = 0  # Controle de balanceamento de parênteses

  tamanho = len(linha)  # leve mudança

  while i < tamanho:

    t = linha[i]

    # Estado: número (inteiro ou real)
    if t.isdigit():
      numero, i = estadoNumero(linha, i)
      tokens.append(numero)

    # Estado: operador
    elif t in ['+', '-', '*', '/', '%', '^']:
      op, i = estadoOperador(linha, i)
      tokens.append(op)

    # Estado: parênteses
    elif t in ('(', ')'):  # pequena variação
      par, i = estadoParenteses(linha, i)

      # Atualiza controle de balanceamento
      parenteses += 1 if par == '(' else -1

      # Detecta fechamento inválido
      if parenteses < 0:
        raise ValueError("Parênteses não correspondentes!")

      tokens.append(par)

    # Estado: comandos (RES, MEM, etc.)
    elif t.isalpha():
      cmd, i = estadoComando(linha, i)
      tokens.append(cmd)

    # Ignora espaços em branco
    elif t.isspace():  # mais genérico que ' '
      i += 1

    # Qualquer outro caractere é inválido
    else:
      raise ValueError("Caractere incorreto! : " + t)

  # Verifica se todos os parênteses foram fechados
  if parenteses != 0:
    raise ValueError("Parênteses não correspondentes!")

  return tokens


def estadoNumero(linha, i):
  # Estado do AFD responsável por reconhecer números reais (com ponto)

  numero = ''
  ponto = False  # Controla ocorrência do ponto decimal

  tamanho = len(linha)

  while i < tamanho:

    c = linha[i]

    if c.isdigit():
      numero += c
      i += 1

    elif c == '.':
      # Permite apenas um ponto decimal
      if ponto:
        raise ValueError("Ponto redundante")

      ponto = True
      numero += c
      i += 1

    else:
      break

  return numero, i


def estadoOperador(linha, i):
  # Estado do AFD para operadores aritméticos

  op = linha[i]

  # Trata operador de divisão inteira (//)
  if op == '/' and i + 1 < len(linha) and linha[i + 1] == '/':
    op = '//'
    i += 1

  # Valida operador
  if op not in ['+', '-', '*', '/', '//', '%', '^']:
    raise ValueError("Operador incorreto!: " + op)

  return op, i + 1


def estadoParenteses(linha, i):
  # Estado do AFD para parênteses

  p = linha[i]

  if p not in ['(', ')']:
    raise ValueError("Parêntese incorreto!")

  return p, i + 1


def estadoComando(linha, i):
  # Estado do AFD para comandos especiais (RES, MEM, variáveis)

  comando = ''

  tamanho = len(linha)

  # Aceita apenas letras maiúsculas (conforme especificação)
  while i < tamanho and linha[i].isalpha() and linha[i].isupper():
    comando += linha[i]
    i += 1

  # Validação de comando vazio
  if not comando:  # pequena mudança
    raise ValueError("Comando incorreto")

  return comando, i
