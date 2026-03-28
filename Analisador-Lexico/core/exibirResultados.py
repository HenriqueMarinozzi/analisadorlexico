'''
Evandro Diniz - Github: evdiniz
Henrique Colle Marinozzi - Github: HenriqueMarinozzi
'''

'''
Evandro Diniz - Github: evdiniz
Henrique Colle Marinozzi - Github: HenriqueMarinozzi
'''

def exibirResultados(resultados):
    # Exibe os resultados das expressões processadas
    if not resultados:
        print("\n[!] Nenhum resultado encontrado.\n")
        return

    print("\n" + "="*40)
    print("        RESULTADOS DO PROGRAMA")
    print("="*40)

    # Percorre resultados ordenados por linha
    for linha in sorted(resultados):
        resultado = resultados[linha]
        try:
            # Formata saída: inteiro ou float
            if float(resultado).is_integer():
                print(f"│ Linha {linha:02d} │ Resultado: {int(float(resultado))}")
            else:
                print(f"│ Linha {linha:02d} │ Resultado: {float(resultado):.1f}")
        except:
            # Caso não seja possível converter (erro simbólico)
            print(f"│ Linha {linha:02d} │ Resultado: ERRO")

    print("="*40 + "\n")

