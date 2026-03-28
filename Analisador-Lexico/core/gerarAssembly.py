'''
Evandro Diniz - Github: evdiniz
Henrique Colle Marinozzi - Github: HenriqueMarinozzi
'''

# Verifica se é número float (tem ponto decimal)
def is_float(s):
    return '.' in s  # se contém ponto, consideramos float

# Verifica se pode ser convertido para número
def is_num(s):
    try:
        float(s)  # tenta converter
        return True  # sucesso → é número
    except ValueError:
        return False  # falha → não é número

# atalhos para facilitar uso no código
isf = is_float
isn = is_num

# Cria o estado global usado durante toda a geração
def criarState():
    base_code = [
        ".syntax unified",       # sintaxe moderna ARM
        ".arch_extension idiv",  # habilita instrução SDIV
        ".global _start",
        "_start:"
    ]

    # estrutura central que guarda tudo durante a geração
    return {
        "cod_assembly": base_code,   # lista com código assembly gerado
        "results": {},               # resultados por linha (label + tipo)
        "memory": {},               # variáveis armazenadas (MEM)
        "variables": [],            # lista de variáveis (para seção .data)
        "result_lines": [],         # resultados finais (para seção .data)
        "float_constants": {},      # constantes float reutilizadas
        "float_const_count": 0,     # contador de constantes float
        "pow_count": 0              # contador de loops de potência
    }

# Finaliza o assembly gerando a seção .data
def finalizarAssembly(state):
    codigo = state["cod_assembly"]
    codigo.append("\n.data")  # inicia seção de dados

    # Declara variáveis (MEM)
    for var in state["variables"]:
        codigo.append(f"  addr_{var}: .word 0")  # cada variável vira um endereço

    # Declara resultados das linhas
    for lbl, is_float_val in state["result_lines"]:
        # define tipo dependendo se é float ou inteiro
        tipo = ".float 0.0" if is_float_val else ".word 0"
        codigo.append(f"  {lbl}: {tipo}")

    # Declara constantes float
    for valor, rotulo in state["float_constants"].items():
        # cada constante é armazenada uma única vez
        codigo.append(f"  {rotulo}: .float {valor}")

    # junta tudo em uma string final
    return "\n".join(codigo)

# Implementa operador % (resto)
def gerarMOD(r1, r2, cod_assembly, reg_count):
    reg_tmp = f"r{reg_count[0]}"  # registrador pro quociente
    reg_count[0] += 1

    # r1 % r2 = r1 - (r1/r2)*r2
    # primeiro calcula divisão inteira
    cod_assembly.append(f"  SDIV {reg_tmp}, {r1}, {r2}")
    # depois aplica fórmula do resto
    cod_assembly.append(f"  MLS {r1}, {reg_tmp}, {r2}, {r1}")

# Implementa potência via loop
def gerarPOW(r1, r2, cod_assembly, reg_count, state):
    idx = state["pow_count"]  # ID único do loop
    state["pow_count"] += 1   # incrementa contador global

    reg_acc = f"r{reg_count[0]}"  # acumulador do resultado
    reg_count[0] += 1

    reg_base = f"r{reg_count[0]}"  # guarda base original
    reg_count[0] += 1

    # labels únicos para evitar conflito entre múltiplos POW
    label_loop = f"pow_loop_{idx}"
    label_end = f"pow_end_{idx}"

    cod_assembly.append(f"  MOV {reg_acc}, #1")   # resultado começa em 1
    cod_assembly.append(f"  MOV {reg_base}, {r1}")   # salva base

    cod_assembly.append(f"{label_loop}:")
    cod_assembly.append(f"  CMP {r2}, #0")           # verifica se expoente chegou a 0
    cod_assembly.append(f"  BEQ {label_end}")        # se sim, sai do loop
    cod_assembly.append(f"  MUL {reg_acc}, {reg_acc}, {reg_base}")  # acumula multiplicação
    cod_assembly.append(f"  SUB {r2}, {r2}, #1")     # decrementa expoente
    cod_assembly.append(f"  B {label_loop}")         # volta pro início
    cod_assembly.append(f"{label_end}:")

    return reg_acc  # retorna registrador com resultado

