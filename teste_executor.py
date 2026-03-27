from lexer import parseExpressao
from parser import construir_arvore
from executor import executarExpressao

linhas = [
    "(3.0 2.0 +)",
    "((3.0 2.0 +) (4.0 5.0 *) /)",
    "(10.5 VAR)",
    "(VAR)",
    "(1 RES)",
    "(8 2 //)",
    "(9 4 %)",
    "(2 3 ^)",
    "(10.0 3.0 -)",
    "(7.5 MEM)",
    "(MEM)",
]

memoria = {}
historico = []

for i, linha in enumerate(linhas, start=1):
    tokens = parseExpressao(linha)
    arvore = construir_arvore(tokens)
    resultado = executarExpressao(arvore, memoria, historico)
    historico.append(resultado)

    print(f"Linha {i}: {linha}")
    print("Tokens:", tokens)
    print("Árvore:", arvore)
    print("Resultado:", resultado)
    print("Memória:", memoria)
    print("Histórico:", historico)
    print("-" * 60)
