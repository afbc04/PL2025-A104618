import sys
import re

#Função que cria tokens a partir de uma string
def tokenizar(string):
    
    #Expressões regulares dos tokens
    tokens_re = [
        
        #Palavras Reservadas
        ('SELECT', r'(?i:select)\b'),
        ('WHERE' , r'(?i:where)\b'),
        ('LIMIT' , r'(?i:limit)\b'),
        ('TYPE_A', r'(a)\b'),
        
        #Variaveis
        ('VAR',     r'\?\w+\b'),
        ('NUM',    r'(\d+)\b'),
        ('TABELA', r'(\w+\:\w+)\b'),
        ('STRING', r'(\".+?\"(@\w+)?)\b'),
        ('ID',     r'([_A-Za-z]\w*)\b'),
        
        #Outros
        ('DOT',    r'\.'),
        ('OPEN_BRACKETS',  r'\{'),
        ('CLOSE_BRACKETS', r'\}'),
        ('NEW_LINE',   r'\n'),
        ('COMMENTARY', r'^\s*\#.*$'),
        ('SKIP',       r'[ \t]+'),
        ('ERRO',       r'.')
    ]
    
    #Criação da Expressão regular
    #Cria um conjunto de alternativas onde guardam no grupo 'P<id>'
    reSet = '|'.join([f'(?P<{id}>{er})' for (id, er) in tokens_re])
    
    lista = []
    linha = 1
    
    mo = re.finditer(reSet, string)
    for m in mo:
        dic = m.groupdict()
        
        if dic['SELECT'] is not None:
            t = ("SELECT",dic['SELECT'],linha,m.span())
        elif dic['WHERE'] is not None:
            t = ("WHERE",dic['WHERE'],linha,m.span())
        elif dic['LIMIT'] is not None:
            t = ("LIMIT",dic['LIMIT'],linha,m.span())
        elif dic['TYPE_A'] is not None:
            t = ("TYPE_A",dic['TYPE_A'],linha,m.span())
            
        elif dic['TABELA'] is not None:
            t = ("TABELA",dic['TABELA'],linha,m.span())
        elif dic['STRING'] is not None:
            t = ("STRING",dic['STRING'],linha,m.span())
        elif dic['NUM'] is not None:
            t = ("NUM",int(dic['NUM']),linha,m.span())
        elif dic['VAR'] is not None:
            t = ("VAR",dic['VAR'],linha,m.span())
        elif dic['ID'] is not None:
            t = ("ID",dic['ID'],linha,m.span())
            
        elif dic['DOT'] is not None:
            t = ("DOT",dic['DOT'],linha,m.span())
        elif dic['OPEN_BRACKETS'] is not None:
            t = ("OPEN_BRACKETS",dic['OPEN_BRACKETS'],linha,m.span())
        elif dic['CLOSE_BRACKETS'] is not None:
            t = ("CLOSE_BRACKETS",dic['CLOSE_BRACKETS'],linha,m.span())
        elif dic['SKIP'] is not None or dic['COMMENTARY'] is not None or dic['NEW_LINE'] is not None:
            continue
        else:
            t = ("ERRO", m.group(), linha, m.span())
        
        #Se for espaços brancos ou comentários, ignora
        if not dic['SKIP'] and not dic['COMMENTARY'] and not dic['NEW_LINE']: 
            lista.append(t)
            

    return lista

#Função Main
def main():
    
    for linha in sys.stdin:
        for token in tokenizar(linha):
            (tipo,string,_,_) = token
            print(f"('{tipo}' , '{string}')")
    

main()