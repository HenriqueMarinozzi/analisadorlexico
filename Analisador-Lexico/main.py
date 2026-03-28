'''
Evandro Diniz - Github: evdiniz
Henrique Colle Marinozzi - Github: HenriqueMarinozzi
'''

import sys
import os

from core.lerExpressao import ler_expressao
from core.parseExpressao import parseExpressao
from core.gerarAssembly import gerarAssembly, criarState, finalizarAssembly
from core.exibirResultados import exibirResultados
from core.executarExpressao import executarExpressao


def main():
    # Verifica se o caminho do arquivo foi passado como argumento
    if len(sys.argv) < 2:
        print("Caminho do arquivo não encontrado")
        return

    caminho = sys.argv[1]

    # Verifica se o arquivo existe
    if not os.path.isfile(caminho):  # pequena mudança aqui
        print("Arquivo inexistente!")
        return

    # Lê o conteúdo do arquivo de entrada
    arq = ler_expressao(caminho)

    # Verifica se o arquivo está vazio ou inválido
    if not arq:
        print("Arquivo incorreto ou vazio!")
        return

    # Estruturas auxiliares
    memoria = {}        # Armazena variáveis (MEM)
    resultados = {}     # Histórico de resultados (RES)
    linha = 1           # Contador de linhas
    all_tokens = []     # Armazena tokens para salvar em arquivo

    # Estado inicial do gerador de Assembly
    state = criarState()

    # (Leitura repetida - poderia ser removida, mas mantida para compatibilidade)
    caminho = sys.argv[1]
    arq = ler_expressao(caminho)

    # Processa cada linha do arquivo
    for linha_texto in arq:  # renomeado "line"
        # Análise léxica (gera tokens via AFD)
        tokens_linha = parseExpressao(linha_texto)

        # Simula execução (SEM realizar cálculos - apenas controle)
        executarExpressao(tokens_linha, memoria, resultados, linha)

        # Gera código Assembly correspondente à expressão
        gerarAssembly(tokens_linha, state, linha)

        # Salva tokens da linha
        all_tokens.append(tokens_linha)

        linha += 1

    # Salva tokens da última execução em arquivo
    with open("tokens.txt", "w", encoding="utf-8") as f:
        for tks in all_tokens:  # leve mudança no nome
            f.write(f"{tks}\n")  # pequena mudança de escrita

    # Finaliza e obtém o código Assembly completo
    assembly_code = finalizarAssembly(state)

    # Salva o Assembly gerado
    with open("saida.s", "w", encoding="utf-8") as f:
        f.write(assembly_code)

    # Exibe resultados simulados
    exibirResultados(resultados)


if __name__ == "__main__":
    main()