# Converte float (S) → inteiro (r)
def floatParaInt(reg, cod_assembly, alloc_r):
    # converte valor float para inteiro
    cod_assembly.append(f"  VCVT.S32.F32 {reg}, {reg}")
    novo = alloc_r()  # aloca registrador inteiro
    cod_assembly.append(f"  VMOV {novo}, {reg}")  # move valor convertido
    return novo

# aliases para facilitar leitura
f2i = floatParaInt
gmod = gerarMOD
gpow = gerarPOW

# Função principal: gera assembly a partir de tokens RPN
def gerarAssembly(tokens, state, linha_atual):
    stack = []  # pilha de execução (registrador, é_float)

    # contadores de registradores (listas para permitir mutabilidade)
    reg_count = [0]
    vreg_count = [0]

    # atalhos para estruturas do estado
    cod_assembly = state["cod_assembly"]
    memory = state["memory"]
    results = state["results"]
    variables = state["variables"]
    float_constants = state["float_constants"]

    # aloca registrador inteiro
    def alloc_r():
        r = f"r{reg_count[0]}"
        reg_count[0] += 1
        return r

    # aloca registrador float (VFP)
    def alloc_s():
        s = f"S{vreg_count[0]}"
        vreg_count[0] += 1
        return s

    # operações inteiras (mapeamento direto)
    int_operations = {
        "+": "ADD",
        "-": "SUB",
        "*": "MUL",
        "//": "SDIV",
    }

    # operações float (VFP)
    float_operations = {
        "+": "VADD.F32",
        "-": "VSUB.F32",
        "*": "VMUL.F32",
        "/": "VDIV.F32"
    }

    # conjunto de operadores suportados
    all_operations = set(int_operations.keys()) | {"/", "%", "^"}

    # percorre tokens da expressão
    for idx, token in enumerate(tokens):

        # NÚMEROS
        if isn(token):
            if isf(token):  # float
                # evita duplicação de constantes
                if token not in float_constants:
                    rotulo = f"fconst_{state['float_const_count']}"
                    float_constants[token] = rotulo
                    state["float_const_count"] += 1
                else:
                    rotulo = float_constants[token]

                # carrega valor da memória para registrador VFP
                r_addr = alloc_r()
                s_reg = alloc_s()

                cod_assembly.append(f"  LDR {r_addr}, ={rotulo}")
                cod_assembly.append(f"  VLDR {s_reg}, [{r_addr}]")

                stack.append((s_reg, True))  # empilha como float

            else:  # inteiro
                r = alloc_r()
                cod_assembly.append(f"  MOV {r}, #{token}")
                stack.append((r, False))  # empilha como inteiro

        # OPERAÇÕES
        elif token in all_operations:
            # desempilha operandos (ordem importa!)
            b, b_float = stack.pop()
            a, a_float = stack.pop()

            is_float_op = a_float or b_float  # verifica tipo da operação

            # resto
            if token == "%":
                if a_float: a = f2i(a, cod_assembly, alloc_r)
                if b_float: b = f2i(b, cod_assembly, alloc_r)

                gmod(a, b, cod_assembly, reg_count)
                stack.append((a, False))

            # potência
            elif token == "^":
                if a_float: a = f2i(a, cod_assembly, alloc_r)
                if b_float: b = f2i(b, cod_assembly, alloc_r)

                res = gpow(a, b, cod_assembly, reg_count, state)
                stack.append((res, False))

            # divisão inteira
            elif token == "//":
                if a_float: a = f2i(a, cod_assembly, alloc_r)
                if b_float: b = f2i(b, cod_assembly, alloc_r)

                cod_assembly.append(f"  SDIV {a}, {a}, {b}")
                stack.append((a, False))

            # operações float
            elif token == "/" or (is_float_op and token in float_operations):
                # garante que ambos sejam float
                if not a_float:
                    s1 = alloc_s()
                    cod_assembly.append(f"  VMOV {s1}, {a}")
                    cod_assembly.append(f"  VCVT.F32.S32 {s1}, {s1}")
                else:
                    s1 = a

                if not b_float:
                    s2 = alloc_s()
                    cod_assembly.append(f"  VMOV {s2}, {b}")
                    cod_assembly.append(f"  VCVT.F32.S32 {s2}, {s2}")
                else:
                    s2 = b

                s_res = alloc_s()
                instr = float_operations[token]
                cod_assembly.append(f"  {instr} {s_res}, {s1}, {s2}")

                stack.append((s_res, True))

            # operações inteiras simples
            else:
                instr = int_operations[token]
                cod_assembly.append(f"  {instr} {a}, {a}, {b}")
                stack.append((a, False))

        # VARIÁVEIS (MEM)
        elif token.isalpha() and token.isupper() and token != "RES":
            nome = token

            # escrita na variável
            if stack and (tokens[idx-1] == ")" or isn(tokens[idx-1])):
                val_reg, val_float = stack.pop()

                memory[nome] = (f"addr_{nome}", val_float)

                if nome not in variables:
                    variables.append(nome)

                r_addr = alloc_r()
                cod_assembly.append(f"  LDR {r_addr}, =addr_{nome}")

                if val_float:
                    cod_assembly.append(f"  VSTR {val_reg}, [{r_addr}]")
                else:
                    cod_assembly.append(f"  STR {val_reg}, [{r_addr}]")

            # leitura
            else:
                if nome in memory:
                    lbl, is_float_val = memory[nome]

                    if is_float_val:
                        r_addr = alloc_r()
                        s_reg = alloc_s()
                        cod_assembly.append(f"  LDR {r_addr}, ={lbl}")
                        cod_assembly.append(f"  VLDR {s_reg}, [{r_addr}]")
                        stack.append((s_reg, True))
                    else:
                        r = alloc_r()
                        cod_assembly.append(f"  LDR {r}, ={lbl}")
                        cod_assembly.append(f"  LDR {r}, [{r}]")
                        stack.append((r, False))
                else:
                    # variável não inicializada → valor padrão 0
                    r = alloc_r()
                    cod_assembly.append(f"  MOV {r}, #0")
                    stack.append((r, False))

        # RES (resultado anterior)
        elif token == "RES":
            stack.pop()  # remove índice da pilha
            n = int(tokens[idx - 1])
            alvo = linha_atual - n

            # valida se a linha existe
            if alvo not in results:
                raise Exception(f"RES fora do intervalo: linha {alvo} não encontrada")

            lbl, is_float_val = results[alvo]

            # carrega resultado anterior
            if is_float_val:
                r_addr = alloc_r()
                s_reg = alloc_s()
                cod_assembly.append(f"  LDR {r_addr}, ={lbl}")
                cod_assembly.append(f"  VLDR {s_reg}, [{r_addr}]")
                stack.append((s_reg, True))
            else:
                r = alloc_r()
                cod_assembly.append(f"  LDR {r}, ={lbl}")
                cod_assembly.append(f"  LDR {r}, [{r}]")
                stack.append((r, False))

    # SALVA RESULTADO FINAL
    if stack:
        res_reg, res_float = stack[-1]  # topo da pilha
        res_label = f"result_{linha_atual}"
        r_addr = alloc_r()

        cod_assembly.append(f"  LDR {r_addr}, ={res_label}")

        # salva resultado na memória
        if res_float:
            cod_assembly.append(f"  VSTR {res_reg}, [{r_addr}]")
        else:
            cod_assembly.append(f"  STR {res_reg}, [{r_addr}]")

        # registra resultado no estado global
        results[linha_atual] = (res_label, res_float)
        state["result_lines"].append((res_label, res_float))
