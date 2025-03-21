# TPC5 - a104618 - Processamento de Linguagens 2024/2025

**Titulo :** TPC5 da UC Processamento de Linguagens  
**Data :** 2025-03-11  
**Autor :**  
- **Nome :** André Filipe Barros Campos  
- **ID :** a104618  

![Fotografia do Aluno](../image.png)

## Resumo

1. Devemos desenvolver um programa que simule uma máquina de vending.  
2. A máquina tem um **stock de produtos** que deverá persistir em ficheiro JSON chamado [stock.json](stock.json), onde este ficheiro deverá ser lido no arranque do programa e deverá ser atualizado quando o programa termina.  
3. Essa máquina deverá ter comandos que permitem manipular a máquina de vending, como por exemplo:
    - Listar
    - Selecionar produto
    - Sair
    - Adicionar Moedas

## Resolução

1. Para resolucionar este TPC, criei o programa **[main.py](main.py)**. Ao iniciar o programa, uso uma função para obter, numa lista, o conteúdo do ficheiro JSON da máquina de venda chamada **[stock.json](stock.json)** para que consiga obter o stock do sistema que foi guardado em ficheiro. Caso este ficheiro não exista, o programa cria automáticamente esse ficheiro e adiciona um produto _"default"_ a esse ficheiro.  
2. Crio o objeto **obj**, que terá as propriedades da máquina de vending, como o **stock** e o **saldo** atual.  
3. Enquanto o programa está a correr, ele espera por _comandos_ dados pelos utilizadores. Após receber esses comandos, o programa usa o **ply.lexer** para _tokenizar_ esses comandos para que seja mais simples executar as _queries_ ditas por eles.  
4. Após tokenizar, verificamos qual o tipo de tokens e, dependendo do seu tipo, tratamo-os de formas diferentes:
    1. **SAIR :** Termina a leitura de comandos, determina quantas moedas a maquina deve dar ao utilizador (no caso, o seu troco) e apresenta essa quantidade no terminal  
    2. **LISTAR :** Lista todos os produtos existentes no stock  
    3. **SALDO :** Indica ao utilizador qual o saldo atual  
    4. **MOEDA :** Adiciona a quantidade de moedas, dadas pelos argumentos do token, ao saldo atual do sistema  
    5. **ADD :** Adicionar um produto novo ao stock, levando em consideração os argumentos deste token, como o código do produto, o seu nome, a sua quantidade e preço  
    6. **REMOVE :** Remove um produto do stock, usando o argumento deste token para descobrir qual produto deve ser removido  
    7. **REFILL :** Adiciona uma quantidade de produtos a um produto do stock especificado pelos argumentos deste token, respetivamente o código do produto e a quantidade a adicionar  
    8. **SELECIONAR :** O sistema obtém o produto indicado pelo argumento do token, verifica se ele existe, verifica se há quantidade dele no stock e verifica se o utilizador pode comprá-lo. Se:
        1. **Produto não existir :** Indica ao utilizador que produto não existe
        2. **Produto vazio :** Indica ao utilizador que não existem produtos daquele tipo  
        3. **Saldo Insuficiente :** Indica ao utilizador que não tem saldo suficiente para efetuar a compra, mostrando qual o preço do produto selecionado  
        4. **Saldo Suficiente :** Subtraimos o valor do produto ao saldo, indicamos que a quantidade desse produto do stock deve diminuir 1 unidade e indicamos ao utilizador que a compra foi efetuada  
5. Após a leitura de _comandos_ terminar, usamos o stock, _carregado em memória_, para atualizarmos o ficheiro JSON do stock, para que ele seja guardado de forma persistente.

## Como usar

- **Sair do programa :** SAIR  
- **Listar produtos :** LISTAR  
- **Ver saldo :** SALDO  
- **Adicionar lista de moedas à máquina :**  
    - MOEDA [2e | 1e | 50c | 20c | 10c | 5c | 2c | 1c]  
    - MOEDA \<LISTA DE MOEDAS SEPARADAS POR VIRGULA\> .  
- **Adicionar produto ao sistema :** ADD \<CÓDIGO\> \<NOME\> \<QUANTIDADE\> \<PREÇO\>  
- **Remover produto do sistema :** REMOVE \<CÓDIGO DO PRODUTO\>  
- **Adicionar quantidade a um produto :** REFILL \<CÓDIGO DO PRODUTO\> \<QUANTIDADE\>  
- **Selecionar produto com a intenção de o comprar :** SELECIONAR \<CÓDIGO DO PRODUTO\>

## Lista de Resultados

- [Programa que resolve este TPC](main.py)  
- [Ficheiro de Input](input.txt)  
- [Ficheiro de Output](output.txt)  
- [Ficheiro que junta os ficheiros de input e output para que seja claramente visivel ver qual o funcionamento do sistema](resultado.txt)