'''
Evandro Diniz - Github: evdiniz
Henrique Colle Marinozzi - Github: HenriqueMarinozzi
'''

def ler_expressao(nomeArquivo):
    try:
        # abre o arquivo e já garante fechamento automático
        with open(nomeArquivo, "r") as file:
            # lê todas as linhas removendo \n
            linhas = [linha.rstrip("\n") for linha in file]

        return linhas
    
    except FileNotFoundError:
        # erro caso o arquivo não exista
        print("O arquivo não existe!")
        return []  # evita retornar None
