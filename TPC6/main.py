from sintatico import sintaticoParser
from nodo import calculaArvore

#Função principal
def main():
    
    print("CTRL + D para parar\n")
    
    try:
        while True:
            #Ler input
            linha = input(">> ")
            #Tokenizar, sintatizar e calcular
            arvore = sintaticoParser(linha)
            #Calcular valor
            (valido,valor) = calculaArvore(arvore)
            #Apresentar valor
            if valido:
                print(f"O valor dá: {valor}")
            else:
                print("Ocorreu um erro")
                
    except EOFError:
        print("Goodbye")

main()

