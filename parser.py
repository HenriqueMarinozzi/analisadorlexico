class ErroSintatico(Exception):
    pass


def _converter_token_para_valor(token):
    if token.tipo == "NUMBER":
        return float(token.valor)

    if token.tipo in ("IDENT", "KEYWORD", "OP"):
        return token.valor

    raise ErroSintatico(f"Token inesperado no parser: {token}")


def _parse_lista(tokens, i):
    if i >= len(tokens) or tokens[i].tipo != "LPAREN":
        raise ErroSintatico("Esperado '(' no início da expressão")

    i += 1
    elementos = []

    while i < len(tokens) and tokens[i].tipo != "RPAREN":
        token_atual = tokens[i]

        if token_atual.tipo == "LPAREN":
            subexpr, i = _parse_lista(tokens, i)
            elementos.append(subexpr)
        else:
            elementos.append(_converter_token_para_valor(token_atual))
            i += 1

    if i >= len(tokens) or tokens[i].tipo != "RPAREN":
        raise ErroSintatico("Esperado ')' no fim da expressão")

    i += 1
    return elementos, i


def construir_arvore(tokens):
    if not tokens:
        raise ErroSintatico("Linha vazia ou sem tokens")

    arvore, i = _parse_lista(tokens, 0)

    if i != len(tokens):
        raise ErroSintatico("Há tokens sobrando após o fim da expressão")

    return arvore
