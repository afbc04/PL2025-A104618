# TPC2 - a104618 - Processamento de Linguagens 2024/2025

**Titulo :** TPC2 da UC Processamento de Linguagens  
**Data :** 2025-02-19  
**Autor :**  
- **Nome :** André Filipe Barros Campos  
- **ID :** a104618  

![Fotografia do Aluno](../image.png)

## Resumo

1. Dado um [dataset em csv](obras.csv), devemos extrair as suas informações _(sem usar o módulo CSV de python)_ e criar os seguintes resultados:  
    1. Lista ordenada alfabeticamente dos compositores musicais,  
    2. Distribuição das obras por período: quantas obras catalogadas em cada período,  
    3. Dicionário em que a cada período está a associada uma lista alfabética dos títulos das obras desse período.  
2. Criei um programa em python chamado [main.py](main.py), que processa o ficheiro csv mencionado em cima e produz os resultados também mencionados acima.  
3. O programa abre o [ficheiro csv](obras.csv) no modo _leitura_ e analiso linha por linha  
4. Em cada linha, analiso caracter a caracter. Dependendo do caracter, o programa pode ter o seguinte comportamento:  
    1. Se o caracter não é um separador _';'_, um '\n', uma aspa e não está dentro de aspas, então adiciono esse caracter ao **buffer**, onde neste buffer estão todos os caracteres que futuramente serão uma _string_ que irá corresponder a uma célula do csv    
    2. Se o caracter é uma aspa, verifico se essa aspa é uma aspa só, _indicando que o texto analisado está dentro de aspas ou não_, ou se é duplas aspas, _indicando que é uma aspa dentro do texto dentro de aspas_:  
        1. Se forem duplas aspas, apenas adiciono o caracter '"' ao **buffer**  
        2. Se não forem duplas aspas, então inverto a _flag_ **dentro_aspas**, que indica se o texto analisado está dentro de aspas ou não. A diferência entre um texto estar dentro ou fora de aspas tem a ver se devo ver caracteres especiais como apenas um caracter dentro de uma _string_ ou se representa operadores do ficheiro  
    3. Se o caracter é o separador _';'_ e ele não está dentro de aspas, então guardo o **buffer** na coluna atual, limpo-o para que possa ser usado futuramente e indico que estou a analisar a próxima coluna  
    4. Se o caracter é '\n', isso significa que cheguei ao fim da linha, logo essa linha foi totalmente analisada. Guardo os dados analisados numa lista e reinicio os dados para que possam ser usados noutra linha  
5. A primeira linha é o **header**, portanto todos os itens serão guardados numa lista de _colunas do header_  
6. As próximas linhas serão dados, portanto todos os itens serão guardados num **dicionário**, onde cada **chave** será uma coluna do header e cada **valor** é o item dessa coluna do dado  
7. Guardo todos os dados, _onde cada dado é um dicionário_, num dicionário maior chamado **csv**  
8. Por fim, com este dicionário _csv_, consigo produzir os resultados pedidos com sucesso, onde:  
    1. Eu coleto todos os compositores e ordeno-os alfabeticamente  
    2. Eu coleto todos os periodos e em cada periodo eu guardo o ID de cada obra numa lista e a quantidade de obras adicionadas nesse periodo  
    3. Eu coleto todos os periodos e em cada periodo eu guardo todos os títulos das obras desse periodo. No fim, eu ordeno-os alfabéticamente  
9. Para verificar que o programa funciona corretamente, e para conseguir visualizar os resultados, eu guardo os resultados em ficheiros **json**:  
    - [Ficheiro "resultados_dataset.json"](resultados_dataset.json) tem todos os dados do ficheiro csv  
    - [Ficheiro "resultados_compositores.json"](resultados_compositores.json) tem todos os compositores ordenados alfabéticamente  
    - [Ficheiro "resultados_quantidade_obras.json"](resultados_quantidade_obras.json) tem todas as quantidades de obras (o ID dessas obras incluido) de um dado periodo  
    - [Ficheiro "resultados_titulo_obras.json"](resultados_titulo_obras.json) tem todos os títulos das obras de um determinado periodo ordenados alfabéticamente  
    - [Ficheiro "resultados.json"](resultados.json) é a junção de todos os resultados listados anteriormente num único ficheiro  

## Lista de Resultados

- [Ficheiro CSV](obras.csv)  
- [Programa que resolve este TPC](main.py)  
- [Ficheiro com os resultados "resultados_dataset.json"](resultados_dataset.json)  
- [Ficheiro com os resultados "resultados_compositores.json"](resultados_compositores.json)  
- [Ficheiro com os resultados "resultados_quantidade_obras.json"](resultados_quantidade_obras.json)  
- [Ficheiro com os resultados "resultados_titulo_obras.json"](resultados_titulo_obras.json)  
- [Ficheiro com os resultados "resultados.json"](resultados.json)  
