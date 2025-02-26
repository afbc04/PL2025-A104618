# TPC3 - a104618 - Processamento de Linguagens 2025

**Titulo :** TPC3 da UC Processamento de Linguagens  
**Data :** 2025-02-26  
**Autor :**  
- **Nome :** André Filipe Barros Campos  
- **ID :** a104618  

## Resumo

1. Dado um ficheiro **MarkDown**, devemos converter esse ficheiro para um ficheiro em **HTML**.  
2. Para isso, criei um programa chamado **[main.py](main.py)** que faz essa conversão, indicando como argumento o _path_ para esse ficheiro escrito em Markdown, dando como resultado um ficheiro **HTML** chamado **index.html**.  
3. Nesse programa _[main.py](main.py)_, abro o ficheiro MarkDown e crio uma **string** (chamado no código como _string_) onde nela ficará todo o texto do ficheiro MarkDown, pois a mudança de linha em MarkDown é indicado por 2 espaços seguidos de um '\n' em vez de '\n'. Por causa deste fator, analisar linha por linha poderia dar problemas.  
4. Existe um conjunto de tratamentos para essa **string**, onde por cada tratamento, a string é modificada com o devido tratamento. A string alterada será tratada pelos seguintes tratamentos até que a string final seja um texto em **HTML**.  
5. Nos tratamentos usei **Expressões Regulares**. Os procedimentos efetuados seguem a seguinte ordem:  
    1. **Tratamento de Listas :** Nesta função, todas as expressões dadas por **` - .\*`** ou **` \d. .\**`** indicam que estamos a tratar de listas em MarkDown. Para tratar das listas, obtenho todas as ocorrências dessas expressões, identifico se é uma **Lista ordenada** ou uma **Lista desordenada**, uso uma variável que indica o **nivel** das listas (para tratar de listas dentro de listas) e uso uma **stack** para abrir e fechar corretamente as tags das listas:  
    _Observação: Quanto maior o nivel, mais afastado o item da lista está do inicio da linha_
        - Se o nivel atual é maior que o nivel anterior, então abro uma nova lista e guardo essa tag na stack  
        - Se o nivel atual é inferior ao nivel anterior, então preciso de fechar a tag, decorrendo à stack para saber que tipo de lista (ordenada ou desordenada) tenho que fechar  
        - Se os níveis forem iguais, não faço nenhuma alteração  
        - Adiciono o item da lista usando a tag \<li\>  
        - Após analisar todas as expressões, fecho todas as tags esvaziando a stack  
    2. **Tratamento de Links de Imagens :** Nesta função, todos os links de imagens são substituidos por uma tag personalizadas chamada **<IMG{N}>**, onde **N** corresponde ao índice de uma lista auxiliar de imagens, que guarda o link e descrição da imagem. O motivo deste tratamento é evitar que sejam feitas alterações nos links, fazendo com o HTML fique desformatado.  
    3. **Tratamento de Links URL :** Nesta função, todos os links URL são substituidos por uma tag personalizadas chamada **<LINK{N}>**, onde **N** corresponde ao índice de uma lista auxiliar de links, que guarda o link e descrição do URL. O motivo deste tratamento é o mesmo do tratamento de links de imagens. Como a diferença entre links de URL e links de imagens é um '!', é necessário que o tratamento de links de imagens sejam executados primeiros, pois o tratamento de links URL iriam dar match com links de imagens.  
    4. **Tratamento de Headers :** Nesta função, todas as linhas que tenham de 1 a 6 '#', conto a quantidade de '#' e substituo por <h{N}>, onde N é a quantidade de '#'.  
    5. **Tratamento de Negrito :** Nesta função, as expressões dadas por "\*\*texto\*\*" serão substituidas por "\<b\>texto\</b\>".  
    6. **Tratamento de Itálico :** Nesta função, as expressões dadas por "\*texto\*" ou "\_texto\_" serão substituidas por "\<i\>texto\</i\>".  
    7. **Tratamento de New Lines :** Nesta função, as expressões dadas por "\n" serão substituidas por "\<br\>".  
    8. **Restauração de Links de Imagens :** Nesta função, todas as tags personalizadas chamadas **<IMG{N}>** serão substituidas pela expressão "\<img src="link da imagem" alt="texto da imagem"\>", onde **link da imagem** e **texto da imagem** estão guardadas na lista auxiliar de imagens mencionada acima.  
    9. **Restauração de Links URL :** Nesta função, todas as tags personalizadas chamadas **<LINK{N}>** serão substituidas pela expressão "\<a href="link URL"\>"descrição"\</a\>", onde **link URL** e **descrição** estão guardadas na lista auxiliar de links mencionada acima.  
6. Como dito acima, após todos estes tratamentos, a **string** estará em formato HTML. Eu crio o ficheiro **[index.html](index.html)** e escrevo a string para esse ficheiro.  

## Lista de Resultados

- [Programa que resolve este TPC](main.py)  
- [Ficheiro MarkDown de input Simples](input.md)  
- [Ficheiro HTML resultante da conversão do Ficheiro de input Simples](index.html)
- [Ficheiro MarkDown de input Complexo](input_complexo.md)  
- [Ficheiro HTML resultante da conversão do Ficheiro de input Complexo](index_complexo.html)  
- [Imagem usada para o Markdown](image.png)  