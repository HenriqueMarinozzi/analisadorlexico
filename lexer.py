class ErroLexico(Exception):
    pass


class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"Token(tipo='{self.tipo}', valor='{self.valor}')"


def eh_digito(c):
    return '0' <= c <= '9'


def eh_letra(c):
    return ('A' <= c <= 'Z') or ('a' <= c <= 'z')


def eh_operador_inicio(c):
    return c in "+-*/%^"


def estado_numero(linha, i):
    inicio = i
    tem_ponto = False
    tem_digito = False

    while i < len(linha):
        c = linha[i]

        if eh_digito(c):
            tem_digito = True
            i += 1
        elif c == '.':
            if tem_ponto:
                raise ErroLexico(f"Número malformado: '{linha[inicio:i+1]}'")
            tem_ponto = True
            i += 1
        else:
            break

    lexema = linha[inicio:i]

    if not tem_digito:
        raise ErroLexico(f"Número inválido: '{lexema}'")

    if lexema == '.':
        raise ErroLexico("Número inválido: '.'")

    if i < len(linha) and linha[i] == '.':
        raise ErroLexico(f"Número malformado: '{linha[inicio:i+1]}'")

    return Token("NUMBER", lexema), i


def estado_identificador(linha, i):
    inicio = i

    while i < len(linha) and eh_letra(linha[i]):
        i += 1

    lexema = linha[inicio:i]

    if lexema in ("RES", "MEM"):
        return Token("KEYWORD", lexema), i

    if not lexema.isupper():
        raise ErroLexico(
            f"Identificador inválido (use apenas letras maiúsculas): '{lexema}'"
        )

    return Token("IDENT", lexema), i


def estado_operador(linha, i):
    c = linha[i]

    if c == '/':
        if i + 1 < len(linha) and linha[i + 1] == '/':
            return Token("OP", "//"), i + 2
        return Token("OP", "/"), i + 1

    if c in "+-*%^":
        return Token("OP", c), i + 1

    raise ErroLexico(f"Operador inválido: '{c}'")


def estado_inicial(linha, i):
    c = linha[i]

    if c.isspace():
        return None, i + 1

    if c == '(':
        return Token("LPAREN", "("), i + 1

    if c == ')':
        return Token("RPAREN", ")"), i + 1

    if eh_digito(c):
        return estado_numero(linha, i)

    if eh_letra(c):
        return estado_identificador(linha, i)

    if eh_operador_inicio(c):
        return estado_operador(linha, i)

    if c == '.':
        raise ErroLexico("Número inválido: não pode começar apenas com ponto")

    if c == ',':
        raise ErroLexico("Caractere inválido: vírgula não é aceita em números")

    raise ErroLexico(f"Caractere inválido: '{c}'")


def validar_parenteses(tokens):
    saldo = 0

    for token in tokens:
        if token.tipo == "LPAREN":
            saldo += 1
        elif token.tipo == "RPAREN":
            saldo -= 1

            if saldo < 0:
                raise ErroLexico("Parênteses desbalanceados: ')' sem '(' correspondente")

    if saldo != 0:
        raise ErroLexico("Parênteses desbalanceados: faltou fechar '('")


def parseExpressao(linha, _tokens_=None):
    tokens = []
    i = 0

    while i < len(linha):
        token, novo_i = estado_inicial(linha, i)

        if token is not None:
            tokens.append(token)

        i = novo_i

    validar_parenteses(tokens)

    if _tokens_ is not None:
        _tokens_.clear()
        _tokens_.extend(tokens)

    return tokens
