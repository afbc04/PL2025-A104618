import json
import locale

locale.setlocale(locale.LC_COLLATE, 'pt_PT.UTF-8')

def main():
        
    #Abrir ficheiro CSV
    with open("obras.csv","r") as ficheiro:
        
        #Separador deste CSV
        separador = ';'
        
        #Indica se o header foi analisado
        analisado_Header = False
        #Lista com os campos do header
        lista_campos_header = []
        #Quantidade de campos no header
        N_campos_header = 0
        #Onde ficam os dados do .csv
        csv = []
        
        #Número de campos analisados
        N = 0
        #objeto de uma linha
        objeto = {}
        #Buffer onde vai acumular os caracteres
        buffer = ""
        #Indica se o texto está dentro de aspas
        dentro_aspas = 0
        
        #Obtem uma linha do ficheiro
        for linha in ficheiro:
            
            i = 0
                   
            #Analisar cada char dessa linha                        
            while i < len(linha):
                
                #Obtem char
                char = linha[i]
                
                #Se o char for o separador e está fora de àspas
                #Temos que guardar os dados que coletamos
                if char == separador and dentro_aspas == 0:
                    
                    #Se for header
                    if analisado_Header == False:
                        lista_campos_header.append(buffer)
                        buffer = ""
                        N_campos_header += 1
                        
                    #Se não for o header
                    else:
                        objeto[lista_campos_header[N]] = buffer
                        buffer = ""
                        N += 1
                    
                #Se o char for '\n' e não estiver dentro de àspas, então terminamos o parsing da linha
                elif char == '\n' and dentro_aspas == 0:
                    
                    #Se for header
                    if analisado_Header == False:
                        lista_campos_header.append(buffer)
                        buffer = ""
                        N_campos_header += 1
                        
                    #Se não for header
                    else:
                        objeto[lista_campos_header[N]] = buffer #Adicionar coluna ao objeto
                        csv.append(objeto) #Guardar objeto
                        objeto = {} #Limpar objeto para que possa ser usado novamente
                        N = 0 #Número de colunas analisadas é 0, para ser usado novamente
                        buffer = "" #Limpar o buffer
            
                #Se o char for uma aspa
                elif char == '"':
                    
                    #Verificamos se essa aspa é uma aspa de texto
                    if dentro_aspas == 1 and (len(linha) > i +1 and linha[i+1] == '"'):
                        
                        buffer += '"' #Adicionar aspa ao buffer
                        i += 1 #Não é preciso analisar o elemento i+1 pois já sabemos que é uma aspa
                        
                    #Não é uma aspa de texto
                    else:
                        dentro_aspas = 1 - dentro_aspas #Inverter a flag
                
                #Se não for uma '"', nem um separador nem um '\n', guardar o char no buffer
                else:
                    buffer += char
                    
                #Incrementar o i para obter o próximo char                    
                i += 1
            
            #Ao fim de uma iteração, o header está analisado, logo as próximas linhas serão de objetos
            if analisado_Header == False:
                analisado_Header = True
                
        #Como a ultima linha pode não ter '\n', devemos guardar o ultimo item que está à espera do '\n' para ser guardado
        #Se N > 0, então significa que há coisas por guardar                
        if N > 0:
            objeto[lista_campos_header[N]] = buffer
            csv.append(objeto)
            objeto = {}
            N = 0
            buffer = ""     

    #Base de Dados onde vão ficar os dados do TPC
    base_de_dados = {}
    base_de_dados['dataset'] = csv
    
    #Lista ordenada alfabeticamente dos compositores musicais
    lista_compositores = []
    for objeto in csv:
        lista_compositores.append(objeto['compositor'])
    
    base_de_dados['compositores'] = sorted(lista_compositores)
    
    #Distribuição das obras por período: quantas obras catalogadas em cada período
    map_periodos = {}
    for objeto in csv:
        
        periodo = objeto['periodo']
        
        if periodo in map_periodos:
            map_periodos[periodo]['quantidade'] += 1
            map_periodos[periodo]['obras_id'].append(objeto['_id'])
        else:
            nova_entrada = {}
            nova_entrada['quantidade'] = 1
            nova_entrada['obras_id'] = []
            map_periodos[periodo] = nova_entrada
            
    base_de_dados['obras_periodo'] = map_periodos
        
    
    #Dicionário em que a cada período está a associada uma lista alfabética dos títulos das obras desse período
    map_periodos = {}
    for objeto in csv:
        
        periodo = objeto['periodo']
        
        if periodo in map_periodos:
            map_periodos[periodo].append(objeto['nome'])
        else:
            map_periodos[periodo] = []
            
    for key in map_periodos:
        map_periodos[key] = sorted(map_periodos[key], key=locale.strxfrm)
            
    base_de_dados['titulos_periodo'] = map_periodos
    
    #Criação de resultados:

    #Todos os resultados
    with open("resultados.json","w", encoding="utf-8") as f:
        json.dump(base_de_dados,f, indent=4,ensure_ascii=False)
        
    #Só o dataset
    with open("resultados_dataset.json","w", encoding="utf-8") as f:
        json.dump(base_de_dados['dataset'],f, indent=4,ensure_ascii=False)
        
    #Só os compositores
    with open("resultados_compositores.json","w", encoding="utf-8") as f:
        json.dump(base_de_dados['compositores'],f, indent=4,ensure_ascii=False)
        
    #Só a quantidade de obras por periodo
    with open("resultados_quantidade_obras.json","w", encoding="utf-8") as f:
        json.dump(base_de_dados['obras_periodo'],f, indent=4,ensure_ascii=False)
    
    #Só o título de obras ordenadas alfabeticamente por periodo
    with open("resultados_titulo_obras.json","w", encoding="utf-8") as f:
        json.dump(base_de_dados['titulos_periodo'],f, indent=4,ensure_ascii=False)
            
main()
