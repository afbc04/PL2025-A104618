# TPC4 - a104618 - Processamento de Linguagens 2025

**Titulo :** TPC4 da UC Processamento de Linguagens  
**Data :** 2025-03-05  
**Autor :**  
- **Nome :** André Filipe Barros Campos  
- **ID :** a104618  

## Resumo

1. Dado um texto em linguagem query **SPARQL**, devemos separar esse texto em tokens que demonstrem qual o tipo e _substring_ correspondentes a esse token.  
2. Para isso, criei um programa chamado **[main.py](main.py)** que faz essa _tokenização_ de um texto escrito no **STDIN**, indicando esses _tokens_ no **STDOUT**.  
3. Nesse programa _[main.py](main.py)_, tokenizo linha a linha do _STDIN_ com a função **tokenizar** e imprimo os tokens retornados por essa função no terminal.  
4. Na função **tokenizar**, indico uma lista chamada **tokens_re** que contém pares onde o 1º elemento é o tipo do _token_ e o 2º elemento é a expressão regular desse tipo.  
```
    ('SELECT', r'(?i:select)\b')
```
Neste trecho do código indicamos que o tipo do token é **SELECT** e a expressão regular para este token é **\?i:select**. Qualquer palavra "select", independente se os caracteres estão em maiusculas ou minusculas, é vista como um _token_ do tipo **SELECT**.  

5. Crio um conjunto dessas expressões regulares, usando a lista referida acima, que será usado no texto em linguagem query _SPARQL_. Este conjunto, a que apelidei de **reSet**, é uma única expressão regular que junta _(sob forma de **alternativa**)_ todas as expressões regulares.  
6. Após isso, utilizo um _iterador_ para verificar quais os _tokens_ que foram capturados. A ordem é importante, por isso comecei por ir dos tokens mais "específicos" até os mais "genéricos". O conjunto de tokens que eu considerei são:
    1. **SELECT** : Palavra reservada "select"  
    2. **WHERE** : Palavra reservada "where"  
    3. **LIMIT** : Palavra reservada "limit"  
    4. **TYPE_A** : Palavra reservada "a"  
    5. **TABELA** : Tokens que tenham ':' a meio  
    6. **STRING** : Tokens que sejam uma string  
    7. **NUM** : Tokens que são um número  
    8. **VAR** : Tokens que são uma variável _(Devem começar por \?)_  
    9. **ID** : Tokens que são identificadores  
    10. **DOT** : Tokens que são um ponto  
    11. **OPEN_BRACKETS** e **CLOSE_BRACKETS** : Tokens que indicam quando uma chaveta _{}_ é aberta ou fechada, respetivamente  
    12. **SKIP**, **COMMENTARY** ou **NEW_LINE** : Tokens que não devem ser considerados, pois significam que devo ignorar, são comentários ou é um '\n', respetivamente  
    13. **ERRO** : Tokens que não fizeram match com nenhuma expressão regular previamente mencionadas, logo vou considera-los como erro.  
7. Todos os _tokens_ válidos são guardados numa lista, a que chamei de **lista**, que será retornada pela função _tokenizar_.  
8. Como dito acima, escrevemos essa lista de _tokens_ válidos no **STDOUT**.  

## Lista de Resultados

- [Programa que resolve este TPC](main.py)  
- [Ficheiro SQARQL de Input](input.txt)  
- [Ficheiro com os tokens resultantes do Ficheiro de Input](output.txt)  