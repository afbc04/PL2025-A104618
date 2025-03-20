from lexico import lexer
from nodo import *

proximoSimbolo = ('Erro', '', 0, 0)

def parserError(s):
    print("Erro sintático, token inesperado: ",s)

#Reconhece Números
def rec_NUMERO():
    global proximoSimbolo
    
    #Se for um número, extrai valor
    if proximoSimbolo.type == 'NUMERO':

        numero = int(proximoSimbolo.value)
        proximoSimbolo = lexer.token() #Avançar char
        return Nodo(False,numero)
    
    #Não é um número
    else:
        parserError(proximoSimbolo)
        return Nodo()

#Reconhece Operadores * /
def rec_MULDIV():
    global proximoSimbolo
    
    #Se for um operador, extrai
    if proximoSimbolo.type == 'MULDIV':

        op = proximoSimbolo.value
        proximoSimbolo = lexer.token() #Avança char
        return op
    
    #Não é um operador
    else:
        parserError(proximoSimbolo)
        return ""

#Reconhece Operadores + -
def rec_SOMSUB():
    global proximoSimbolo
    
    #Se for operador, extrai
    if proximoSimbolo.type == 'SOMSUB':

        op = proximoSimbolo.value
        proximoSimbolo = lexer.token() #Avnça char
        return op
    
    #Não é um operador
    else:
        parserError(proximoSimbolo)
        return ""

# Regra-1 => INIT = ExpMULDIVInit ExpSOMSUB
def rec_INIT():
    global proximoSimbolo

    numero = rec_ExpMULDIVInit() #Extrair valor
    return rec_ExpSOMSUB(numero) #Calcular expressão com o número calculado

# Regra-2 => ExpSOMSUB = SOMSUB ExpMULDIVInit ExpSOMSUB
# Regra-3 =>           =
def rec_ExpSOMSUB(valor_esquerda):
    global proximoSimbolo

    # Regra-3
    if proximoSimbolo is None: #Acabou os tokens
        return valor_esquerda #Mantem valor
    
    # Regra-2
    elif proximoSimbolo.type == 'SOMSUB':
        
        operador = rec_SOMSUB()
        valor_direita = rec_ExpMULDIVInit()
        expressao = Exp(operador,valor_esquerda,valor_direita)
        
        return rec_ExpSOMSUB(expressao)

    #Não entra em nenhuma regra e ainda há tokens
    else:
        parserError(proximoSimbolo)
        return valor_esquerda

# Regra-4 => ExpMULDIVInit = NUMERO ExpMULDIV
def rec_ExpMULDIVInit():
    global proximoSimbolo
    
    numero = rec_NUMERO() # Extrai número
    return rec_ExpMULDIV(numero)

# Regra-5 => ExpMULDIV = MULDIV NUMERO ExpMULDIV
# Regra-6 =>           =
def rec_ExpMULDIV(valor_esquerda):
    global proximoSimbolo

    # Regra-6
    if proximoSimbolo is None or proximoSimbolo.type == 'SOMSUB':
        return valor_esquerda
    
    # Regra-5
    elif proximoSimbolo.type == 'MULDIV':

        operador = rec_MULDIV()
        valor_direita = rec_NUMERO()
        expressao = Exp(operador,valor_esquerda,valor_direita)
        
        return rec_ExpMULDIV(expressao)

    #Não entra em nenhuma regra e ainda há tokens
    else:
        parserError(proximoSimbolo)
        return valor_esquerda

#Função que faz o parser dos tokens
def sintaticoParser(input):
    global proximoSimbolo
    
    lexer.input(input)
    proximoSimbolo = lexer.token() #Iniciar
    return rec_INIT()
    