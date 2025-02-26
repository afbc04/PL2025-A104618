# TPC2 - a104618 - Processamento de Linguagens 2025

**Titulo :** TPC2 da UC Processamento de Linguagens  
**Data :** 2025-02-19  
**Autor :**  
- **Nome :** André Filipe Barros Campos  
- **ID :** a104618  

## Resumo

1. Dado um [dataset em csv](obras.csv), devemos extrair as suas informações *(sem usar o módulo CSV de python)* e criar os seguintes resultados:  
2. Criei um programa em python chamado [main.py](main.py), que processa o ficheiro csv mencionado em cima e produz os resultados também mencionados acima.  
3. O programa abre o [ficheiro csv](obras.csv) no modo *leitura* e analiso linha por linha  
4. Em cada linha, analiso caracter a caracter. Dependendo do caracter, o programa pode ter o seguinte comportamento:  
5. A primeira linha é o **header**, portanto todos os itens serão guardados numa lista de *colunas do header*  
6. As próximas linhas serão dados, portanto todos os itens serão guardados num **dicionário**, onde cada **chave** será uma coluna do header e cada **valor** é o item dessa coluna do dado  
7. Guardo todos os dados, *onde cada dado é um dicionário*, num dicionário maior chamado **csv**  
8. Por fim, com este dicionário *csv*, consigo produzir os resultados pedidos com sucesso, onde:  
9. Para verificar que o programa funciona corretamente, e para conseguir visualizar os resultados, eu guardo os resultados em ficheiros **json**:  

## Lista de Resultados

- [Ficheiro CSV](obras.csv)  
- [Programa que resolve este TPC](main.py)  
- [Ficheiro com os resultados "resultados_dataset.json"](resultados_dataset.json)  
- [Ficheiro com os resultados "resultados_compositores.json"](resultados_compositores.json)  
- [Ficheiro com os resultados "resultados_quantidade_obras.json"](resultados_quantidade_obras.json)  
- [Ficheiro com os resultados "resultados_titulo_obras.json"](resultados_titulo_obras.json)  
- [Ficheiro com os resultados "resultados.json"](resultados.json)  

### Imagem

![Imagem](image.png)