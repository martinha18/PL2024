import sys
import ply.lex as lex
import ply.yacc as yacc
import re

#------------------------------------------------
#--------------- Análise Léxica -----------------
#------------------------------------------------

tokens = (
    'INT',
    'MOD',
    'COMMENT',
    'PRINT',
    'CHAR',
    'EMIT',
    'NOME',
    'VARIABLE',
    'MAIORIGUAL',
    'MENORIGUAL',
    'IF',
    'THEN',
    'ELSE',
    'BEGIN',
    'UNTIL',
    'WHILE',
    'REPEAT',
    'DO',
    'LOOP',
    'LOOPN',
    'VALUE',
    'TO',
    'LOCALS',
    'SPACES',
    'I'
)

literals = ['+', ':', '-', '/', '*', '.', ';', '!', '>', '<', '@', '|', '=']


def t_I(t):
    r'(?i:i)\b'
    return t


def t_VALUE(t):
    r'\b(?i:value)\b'
    return t


def t_VARIABLE(t):
    r'\b(?i:variable)\b'
    return t


def t_SPACES(t):
    r'\b(?i:spaces)\b'
    return t


def t_TO(t):
    r'\b(?i:to)\b'
    return t


def t_LOCALS(t):
    r'\b(?i:locals)'
    return t


def t_CHAR(t):
    r'\b(?i:char\s([^\s]+))'
    t.value = t.value[5:]
    return t


def t_EMIT(t):
    r'\b(?i:emit)\b'
    return t


def t_INT(t):
    r'[+-]?\d+\b'
    t.value = int(t.value)
    return t


def t_MOD(t):
    r'\b(?i:mod)\b'
    return t


def t_COMMENT(t):
    r'(\( [\s\S]*?\))|(\\[^\n]*)'
    pass


def t_PRINT(t):
    r'( \.\( [\s\S]*?\))|( \." [\s\S]*?")'
    t.value = t.value[3:-1]
    return t


def t_MAIORIGUAL(t):
    r'>='
    return t


def t_MENORIGUAL(t):
    r'<='
    return t


def t_LOOPN(t):
    r'\s*(?i:\+loop)\s*'
    return t


def t_LOOP(t):
    r'\b(?i:loop)\b'
    return t


def t_BEGIN(t):
    r'\b(?i:begin)\b'
    return t


def t_UNTIL(t):
    r'\b(?i:until)\b'
    return t


def t_WHILE(t):
    r'\b(?i:while)\b'
    return t


def t_REPEAT(t):
    r'\b(?i:repeat)\b'
    return t


def t_DO(t):
    r'\b(?i:do)\b'
    return t


def t_IF(t):
    r'\b(?i:if)\b'
    return t


def t_ELSE(t):
    r'\b(?i:else)\b'
    return t


def t_THEN(t):
    r'\b(?i:then)\b'
    return t


def t_NOME(t):
    r'(\w[\w-]*)'
    return t

t_ignore = ' \t\n'


def t_error(t):
    print(f"Carácter ilegal {t.value[0]}")
    t.lexer.skip(1)


lexer = lex.lex()

def lexer_debug(dados):
    lexer.input(dados)
    while token := lexer.token():
        print(token)


#lexer_debug(data2)

#---------------------------------------------------------------
#--------------- Análise Sintática e Semântica -----------------
#---------------------------------------------------------------

func_dict = {
    '>': 'SUP\n',
    '<': 'INF\n',
    '=': 'EQUAL\n',
    '>=': 'SUPEQ\n',
    '<=': 'INFEQ\n',
    'dup': 'DUP 1\n',
    'swap': 'SWAP\n',
    'drop': 'POP 1\n',
    'over': 'PUSHSP\nLOAD -1\n',
    '2dup': 'PUSHSP\nLOAD -1\nPUSHSP\nLOAD -1\n',
    '2over': 'PUSHSP\nLOAD -3\nPUSHSP\nLOAD -3\n',
    '2drop': 'POP 2\n',
    'cr': 'WRITELN\n',
    'key': 'READ \npushi 0 \nCHARAT\n',
    'space': 'pushs " "\nwrites\n',
}

