from lexer import parseExpressao, ErroLexico

entradas_validas = [
    "(3.14 2.0 +)",
    "(5 RES)",
    "(10.5 CONTADOR)",
    "(VAR)",
    "((3.0 2.0 +) (4.0 5.0 *) /)",
    "(8 2 //)",
    "(9 4 %)",
    "(2 3 ^)",
    "(6.0 3.0 -)",
    "(7.5 MEM)",
    "(MEM)",
]

entradas_invalidas = [
    "(3.14.5 2.0 +)",
    "(3,45 2.0 +)",
    "(3.0 2.0 &)",
    "(contador)",
    "(3.0 2.0 +",
    "3.0 2.0 +)",
]

print("=== TESTES VÁLIDOS ===")
for entrada in entradas_validas:
    try:
        tokens = parseExpressao(entrada)
        print(entrada)
        print(tokens)
        print()
    except ErroLexico as e:
        print(f"ERRO inesperado em válida: {entrada} -> {e}")

print("=== TESTES INVÁLIDOS ===")
for entrada in entradas_invalidas:
    try:
        tokens = parseExpressao(entrada)
        print(f"ERRO: deveria falhar, mas passou -> {entrada}")
        print(tokens)
    except ErroLexico as e:
        print(entrada)
        print(f"Erro detectado corretamente: {e}")
        print()
