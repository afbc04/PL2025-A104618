import sys
import json
import datetime
import ply.lex as lex
import re

tokens = [
    'MOEDA', #DONE
    'ADD', #DONE
    'REMOVE', #DONE
    'REFILL',
    'LISTAR', #DONE
    'SALDO', #DONE
    'SELECIONAR', #DONE
    'SAIR', #DONE
    'SKIP',
    'ERRO'
]

possiveis_moedas_euros = [1,2]
possiveis_moedas_centimos = [1,2,5,10,20,50]

t_LISTAR = r'LISTAR'
t_SALDO = r'SALDO'
t_SAIR = r'SAIR'

#Trata das moedas
def t_MOEDA(t):
    r'MOEDA\s+\d+[ec](\s*,\s*\d+[ec])*\s*\.?'
    
    euros = 0
    centimos = 0
    
    #Lista com todos os euros
    euros_token = re.findall(r"(\d+)e",t.value)
    if euros_token is not None:
        
        for e in euros_token:
            if int(e) in possiveis_moedas_euros:
                euros += int(e)
    
    #Lista com todos os centimos
    centimos_token = re.findall(r"(\d+)c",t.value)
    if centimos_token is not None:
        
        for c in centimos_token:
            if int(c) in possiveis_moedas_centimos:
                centimos += int(c)
        
    t.value = (euros,centimos)
    
    return t

def t_ADD(t):
    r'ADD\s+(\w+)\s+(\w+)\s+(\d+)\s+(\d+)\.(\d+)\s*'
    
    regex = re.search(r'ADD\s+(\w+)\s+(\w+)\s+(\d+)\s+(\d+)\.(\d{2})\s*',t.value)
    #cod | nome | quantidade | euros_preco | centimos_preco
    t.value = (regex.group(1),
               regex.group(2),
               regex.group(3),
               regex.group(4),
               regex.group(5))
    
    return t

def t_REMOVE(t):
    r'REMOVE\s+\w+'
    
    id = re.search(r'REMOVE\s+(\w+)',t.value)
    t.value = id.group(1)
    
    return t

def t_SELECIONAR(t):
    r'SELECIONAR\s+\w+'
    
    id = re.search(r'SELECIONAR\s+(\w+)',t.value)
    t.value = id.group(1)
    
    return t

def t_REFILL(t):
    r'REFILL\s+\w+\s+\d+\s*'
    
    regex = re.search(r'REFILL\s+(\w+)\s+(\d+)\s*',t.value)
    t.value = (regex.group(1),regex.group(2))
    
    return t

t_ignore = ' \t'

#Função que captura os erros
def t_error(t):
    print("Caracter Ilegal '%s'" % t.value[0])
    t.lexer.skip(1)


#Função que abre o ficheiro de stock
def DaStock():
    
    try:
        f = open("stock.json","r+")
        
    #Se não existir, cria um já com 1 item
    except (FileNotFoundError):
        f = open("stock.json","w+")
        stock = {}
        
        #{"cod": "A23", "nome": "água 0.5L", "quant": 8, "preco": 0.7}
        item_1 = {}
        item_1['cod'] = "A23"
        item_1['nome'] = 'água 0.5L'
        item_1['quant'] = 8
        item_1['preco'] = 0.7
        
        stock['stock'] = [item_1]
        return stock
        
    stock = json.load(f)
    f.close()
    return stock

#Função que salva o stock
def SalvaStock(stock):
    
    f = open("stock.json","w+")
    json.dump(stock,f, indent=4,ensure_ascii=False)
    f.close()


lexer = lex.lex()

#Função que retorna o saldo
def CalculaSaldo(saldo):
    saldo_euros = int(saldo / 100)
    saldo_centimos = int(saldo % 100)
    
    string = ""
    
    #Imprimir euros e centimos
    if saldo_euros > 0 and saldo_centimos > 0:
        string = f"{saldo_euros}e{saldo_centimos}c"
    
    #Imprimir só euros
    elif saldo_euros > 0 and saldo_centimos == 0:
        string = f"{saldo_euros}e"
    
    #Imprimir só centimos
    else:
        string = f"{saldo_centimos}c"
    
    return string