variable_dict = {}
loop_dict = {}
locals_dict = {}
value_dict = {}

posicao_memoria = 0

ifs = 0
def incIfs():
    global ifs
    ifs += 1
def getIfs():
    global ifs
    return ifs


begins = 0
def incBegins():
    global begins
    begins += 1
def getBegins():
    global begins
    return begins


dos = 0
def incDos():
    global dos
    dos += 1
def getDos():
    global dos
    return dos

func_atual = "main"
function_count = 0

# Produções gramaticais
def p_forth(t): "forth : funcs"; t[0] = aloca_variaveis() + 'START\n' + t[1] + 'STOP\n'


def p_funcs(t): "funcs : funcs funcao"; t[0] = t[1] + t[2]
def p_funcs1(t): "funcs : funcao"; t[0] = t[1]


def p_ciclos1(t): "ciclos : ciclos funcs is"; t[0] = t[1] + [t[2]] + t[3]
def p_ciclos2(t): "ciclos : is"; t[0] = t[1]


def p_is1(t): "is : I"; t[0] = ['i']
def p_is2(t): "is : "; t[0] = []


def p_funcao1(t): "funcao   : ':' nomefunc funcs pontoVirgula "; t[0] = ""; func_def_unica(t[2].lower(), t[3])
def p_funcao2(t): "funcao   : ':' nomefunc vars funcs pontoVirgula "; t[0] = ""; func_def_unica(t[2].lower(),t[4])
def p_funcao3(t): "funcao : operacoes"; t[0] = t[1]
def p_funcao4(t): "funcao : IF funcs THEN"; incIfs(); t[0] = f'jz then{getIfs()}\n' + t[2] + f'then{getIfs()}:\n'
def p_funcao5(t): "funcao : IF funcs ELSE funcs THEN"; incIfs(); t[0] = f'jz else{getIfs()}\n' + t[2] + f'jump then{getIfs()}\nelse{getIfs()}:\n' + t[4] + f'then{getIfs()}:\n'
def p_funcao6(t): "funcao : BEGIN funcs UNTIL"; incBegins(); t[0] = f'begin{getBegins()}:\n' + t[2] + f'\njz begin{getBegins()}\n'
def p_funcao7(t): "funcao : BEGIN funcs WHILE funcs REPEAT"; incBegins(); t[0] = f'begin{getBegins()}:\n' + t[2] + f'\njz end{getBegins()}\n' + t[4] + f'\njump begin{getBegins()}\nend{getBegins()}:\n'
def p_funcao8(t): "funcao : DO ciclos LOOP"; incDos(); add_loop_dict(f'index{getDos()}'); add_loop_dict(f'limit{getDos()}'); t[0] = f"{define_loop_dict(f'index{getDos()}')}{define_loop_dict(f'limit{getDos()}')}while{getDos()}:\n" + colocaIs(t[2]) + f"{get_loop_dict(f'index{getDos()}')}pushi 1\nadd\n{define_loop_dict(f'index{getDos()}')}{get_loop_dict(f'index{getDos()}')}{get_loop_dict(f'limit{getDos()}')}supeq\njz while{getDos()}\n"
def p_funcao9(t): "funcao : DO ciclos LOOPN"; incIfs(); incDos();add_loop_dict(f'index{getDos()}');add_loop_dict(f'limit{getDos()}'); t[0] = f"{define_loop_dict(f'index{getDos()}')}{define_loop_dict(f'limit{getDos()}')}while{getDos()}:\n" + colocaIs(t[2]) + f"dup 1\n{get_loop_dict(f'index{getDos()}')}add\n{define_loop_dict(f'index{getDos()}')}pushi 0\ninf\njz else{getIfs()}\n{get_loop_dict(f'index{getDos()}')}{get_loop_dict(f'limit{getDos()}')}infeq\njump then{getIfs()}\nelse{getIfs()}:\n{get_loop_dict(f'index{getDos()}')}{get_loop_dict(f'limit{getDos()}')}supeq\nthen{getIfs()}:\njz while{getDos()}\n"


