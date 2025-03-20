# Expressão
class Exp:
    def __init__(self, operador, valor_esquerda, valor_direita):
        self.operador = operador #Operação
        self.valor_esquerda = valor_esquerda #Nodo da Esquerda
        self.valor_direita = valor_direita #Nodo da Direita

    def __str__(self):
        return f"({self.operador} {self.valor_esquerda} {self.valor_direita})"

# Nodo
class Nodo:
    def __init__(self, vazio=True, numero=0):
        self.vazio = vazio #Indica se o nodo está vazio
        self.numero = numero #

    def __str__(self):
        
        if self.vazio == False:
            return f"({self.numero})"
        else:
            return "()"
        
# Calcular Valor de Arvore
def calculaArvore(arvore):
    
    #Se for um Nodo
    if isinstance(arvore,Nodo):
        
        #Se nao está vazio
        if arvore.vazio == False:
            return (True,arvore.numero)
        #Não tem nada
        else:
            return (False,0)
        
    #Se for uma expressão
    elif isinstance(arvore,Exp):
        
        operador = arvore.operador
        valor_esquerda = calculaArvore(arvore.valor_esquerda)
        valor_direita = calculaArvore(arvore.valor_direita)
        
        #Se não há valores válidos, retorna um valor inválido
        if not valor_esquerda[0] and not valor_direita[0]:
            return (False,0)
        
        #Se o valor da direita é o único válido, retorna o valor da direita
        elif not valor_esquerda[0] and valor_direita[0]:
            return valor_direita
        
        #Se o valor da esquerda é o único válido, retorna o valor da esquerda
        elif valor_esquerda[0] and not valor_direita[0]:
            return valor_esquerda
        
        #Ambos valores são válidos
        else:
            
            #Vê qual tipo de operador
            match operador:
                
                #Subtração
                case '-':
                    valor_calculado = valor_esquerda[1] - valor_direita[1]
                
                #Soma
                case '+':
                    valor_calculado = valor_esquerda[1] + valor_direita[1]
                    
                #Multiplicação
                case '*':
                    valor_calculado = valor_esquerda[1] * valor_direita[1]
                    
                #Divisão
                case '/':
                    valor_calculado = valor_esquerda[1] / valor_direita[1]
                    
                #Operador inválido
                case _:
                    return (False,0)
            
            #Retorna valor
            # (A,B)
            # A => Indica se o valor é válido
            # B => valor do nodo
            return (True,valor_calculado)
        
    #Não é um nodo nem uma expressão
    else:
        return (False,0)