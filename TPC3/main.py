import re
import sys

#Função que trata de negrito
def trataNegrito(string):
    return re.sub(r'(?<!\")(.*?)\*\*(.+?)\*\*(.*?)(?<!\")',r"\1<b>\2</b>\3",string)

#Função que trata do itálico
def trataItalico(string):
    string = re.sub(r'(?<!\")(.*?)\_(.+?)\_(.*?)(?<!\")',r"\1<i>\2</i>\3",string)
    return re.sub(r'(?<!\")(.*?)\*(.+?)\*(.*?)(?<!\")',r"\1<i>\2</i>\3",string)
    
#Função que trata dos headers
def trataHeaders(string):
    
    #Função auxiliar que trata só de 1 substring que deu match
    def trataHeaders_aux(string2):
        grupo1 = string2.group(1)
        grupo2 = string2.group(2)
        nivel_header = len(grupo1)
        return f"<h{nivel_header}>{grupo2}</h{nivel_header}>\n"

    return re.sub(r'(#{1,6}) (.+?)\s*\n', trataHeaders_aux, string)

#Função que trata dos links de URL
def trataLinkURL(string):
    link_coletados = re.findall(r'\[(.*?)\]\((.+?)\)',string)
    dic_links = []
    
    i = 1
    
    for (texto,link) in link_coletados:
        string = re.sub(rf"\[{texto}\]\({link}\)",rf"<LINK{str(i)}>",string,1)
        dic_links.append((texto,link))
        i += 1
    
    return (string,dic_links)


#Função que restaura os URL
def restauraLinkURL(string,dic):
    
    i = 1
    
    for (texto,url) in dic:
        string = re.sub(rf"<LINK{str(i)}>",rf"<a href=\"{url}\">{texto}</a>",string,1)
        i += 1
        
    return string
    

#Função que trata dos links de imagens
def trataLinkImg(string):
    
    imagens_coletadas = re.findall(r'\!\[(.*?)\]\((.+?)\)',string)
    dic_imagens = []
    
    i = 1
    
    for (texto,link) in imagens_coletadas:
        string = re.sub(rf"\!\[{texto}\]\({link}\)",rf"<IMG{str(i)}>",string,1)
        dic_imagens.append((texto,link))
        i += 1
    
    return (string,dic_imagens)

#Função que restaura as imagens
def restauraLinkImg(string,dic):
    
    i = 1
    
    for (texto,img) in dic:
        string = re.sub(rf"<IMG{str(i)}>",rf"<img src={img} alt={texto}/>",string,1)
        i += 1
        
    return string

#Função que trata das listas, tanto ordenadas tanto desordenadas
def trataListas(string):
    
    #Função auxiliar
    def trataListas_aux(string2):
        
        linhas = string2.group().split('\n')
        string = ""
        stack = []
        nivel_anterior = -1

        #Analisar itens das listas
        for linha in linhas:

            ol = re.match(r'^(\s*)\d+\.\s+(.*)$', linha)
            ul = re.match(r'^(\s*)-\s+(.*)$', linha)

            if ol or ul:
                
                #Buscar os espaços para determinar o nivel
                espacos = (ol or ul).group(1)
                conteudo = (ol or ul).group(2)
                nivel = len(espacos) // 4
                
                #Tipo de lista
                tipo = "ol" if ol else "ul"

                #Abrir tags de listas
                while nivel > nivel_anterior:
                    string += f"<{tipo}>"
                    stack.append(tipo) #Guardar qual foi o tipo de lista guardado
                    nivel_anterior += 1

                #Fechar tags das listas
                while nivel < nivel_anterior:
                    item_stack = stack.pop()
                    string += f"</{item_stack}>"
                    nivel_anterior -= 1

                string += f"<li>{conteudo}</li>"

        #Fechar todas as tags que ficaram abertas
        while stack:
            resto = stack.pop()
            string += f"</{resto}>"

        return string

    return re.sub(r'((?:^\s*(?:-|\d+\.)\s+.*(?:\n|$))+)', trataListas_aux, string, flags=re.MULTILINE)

#Função que trata dos '\n'
def trataNewline(string):
    return re.sub(r'(.+?)  \n',r"\1<br>\n",string)

def main():
    
    #Verificação que ficheiro existe
    if len(sys.argv) < 2:
        print("Argumento em falta\nIndique o ficheiro markdown")
        return None
    
    #Abrir ficheiro MarkDown
    f = open(sys.argv[1],"r")
    
    #String que contem o texto todo
    string = "<html>"
        
    #Adicionar todas as linhas do ficheiro
    for linha in f:
        string += linha

    string += "</html>"

    #Tratamentos
    string = trataListas(string) # Listas
    (string,dic_imagens) = trataLinkImg(string) #Links de imagens
    (string,dic_links) = trataLinkURL(string) #Links de URL
    string = trataHeaders(string) #Titulos
    string = trataNegrito(string) #Negrito
    string = trataItalico(string) #Italico
    string = trataNewline(string) #'\n'
    string = restauraLinkImg(string,dic_imagens) #Restaura os links das imagens
    string = restauraLinkURL(string,dic_links) #Restaura os links dos URL
    
    #Criar ficheiro html
    html = open("index.html","w")
    html.write(string)
    print("Ficheiro index.html criado com sucesso!")
    
main()