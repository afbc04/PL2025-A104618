import sys

#Função que calcula o número com base numa lista
# Exemplo:
#   Lista = [1,2,3]
#   3*10^0 + 2*10^1 + 1*10^2 = 123
def calculaNumeroComLista(lista):
    
    i = len(lista) - 1
    potencia = 0
    res = 0
    
    while i >= 0:
        res += int(lista[i]) * 10**potencia
        
        i-=1
        potencia+=1
        
    return res

#Verifica se tem a 'string_comparacao' na 'string' no índice i,ignorando as maiusculas
def verifica_on_off(string_,i,string_comparacao_):    
    
    #Obtem a substring iniciando por 'i' e com tamanho da string_comparacao
    string = string_[i : i + len(string_comparacao_)]
    #Torna as letras em minúsculas
    string = string.lower()
    
    #Torna as letras em minúsculas
    string_comparacao = string_comparacao_.lower()
    
    #Indica se as strings são iguais
    return string == string_comparacao
    

def func(string,debug):
    
    i = 0 #Indique indice
    estaLigado = 1 #Indica se o leitor de números está ligado
    acc = 0 #Acumulador
    
    lista_numeros = [] #Lista de números
    
    #Enquanto estamos dentro da string
    while i < len(string):
        
        #Obtem char
        c = string[i]
        
        #É digito
        if c >= '0' and c <= '9':
            
            #Se está ligado, adiciona à lista
            if estaLigado == 1:
                
                lista_numeros.append(c)
                
                if debug:
                    print(f"APPENDING ({c})")
                
            #Não está ligado
            elif debug:
                print(f"IGNORING ({c})")
            
        #Não é digito
        else:
            #Há conteudo em lista_numeros
            if lista_numeros:
                
                #Adiciona número ao acumulador
                acc += calculaNumeroComLista(lista_numeros)
                #Limpa a lista
                lista_numeros = []
                
                if debug:
                    print(f"CALCULATING NUMBER ({c})")
                    print("CALCULATED NUMBER : ",acc)
                
            #Lista está vazia
            elif debug:
                print(f"NOTHING ({c})")
                
            #Mostrar número
            if c == '=':
                print(acc)
                
                if debug:
                    print("SHOWING NUMBER : ",acc)
            
            #Provavelmente tem 'on' ou 'off'
            if c == 'o' or c == 'O':
                
                #Verifica se a string é ON
                if verifica_on_off(string,i,"on"):
                    estaLigado = 1
                    i+=1 #Como sabemos que os próximos chars são "n", então não é preciso verificar esses caracteres
                    
                    if debug:
                        print("TURNING ON NUMBER READER")
                    
                #Verifica se a string é OFF
                if verifica_on_off(string,i,"off"):
                    estaLigado = 0
                    i+=2 #Como sabemos que os próximos chars são "ff", então não é preciso verificar esses caracteres
                    
                    if debug:
                        print("TURNING OFF NUMBER READER")
        
        #Incrementar i
        i+=1
        
        
def main():
    
    #string teste : abc123 1a23cd75=OfF1oNa7=8
    
    while True:
        
        
        try:
            #Obtem string do input
            string = input()

            
            #se a string for "quit", sai
            if string == "quit":
                break
            
            print("---[INICIO]---")
            
            #Se a string não for quit, executa função
            func(string,False)

            print("---[FIM]---\n")
            
        #Ver se é EOF
        except EOFError:
            break
        
main()