def p_nomefunc(t): "nomefunc : NOME"; t[0] = t[1]; global func_atual; func_atual = t[1]


def p_pontoVirgula(t): "pontoVirgula : ';' "; t[0] = ""; global func_atual; func_atual = "main"


def p_vars1(t): "vars : vars var  "; t[0] = t[1] + t[2]
def p_vars2(t): "vars : var"; t[0] = t[1]


def p_var1(t): "var : LOCALS '|' nomes '|' "; t[0] = t[3]; t[0] = adicionarVarsLocais(t[3])


def p_nomes1(t): "nomes : NOME"; t[0] = [t[1]]
def p_nomes2(t): "nomes : nomes NOME"; t[0] = t[1] + [t[2]]


def p_operacoesAri(t): "operacoes  : fator"; t[0] = t[1]
def p_operacoesAri1(t): "operacoes  : operacoes fator"; t[0] = t[1] + t[2]


def p_fator(t): "fator   : INT      "; t[0] = f'pushi {t[1]}\n'
def p_fator1(t): "fator   : '+'      "; t[0] = "ADD\n"; global func_atual
def p_fator2(t): "fator   :  '-'     "; t[0] = "SUB\n"
def p_fator3(t): "fator   : '*'      "; t[0] = "MUL\n"
def p_fator4(t): "fator   : '/'      "; t[0] = "DIV\n"
def p_fator5(t): "fator   : '='      "; t[0] = func_dict['=']
def p_fator6(t): "fator   : '>'      "; t[0] = func_dict['>']
def p_fator7(t): "fator   : '<'      "; t[0] = func_dict['<']
def p_fator8(t): "fator   : MAIORIGUAL "; t[0] = func_dict['>=']
def p_fator9(t): "fator   : MENORIGUAL "; t[0] = func_dict['<=']
def p_fator10(t): "fator   : MOD      "; t[0] = "MOD\n"
def p_fator11(t): "fator   :  '.'    "; t[0] = 'writei\npushs " "\nwrites\n'
def p_fator12(t): "fator   :  PRINT   "; t[0] = f'pushs "{t[1]} "\nwrites\n'
def p_fator13(t): "fator   :  EMIT    "; t[0] = f'WRITECHR\n'
def p_fator14(t): "fator   :  COMMENT "; t[0] = ""
def p_fator15(t): "fator   :   CHAR    ";  t[0] = f'pushs "{t[1]}"\nCHRCODE\n'
def p_fator16(t): "fator   :   VARIABLE NOME";  t[0] = ""; dupl_dict(t[2]); aloca_variable_dict(t[2])
def p_fator17(t): "fator   :   NOME '!'";  t[0] = define_variable_dict(t[1])
def p_fator18(t): "fator   :  NOME "; t[0] = verificar_tipo_variavel(t[1])
def p_fator19(t): "fator   :  NOME '@'    ";  t[0] = valor_variavel(t[1])
def p_fator20(t): "fator   :   VALUE NOME"; dupl_dict(t[2]); t[0] = define_value_dict(t[2])
def p_fator21(t): "fator   :   TO NOME     ";  t[0] = altera_value(t[2])
def p_fator22(t): "fator   :   INT   SPACES   ";  t[0] = func_espaco(t[1])


def p_error(t):
    if t is not None:
        print(f"Erro sintático {t.value} {t}")
    else:
        raise Exception(f"A expressão não é compativel com a gramática")


# Funções auxiliares
def colocaIs(lista):
    value = get_loop_dict(f'index{getDos()}')
    s = ''
    for elem in lista:
        if elem == 'i':
            s+=value
        else:
            s+=elem
    return s


def tamanhoVarsLocais():
    tamanho = 0
    for listaVars in locals_dict.values():
        tamanho += len(listaVars)

    return tamanho


def aloca_variaveis():
    n = 0
    n += len(value_dict.keys())
    n += len(variable_dict.keys())
    n += tamanhoVarsLocais()
    n += len(loop_dict.keys())

    variaveis = ""
    for _ in range(n):
        variaveis += 'pushi 0\n'

    return variaveis


