# TPC6 - a104618 - Processamento de Linguagens 2024/2025

**Titulo :** TPC6 da UC Processamento de Linguagens  
**Data :** 2025-03-20  
**Autor :**  
- **Nome :** André Filipe Barros Campos  
- **ID :** a104618  

![Fotografia do Aluno](../image.png)

## Resumo

1. Devemos desenvolver um programa que calcule o valor de uma expressão algébrica composta por **números** e pelos operadores matemáticos binários:
    - **soma :** +
    - **subtração :** -
    - **multiplicação :** *
    - **divisão :** /
2. Este programa deverá respeitar as prioridades das operações _(isto é, multiplicações e divisões antes das somas e subtrações)_.
3. A resolução deste TPC deverá usar análise sintática _(usando ply.lex)_ e análise sintática recorrendo à **recursividade descendente**.

## Resolução

1. Para resolucionar este TPC, separei a lógica dele em quatro ficheiros:
    - **lexico.py :** contém toda a lógica da análise léxica
    - **sintatico.py :** contém toda a lógica da análise sintática
    - **nodo.py :** usada para representar a árvore de derivação da análise sintática
    - **main.py :** programa onde é resolvido este TPC
2. Para tokenizar a expressão algébrica, recorri ao ficheiro **[lexico.py](lexico.py)** para que reconheça os seguintes tokens:
    - **NUMERO :** representa um número
    - **SOMSUB :** representa um operador de soma ou subtração
    - **MULDIV :** representa um operador de multiplicação ou divisão
3. Para construir a árvore de derivação, criei a seguinte gramática:
```
Regra-1 => INIT = ExpMULDIVInit ExpSOMSUB
Regra-2 => ExpSOMSUB = SOMSUB ExpMULDIVInit ExpSOMSUB
Regra-3 =>           = ε
Regra-4 => ExpMULDIVInit = NUMERO ExpMULDIV
Regra-5 => ExpMULDIV = MULDIV NUMERO ExpMULDIV
Regra-6 =>           = ε
```

4. A explicação destas regras são:
    1. **INIT :** Inicio da expressão algébrica onde quero que ela inicie por um número ou por uma expressão algébrica envolvendo multiplicações e divisões. A chamada recursiva à regra ExpSOMSUB garante que as expressões de soma e subtração são consideradas,
    2. **ExpSOMSUB :** Reconhece expressões algébricas envolvendo somas e subtrações. Elas podem não existir _(Regra-3)_ ou se existirem _(Regra-2)_, têm que ter um operador de soma/subtração, seguido de um número/expressão algébrica de multiplicação ou divisão. Esta regra é recursiva, logo considera multiplas expressões algébricas de soma ou subtração
    1. **ExpMULDIVInit :** Inicio da expressão algébrica envolvendo multiplicações/divisões onde quero que ela inicie um número. A chamada recursiva à regra ExpMULDIV garante que as expressões de multiplicação e divisão são consideradas,
    2. **ExpMULDIV :** Reconhece expressões algébricas envolvendo multiplicações e divisões. Elas podem não existir _(Regra-6)_ ou se existirem, têm que ter um operador de multiplicação/divisão, seguido de um número. Esta regra é recursiva, logo considera multiplas expressões algébricas de multiplicação ou divisão
5. O ficheiro **[sintatico.py](sintatico.py)** vai usar o ficheiro **[nodo.py](nodo.py)** e, usando as gramática apresentada, irá construir a árvore de derivação.
6. Eu gostaria que o calculo da expressão algébrica fosse feita com apenas uma travessia à árvore. Como esta travessia começaria nas folhas da árvore e o resultado delas ia subindo até à raiz, precisei que todas as operações de multiplicação e divisão estivessem abaixo das operações de soma e subtração, para que a prioridade das operações seja respeitada.
7. A forma como pensei na gramática seria considerar uma gramática de apenas somas e subtrações. Desta forma, a árvore gerada teria os operadores perto da raiz e os elementos entre os operadores _(por exemplo, números)_, estariam nas folhas.
8. Se substituísse os elementos por operações de multiplicação e divisão, garantia que estas eram efetuadas antes das operações de soma e subtração (algo desejado). Por isso, tinha que garantir que estes elementos seriam operações de multiplicação e divisão _(para casos de 1+A onde A=2*3)_ ou números _(para casos de 1+A onde A=1)_. Por isso que nas regras 2 e 3, as expressões algébricas envolvendo operações de soma e subtração não são aplicadas diretamente a números, e sim a estes elementos que me refiro.
9. Para calcular o valor da expressão usando a árvore de derivação, usei um algoritmo recursivo que, dependendo do tipo de nodo, iria retornar o número representado ou efetuar a operação nos seus nodos filhos e retornar o resultado para o seu nodo-pai. O resultado retornado pela raíz será o resultado da expressão algébrica.

Exemplo:
```

    +
   / \
  1   *
     / \
    2   3

```
_Iteração 1_
```

    +
   / \
  1   6

```
_Iteração 2_
```

    7

```
_Iteração 3_

10. Por fim, usei o programa **[main.py](main.py)** para ler as expressões algébricas do terminal, tokeniza-las, transformar as equações em árvores de derivação e apresentar o resultado das equações ao utilizador após efetuar a travessia destas árvores.

## Lista de Resultados

- [Programa que resolve este TPC](main.py)  
- [Ficheiro de Input](input.txt)  
- [Ficheiro de Output](output.txt)  