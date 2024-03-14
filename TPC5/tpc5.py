import ply.lex as lex
import json
from datetime import datetime
import math

with open("stock.json", 'r') as arquivo:
    bd = json.load(arquivo)

produtos = bd['stock']

saldo_atual = 0



#Moedas
moedas = [("2e",2), ("1e",1), ("50c",0.50), ("20c",0.20), ("10c",0.10), ("5c",0.05), ("2c",0.02), ("1c",0.01)]

def get_value_moeda(m):
    r = None
    for (moeda, valor) in moedas:
        if moeda == m:
            r = valor
    return r

def troco (v):
    v = round(v,2)
    moedas_dict = {}
    for (moeda, valor) in moedas:
        while v>=valor:
            if valor not in moedas_dict.keys():
                moedas_dict[moeda] = 1
            else:
                moedas_dict[moeda] += 1
            v = round(v-valor,2)
    moedas_troco = "Pode retirar o troco: "
    first = True
    for value, number in moedas_dict.items():
        if first:
            moedas_troco += f"{number}x {value}"
            first = False
        else:
            moedas_troco += f", {number}x {value}"
    moedas_troco += "."

    return moedas_troco

def float_para_moedas (valor):
    r = ""
    parte_fracionaria, parte_inteira = math.modf(valor)
    if parte_inteira > 0:
        r += f"{int(parte_inteira)}e"
    if parte_fracionaria > 0:
        r += f"{int(round(parte_fracionaria*100,0))}c"
    if not r:
        r = "0"
    return r

#Lexer
tokens = (
    'LISTAR',
    'DEPOSITAR',
    'SELECIONAR' ,
    'SAIR' ,
    'VIRGULA' ,
    'PONTO' ,
    'MOEDA' ,
    'ID'
)

t_LISTAR = r'LISTAR'
t_DEPOSITAR = r'MOEDA'
t_SELECIONAR =  r'SELECIONAR'
t_SAIR = r'SAIR'
t_VIRGULA = r','
t_PONTO = r'\.'

def t_MOEDA(t):
    r'\d+(e|c)' #docstring
    return t

def t_ID(t):
    r'[A-Z]\d{2}' #docstring
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Carácter ilegal {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()



# Interações da máquina
data_atual = datetime.now().date()
print(f"{data_atual}, Stock carregado, Estado atualizado.")

print("Bom dia. Estou disponível para atender o seu pedido.")

continuar = True
#tok.type, tok.value
while continuar:
    data = input(">> ")
    lexer.input(data)
    tok = lexer.token()
    if tok:
        if tok.type == 'SAIR':
            continuar = False
        elif tok.type == 'LISTAR':
            print ("""cod | nome | quantidade | preço
    ---------------------------------""")
            for p in produtos:
                print(f"{p['cod']} {p['nome']} {p['quant']} {p['preco']}")
        elif tok.type == 'DEPOSITAR':
            sair = False
            more = True
            while not sair and (tok := lexer.token()):
                if tok:
                    if tok.type=='PONTO':
                        sair = True
                    elif tok.type=='MOEDA':
                        found = False
                        for par in moedas:
                            if tok.value == par[0]:
                                saldo_atual+=par[1]
                                found = True
                        if not found:
                            print("O valor inserido não corresponde a uma moeda válida")
                    elif tok.type=='VIRGULA':
                        pass
                    else:
                        print("Input inválido: MOEDA deve ser seguido por uma lista de moedas formadas por um valor inteiro seguido de e ou c conforme se tratem de euros ou cêntimos, respetivamente. Estas devem ser separadas or vírgulas e a lista deve terminar em ponto final")
                else:
                    print("Input inválido: MOEDA deve ser seguido por uma lista de moedas formadas por um valor inteiro seguido de e ou c conforme se tratem de euros ou cêntimos, respetivamente. Estas devem ser separadas or vírgulas e a lista deve terminar em ponto final")
            print(f"Saldo = {float_para_moedas(saldo_atual)}")
                        
        elif tok.type == 'SELECIONAR':
            tok = lexer.token()
            if tok:
                if tok.type == 'ID':
                    found = False
                    for p in produtos:
                        if p['cod'] == tok.value:
                            found = True
                            if saldo_atual >= p['preco']:
                                saldo_atual -= p['preco']
                                parte_fracionaria, parte_inteira = math.modf(saldo_atual)
                                print (f"Saldo = {float_para_moedas(saldo_atual)}")
                            else:
                                print("Saldo insufuciente para satisfazer o seu pedido")
                                print (f"Saldo = {float_para_moedas(saldo_atual)}; Pedido = {float_para_moedas(p['preco'])}")
                    if not found:
                        print ("O artigo selecionado não existe")
                else:
                    print("Input inválido: SELECIONAR deve ser seguido pelo id de um produto")
            else:
                print("Input inválido: SELECIONAR deve ser seguido pelo id de um produto")
        else:
            print("Input inválido")
    else:
        print("Input inválido")
    


if saldo_atual>0:
    print(troco(saldo_atual))
else:
    print("Não há troco para ser devolvido")

bdw = {}
bdw['stock'] = produtos

with open("stock.json", 'w') as arquivo:
    json.dump(bdw, arquivo, indent=2)

print("Até à próxima")