def change_labels(codigo):
    global function_count
    function_count += 1
    new = re.sub(r'(if|else|then|begin|end|while)\d+', lambda match: match.group(0)+'f'+str(function_count), codigo)
    return new


def adicionarVarsLocais(vars):
    global func_atual
    # Verificar se não existem variaveis repetidas
    if len(set(vars)) == len(vars):
        # Não existem repetições, alocar posição mem
        variaveis = []
        for var in vars:
            global posicao_memoria
            par = (var, posicao_memoria)
            variaveis.append(par)
            posicao_memoria += 1
            
        locals_dict[func_atual.lower()] = variaveis
    else:
        # Existem repetições
        raise Exception(f"Erro: Variávies locais com nomes repetidos")


def func_def_unica(nome, resultlado):
    if nome.lower() in func_dict:
        raise Exception(f"Erro: Função {nome} já declarada")
    else:
        func_dict[nome.lower()] = resultlado


def func_espaco(espaco):
    space = ''
    for i in range(espaco):
        space += ' '
    result = f'\npushs "{space}"\nwrites\n'
    return result


def dupl_dict(nome):
    if nome.lower() in func_dict:
        raise Exception(f"Erro: Nome {nome} já declarada para uma função")
    elif nome in variable_dict:  # QUANDO EXISTIREM OS OUTROS DICIONÁRIOS DEVE-SE VERIFICAR NOS OUTROS DICIONÁRIOS
        raise Exception(f"Aviso: Variável com alocação {nome} já declarada")
    elif nome in value_dict:
        raise Exception(f"Aviso: Variável com Value {nome} já declarado")


def define_value_dict(nome):
    global  func_atual

    if nome.lower() in func_dict:
        raise Exception(f"Erro: Este nome já foi utilizado para uma função {func_dict}")
    elif func_atual != "main" and func_atual.lower() in locals_dict:
        vars = locals_dict[func_atual.lower()]
        encontrei = False
        for item in vars:
            if item[0] == nome:
                encontrei = True
        if encontrei == True:
            raise Exception(f"Erro: {nome} é uma variável local, não pode ser declarada com VALUE")

    global posicao_memoria

    value_dict[nome] = posicao_memoria
    posicao_memoria += 1
    return f'storeg {value_dict[nome]}\n'


def altera_value(nome):
    global func_atual

    if nome in variable_dict and func_atual == "main":
        raise Exception(f"Erro: Variável {nome} alocada não pode ser alterada com TO")
    elif nome not in value_dict and func_atual == "main":
        raise Exception(f"Erro: Valor {nome} não declarado")
    elif nome.lower() in func_dict and func_atual == "main":
        raise Exception(f"Erro: {nome} é uma função, não pode ser usada como variável")
    elif func_atual != "main" and func_atual.lower() in locals_dict:
        vars = locals_dict[func_atual.lower()]
        encontrei = False
        posicao_memoria= None
        for item in vars:
            if item[0] == nome:
                encontrei = True
                posicao_memoria = item[1]
        if encontrei == False:
            if nome not in value_dict:
                raise Exception(f"Erro: {nome} é uma variável local que não existe")
            else:
                posicao_memoria = value_dict[nome]
    else:
        posicao_memoria = value_dict[nome]
    return f'storeg {posicao_memoria}\n'


def aloca_variable_dict(nome):
    global func_atual

    if nome.lower() in func_dict:
        raise Exception(f"Erro: Este nome já foi utilizado para uma função {func_dict}")
    elif func_atual != "main" and func_atual.lower() in locals_dict:
        vars = locals_dict[func_atual.lower()]
        encontrei = False
        for item in vars:
            if item[0] == nome:
                encontrei = True
        if encontrei == True:
            raise Exception(f"Erro: {nome} é uma variável local, não pode ser declarada com VARIABLE")

    global posicao_memoria

    variable_dict[nome] = (posicao_memoria, False)
    posicao_memoria += 1


