'''
Evandro Diniz - Github: evdiniz
Henrique Colle Marinozzi - Github: HenriqueMarinozzi
'''

from core.gerarAssembly import is_num

def executarExpressao(tokens: list[str], memoria: dict[str, float], resultados: dict[int, float], linha_atual: int):
    
    operacoes = {"+", "-", "*", "/", "//", "%", "^"}
    stack = []

    # função auxiliar de cálculo
    def aplicar_operacao(a, b, op):
        if op == "+":
            return a + b
        elif op == "-":
            return a - b
        elif op == "*":
            return a * b
        elif op == "/":
            return a / b
        elif op == "//":
            return a // b
        elif op == "%":
            return a % b
        elif op == "^":
            return a ** b

    for idx, token in enumerate(tokens):

        # número → empilha
        if is_num(token):
            stack.append(float(token))

        # operador → aplica nos dois últimos valores
        elif token in operacoes:
            b = stack.pop()
            a = stack.pop()
            stack.append(aplicar_operacao(a, b, token))

        # RES → busca resultado anterior
        elif token == "RES":
            if stack:
                offset = int(stack.pop())
                linha_ref = linha_atual - offset

                if offset > 0 and linha_ref in resultados:
                    stack.append(resultados[linha_ref])

        # variáveis (MEM)
        elif token.isalpha() and token.isupper():
            
            # escrita
            if stack and (tokens[idx - 1] == ")" or is_num(tokens[idx - 1])):
                valor = stack.pop()
                memoria[token] = valor
            else:
                # leitura
                stack.append(memoria.get(token, 0.0))

    # salva resultado final
    if stack:
        resultados[linha_atual] = stack.pop()


def testes_executarExpressao():
    testes = [
        ['(', '3.14', '2.0', '+', ')'],
        ['1', 'RES'],
        ['(', '(', '1.5', '2.0', '*', ')', '(', '3.0', '4.0', '*', ')', '/', ')'],
        ['(', '5.0', 'MEM', ')'],
        ['(', '2', 'RES', ')'],
        ['(', '10.5', 'CONTADOR', ')', 'CONTADOR'],
        ["(", "15.5", "4.2", "*", ")", "(", "10", "5", "+", ")", "/"],
        ["(", "10", "2", "^", ")", "(", "50", "5", "//", ")", "(", "1", "RES", "10", "%", ")", "+", "+"],
        ["(", "25.5", "10.5", "+", ")", "(", "3.14", "MI", "MI", ")", "*"],
        ["(", "(", "8", "2", "/", ")", "(", "3", "1", "-", ")", "*", ")", "(", "100", "50", "%", ")", "+"],
        ["100", "(", "(", "5", "2", "%", ")", "(", "10", "2", "*", ")", "+", ")", "/"],
        ['(', '10.5', 'MI', ')'],
        ['(', '(', '3', '9', '/' ,')', ')'],
        ['(', '(', '2', '2', '^', ')', '(', '5', '10', '+', ')', '+', ')'],
        ['(', '5', '(', 'MI', ')', '+', ')']
    ]
    linha = 1
    memoria = {}
    resultados = {}

    for teste in testes:
        executarExpressao(teste, memoria, resultados, linha)
        linha += 1

    print(resultados)
    print(memoria)
