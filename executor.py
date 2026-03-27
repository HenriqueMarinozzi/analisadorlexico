class ErroExecucao(Exception):
    pass


OPERADORES = {"+", "-", "*", "/", "//", "%", "^"}
KEYWORDS = {"RES", "MEM"}


def _eh_numero(valor):
    return isinstance(valor, (int, float))


def _eh_identificador(valor):
    return (
        isinstance(valor, str)
        and valor.isupper()
        and valor not in KEYWORDS
        and valor not in OPERADORES
    )


def _aplicar_operacao(a, b, op):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            raise ErroExecucao("Divisão por zero")
        return a / b
    if op == "//":
        if int(b) == 0:
            raise ErroExecucao("Divisão inteira por zero")
        return int(a) // int(b)
    if op == "%":
        if int(b) == 0:
            raise ErroExecucao("Resto por zero")
        return int(a) % int(b)
    if op == "^":
        return a ** b

    raise ErroExecucao(f"Operador desconhecido: {op}")


def _resolver_folha(item, memoria, historico):
    """Resolve um elemento folha (número, variável ou keyword de leitura)."""
    if _eh_numero(item):
        return float(item)

    if item == "MEM":
        return float(memoria.get("MEM", 0.0))

    if _eh_identificador(item):
        return float(memoria.get(item, 0.0))

    raise ErroExecucao(f"Elemento folha inválido: {item!r}")


def _avaliar_com_pilha(arvore, memoria, historico):
    """
    Avalia uma expressão representada como lista (possivelmente aninhada)
    usando uma pilha explícita para processar os operandos e o operador.

    Estrutura esperada da lista:
      - 1 elemento : leitura de variável  →  [NOME]  ou  [MEM]
      - 2 elementos: atribuição ou RES    →  [valor, NOME]  /  [N, RES]
      - 3 elementos: operação binária     →  [esq, dir, op]
    """
    if not isinstance(arvore, list):
        raise ErroExecucao(f"Expressão inválida: {arvore!r}")

    pilha = []

    # Empurra cada elemento da lista na pilha, resolvendo sub-listas
    # recursivamente (parênteses aninhados geram sub-listas)
    for elemento in arvore:
        if isinstance(elemento, list):
            # Sub-expressão aninhada: avalia recursivamente e empurra resultado
            valor = _avaliar_com_pilha(elemento, memoria, historico)
            pilha.append(valor)
        else:
            pilha.append(elemento)

    # ---------- interpreta o conteúdo da pilha ----------

    if len(pilha) == 1:
        # Leitura simples: (NOME) ou (MEM)
        item = pilha[0]
        return _resolver_folha(item, memoria, historico)

    if len(pilha) == 2:
        esquerda, direita = pilha

        if direita == "RES":
            if not _eh_numero(esquerda):
                raise ErroExecucao("RES exige um número inteiro de linhas anteriores")
            n = int(esquerda)
            if n <= 0:
                raise ErroExecucao("RES exige valor maior que zero")
            if n > len(historico):
                raise ErroExecucao("Não há resultados anteriores suficientes para RES")
            return float(historico[-n])

        if direita == "MEM":
            valor = _resolver_folha(esquerda, memoria, historico)
            memoria["MEM"] = float(valor)
            return float(valor)

        if _eh_identificador(direita):
            valor = _resolver_folha(esquerda, memoria, historico)
            memoria[direita] = float(valor)
            return float(valor)

        raise ErroExecucao(f"Expressão especial inválida: {pilha}")

    if len(pilha) == 3:
        esquerda, direita, operador = pilha

        if operador not in OPERADORES:
            raise ErroExecucao(f"Operador inválido: {operador!r}")

        # Os operandos esquerda/direita já chegam aqui resolvidos (números)
        # quando vinham de sub-listas. Caso sejam folhas ainda não resolvidas
        # (variáveis ou literais), resolvemos agora.
        a = _resolver_folha(esquerda, memoria, historico) if not _eh_numero(esquerda) else float(esquerda)
        b = _resolver_folha(direita, memoria, historico)  if not _eh_numero(direita)  else float(direita)

        return float(_aplicar_operacao(a, b, operador))

    raise ErroExecucao(f"Formato de expressão inválido (tamanho {len(pilha)}): {pilha}")


def executarExpressao(arvore, memoria, historico):
    return _avaliar_com_pilha(arvore, memoria, historico)