def define_variable_dict(nome):
    global func_atual
    encontrei = False

    if nome.lower() in func_dict:
        raise Exception(f"Erro: {nome} é uma função, não pode ser usada como variável alocada")
    elif nome not in variable_dict:
        raise Exception(f"Erro: Variável alocada {nome} não declarada")
    elif func_atual != "main" and func_atual.lower() in locals_dict:
        vars = locals_dict[func_atual.lower()]
        encontrei = False
        for item in vars:
            if item[0] == nome:
                encontrei = True
        if encontrei == True:
            raise Exception(f"Erro: {nome} é uma variável local, operação inválida (!)")
    if encontrei == False:
        posicao_memoria, _ = variable_dict[nome]
        variable_dict[nome] = (posicao_memoria, True)

    return f'storeg {variable_dict[nome][0]}\n'


def verificar_tipo_variavel(nome):
    nome = nome.lower()
    global func_atual
    result = ""
    encontrei = False
    if func_atual != "main" and func_atual.lower() in locals_dict:
        vars = locals_dict[func_atual.lower()]
        encontrei = False
        for item in vars:
            if item[0] == nome:
                result = f'pushg {item[1]}\n'
                encontrei = True
    if nome.lower() in func_dict and not encontrei:
        if func_atual == "main":
            if nome.lower() in locals_dict:
                for vars in locals_dict[nome.lower()]:
                    result += "storeg " + str(vars[1]) + "\n"
        result += change_labels(func_dict[nome.lower()])
    if nome in variable_dict and encontrei == False:
        result = f'pushi {variable_dict[nome][0]}\n'
    if nome in value_dict and encontrei == False:
        result = f'pushg {value_dict[nome]}\n'
    if result == "":
        raise Exception(f"Erro: Variável/Função {nome} não declarada")
    return result


def valor_variavel(nome):
    result = ""
    global func_atual
    encontrei = False
    if func_atual != "main" and func_atual.lower() in locals_dict:
        vars = locals_dict[func_atual.lower()]
        encontrei = False
        for item in vars:
            if item[0] == nome:
                encontrei = True
        if encontrei == True:
            raise Exception(f"Erro: {nome} é uma variável local, não pode ser alocada")
    if nome.lower() in func_dict and encontrei == False:
        raise Exception(f"Erro: {nome} é uma função, não pode ser usada como variável")
    if nome in variable_dict and encontrei == False:
        if variable_dict[nome][1]:
            result = f'pushg {variable_dict[nome][0]}\n'
        else:
            result = f'pushi {0}\n'
    else:
        # Verificar depois os dois outros diccionários
        raise Exception(f"Erro: Variável {nome} não alocada")

    return result


def add_loop_dict(nome):
    global posicao_memoria
    loop_dict[nome] = posicao_memoria
    posicao_memoria += 1


def define_loop_dict(nome):
    result = ""
    if nome not in loop_dict:
        raise Exception(f"Erro: {nome} os loops estão mal")
    else:
        result = f'storeg {loop_dict[nome]}\n'

    return result


def get_loop_dict(nome):
    result = ""
    if nome not in loop_dict:
        raise Exception(f"Erro: {nome} os loops estão mal 2")
    else:
        result = f'pushg {loop_dict[nome]}\n'
    return result




# Funções de leitura e escrita em arquivos
def processar_arquivo(nome_arquivo):
    result = ""
    try:
        with open(nome_arquivo, 'r') as arquivo:
            for linha in arquivo:
                linha = linha.strip()  # Remover espaços em branco adicionais
                if linha:
                    result += linha + '\n'
        return result
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {e}")
        sys.exit(1)


def escreve_ficheiro (data):
    parser = yacc.yacc()
    codigoVM = parser.parse(data)
    if codigoVM:
        with open("./codigovm.ewvm", 'w') as file:
            file.write(codigoVM)
    else:
        print("Erro: não foi possível obter o código VM")


# MAIN 
def main():

    if len(sys.argv) != 2:
        sys.exit(1)
    nome_arquivo = sys.argv[1]
    print(f"A processar o arquivo '{nome_arquivo}'")
    data = processar_arquivo(nome_arquivo)
    #lexer_debug(data) 
    escreve_ficheiro(data)
    print ("Código VM gerado para o ficheiro codigovm.ewvm")


if __name__ == "__main__":
    main()