#Função que trata dos pedidos
def PedidoHandler(pedido,obj):
    
    #Listar itens
    if (pedido.type == 'LISTAR'):
        print(f"maq:\n{'cod':<8} | {'nome':<20} | {'quantidade':>10} | {'preço':>8}\n------------------------------------------------------")
        
        for item in obj['stock']:
            print(f"{item['cod']:<8}  {item['nome']:<20}  {item['quant']:>10}   {item['preco']:>8.2f}")
    
    #Ver o Saldo
    elif (pedido.type == 'SALDO'):
        print(f"maq: Saldo = {CalculaSaldo(int(obj['saldo']))}")

    #Adicionar moedas ao saldo
    elif (pedido.type == 'MOEDA'):
        obj['saldo'] += pedido.value[1]
        obj['saldo'] += (pedido.value[0]) * 100
        print(f"maq: Saldo = {CalculaSaldo(int(obj['saldo']))}")
        
    #Selecionar pedido
    elif (pedido.type == 'SELECIONAR'):
        
        pedido_selecionado = None
        pedido_index = 0
        pedido_i = 0
        
        #Buscar index e item do stock
        for item in obj['stock']:
                        
            if item['cod'] == pedido.value:
                pedido_selecionado = item
                pedido_index = pedido_i
        
            pedido_i += 1
        
        #Item existe
        if pedido_selecionado is not None:
            
            #Há quantidade do produto
            if pedido_selecionado['quant'] > 0:
                
                #Há saldo suficiente
                if obj['saldo'] >= (pedido_selecionado['preco'] * 100):
                    
                    obj['saldo'] -= (pedido_selecionado['preco'] * 100) #Tira o saldo
                    pedido_selecionado['quant'] -= 1 #Retira quantidade do produto
                    obj['stock'][pedido_index] = pedido_selecionado #Atualiza pedido
                    
                    #Mensagens
                    print(f"maq: Pode retirar o produto dispensado \"{pedido_selecionado['nome']}\"")
                    print(f"maq: Saldo = {CalculaSaldo(int(obj['saldo']))}")

                #Não há saldo suficiente
                else:
                    print("maq: Saldo insuficiente para satisfazer o seu pedido")
                    print(f"maq: Saldo = {CalculaSaldo(int(obj['saldo']))}; Pedido = {CalculaSaldo(int(pedido_selecionado['preco'] * 100))}")
                
            #Não há quantidade do produto
            else:
                print(f"maq: Não existem produtos deste tipo \"{pedido_selecionado['nome']}\"")
                print(f"maq: Saldo = {CalculaSaldo(int(obj['saldo']))}")
                
        #Item não existe
        else:
            print("maq: Item não existe")
            print(f"maq: Saldo = {CalculaSaldo(int(obj['saldo']))}")
        
    #Adicionar produto
    elif (pedido.type == 'ADD'):
        
        novo_item = {}
        (cod, nome,quantidade, euros, centimos) = pedido.value
        novo_item['cod'] = cod
        novo_item['nome'] = nome
        novo_item['quant'] = int(quantidade)
        novo_item['preco'] = float(int(euros) + (int(centimos) / 100))
        
        obj['stock'].append(novo_item)
        print(f"maq: Produto \"{cod}\" foi adicionado ao sistema!")
        
    #Remover produto
    elif (pedido.type == 'REMOVE'):
    
        novo_stock = []
        
        #Iterar pela lista e só adicionar os itens que não são o que eu quero eliminar
        for item in obj['stock']:
            
            if item['cod'] != pedido.value:
                novo_stock.append(item)
                
        obj['stock'] = novo_stock        
        
        print(f"maq: Produto \"{pedido.value}\" foi removido do sistema!")
                
    #Adicionar quantidade a um produto
    elif (pedido.type == 'REFILL'):
        
        pedido_selecionado = None
        pedido_index = 0
        pedido_i = 0
        
        (item_id,quantidade) = pedido.value
        
        #Buscar produto
        for item in obj['stock']:
                        
            if item['cod'] == item_id:
                pedido_selecionado = item
                pedido_index = pedido_i
        
            pedido_i += 1
        
        #Produto existe
        if pedido_selecionado is not None:
                
            pedido_selecionado['quant'] += int(quantidade) #Aumentar quantidade
            obj['stock'][pedido_index] = pedido_selecionado #Atualizar Stock
            print(f"maq: Foram adicionados {quantidade}x \"{pedido_selecionado['nome']}\"")
                
        #Produto não existe
        else:
            print("maq: Item não existe")
        
    return obj

#Função que tira o saldo com uma certa moeda
def TiraSaldo(saldo,quantidade,moeda_string,troco):
    
    moedas = 0
    
    #Tira essa quantidade até não poder mais
    while saldo >= quantidade:
        moedas += 1
        saldo -= quantidade
        
    troco.append((moedas,moeda_string))
    
    return (saldo,troco)
    

#Função que trata da saida
def SaidaHandler(obj):
    
    saldo = obj['saldo']
    troco = []
    
    #Euros
    (saldo,troco) = TiraSaldo(saldo,200,"2e",troco)
    (saldo,troco) = TiraSaldo(saldo,100,"1e",troco)
    
    #Centimos
    (saldo,troco) = TiraSaldo(saldo,50,"50c",troco)
    (saldo,troco) = TiraSaldo(saldo,20,"20c",troco)
    (saldo,troco) = TiraSaldo(saldo,10,"10c",troco)
    (saldo,troco) = TiraSaldo(saldo,5,"5c",troco)
    (saldo,troco) = TiraSaldo(saldo,2,"2c",troco)
    (saldo,troco) = TiraSaldo(saldo,1,"1c",troco)
    
    moedas_do_troco = []
    
    #Obter todas as moedas
    for (quant,moeda) in troco:
        
        if quant > 0:
            moedas_do_troco.append(f"{quant}x {moeda}")
    
    string_troco = ", ".join(moedas_do_troco)
    
    print(f"maq: Pode retirar o troco: {string_troco}")
    print("maq: Até à próxima")

#Função Main
def main():
    
    #Abrir o Stock
    stock = DaStock()
    data = datetime.datetime.now().date()
    print(f"maq: {data}, Stock carregado ({len(stock)} itens), Estado atualizado")
    print(f"maq: Bom dia. Estou disponível para atender o seu pedido.")

    #Indica se está a correr
    running = True

    #Objeto com as informações da Vending Machine
    obj = {}
    obj['saldo'] = 0
    obj['stock'] = stock

    #Programa a correr
    while running:
        
        #Ler pedido
        pedido = input(">> ")
        lexer.input(pedido)
        
        #Analisar Pedido
        for tok in lexer:
            
            #Sair
            if tok.type == 'SAIR':
                running = False
                SaidaHandler(obj)
                
            #Pedido
            else:
                obj = PedidoHandler(tok,obj)
            
    #Guardar o Stock em Memória
    SalvaStock(obj['stock'])


main()
    
    
    