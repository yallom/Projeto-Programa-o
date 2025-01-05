# Relatório do Projeto do Sistema de Consulta e Análise de Publicações Científicas

## Introdução
Este projeto consistiu no desenvolvimento de uma aplicação que visa Consulta e Análise de Publicações Científicas.
O sistema permite o carregamento da base de dados, criação de publicações, atualização de publicações, consulta de publicações, análise de publicações por autor, análise de publicações por palavras-chave, armazenamento dos dados, importação de dados e exportação parcial de dados.  O sistema apresenta relatórios que incluem gráficos da distribuição de publicações por ano, publicações por mês de um determinado ano, número de publicações por autor (top 20 autores), publicações de um autor por anos, palavras-chave pela sua frequência (top 20 palavras-chave) e palavras-chave mais frequente por ano.

## Análise e Requisitos
Inicialmente, começou-se por analisar o problema proposto. Foi sugerida a criação de uma aplicação na qual fosse possível consultar, introduzir e alterar conteúdo numa base de dados fornecida, com uma estrutura definida. Assim, o primeiro passo foi o desenvolvimento de uma interface gráfica funcional que permitisse cumprir todos os requisitos.
Para  se aceder às informações contidas na base de dados, é necessário introduzir o nome do ficheiro de texto com formato json já existente, havendo uma tentativa inicial de importar um ficheiro “ata_medica_papers.json”. A partir daí são apresentadas várias opções: “Carregar Base de Dados”, que permite ao usuário a importação de um ficheiro json, para manipulação através da interface, e “Guardar Base de Dados”, que permite a exportação de uma qualquer base de dados, num formato json, salvando quaisquer alterações efetuadas. 
Outras opções são ainda “Adicionar Publicação” e “Editar Publicação”, que permitem, respetivamente, criar uma entrada no DataSet atual conforme alguns critérios específicos, e editar qualquer entrada no documento.
 “Pesquisar Publicações”, “Listar Autores” e “Análise de Keywords” permitem uma compreensão geral da estrutura e conteudo do DataSet, dando a possibilidade de pesquisar por publicações segundo vários critérios, e listar autores e palavras-chave de cada entrada, para obter uma visão geral da informação no documento.
“Estatísticas” permite a visualização, em gráficos, de vários aspetos do documento (Palavras-chave mais mencionadas, autores com mais publicações, etc.) de uma forma mais intuitiva e lúdica.
“Eliminar Publicação” cria a possibilidade para remoção de entradas no DataSet.
“Sair” é a opção final da interface visual, fechando a interface e guardando quaisquer alterações feitas ao documento, se algum tiver sido carregado.

## Estrutura de dados
Para ser possível o desenvolvimento do algoritmo, foi necessário definir a estrutura de dados adequada para o trabalho. Este passo é essencial na criação de uma linha de raciocínio para a definição das funções que constituem o código.
Deste modo, a base de dados é definida por uma lista de dicionários, em que cada um corresponde a uma publicação. Por sua vez, cada publicação inclui "keys". Cada publicação é constituída por título, resumo, palavras-chave, autores, DOI, PDF, data de publicação e URL. Já os autores, são constituídos por uma lista de dicionários, onde cada dicionário contém informações sobre nome, afiliação e ORCID.


Imagem


## Conceção do Algoritmo
### Bibliotecas
O primeiro passo consistiu na importação de módulos necessários para o desenvolvimento do código. Foram importados módulos em json e os, para além de módulos necessários para a criação de gráficos, criação de uma janela e manipulação de datas.
* import matplotlib.pyplot as matp: importa a biblioteca Matplotlib, que é usada para criar gráficos e visualizações em Python;
* import json: converte dicionários e listas Python em strings JSON, como o dataset se encontrava guardado em um ficheiro JSON, esta biblioteca foi usada para conseguir ler e escrever os dados das publicações;
* import os: permite aceder a funcionalidades dependentes do Sistema Operativo.
* import PySimpleGUI as sg : ajuda na criação de um layout de GUI (interface gráfica), janela, texto e botões, com Python;
* from typing import Dict, List: importa os tipos Dict (dicionário) e List (lista) do módulo typing

### Linha de comandos
Este é um programa em Python que realiza operações de gestão de tarefas através da linha de comandos. Começa-se por importar as bibliotecas necessárias, como ‘od‘, ‘json‘ e ‘matplotlib.pyplot as matp’.

De seguida, inicializamos com Paper_file como uma lista vazia. Já a função clear_console() tem como objetivo limpar o ecrã do terminal onde o script está a ser executado. Este verifica o sistema operacional com a expressão os.name, e dependendo do sistema, executa um comando específico para limpar o ecrã: no Windows, usa os.system('cls') e, em sistemas Unix-like (como Linux e macOS), usa os.system('clear').
Em seguida, várias funções são definidas para executar operações específicas, como:

#### Menu principal
Ao selecionar a opção ’Command Line Interface’, surge no terminal do VS Code um menu principal que apresenta todas as opções disponíveis. Essas opções, exigem que o utilizador introduza a opção correspondente à tarefa desejada. Caso selecione a opção ’Visual Interface’ abrirá a interface, que vai ser abordada mais à frente. 


imagem


#### Carregar Base de Dados
O programa deve ser capaz de carregar para a memória interna o conjunto de dados presente num ficheiro
com a seguinte estrutura:


imagem 



#### Criar Publicações
O programa deve permitir que o utilizador crie uma nova publicação, especificando título, resumo, palavras-chave, DOI, autores (com nome, afiliação e ORCID), caminho para o PDF, data da publicação e URL da publicação.

#### Atualizar Publicações
O programa deve permitir que o utilizador atualize as informações de uma dada publicação. Estas informações incluem título, resumo, palavras-chave, autores (nome, afiliação e ORCID), DOI, caminho para o PDF, data da publicação e URL da publicação.

#### Consultar Publicações
O programa deve permitir que o utilizador consulte as publicações através de filtros por título, autor, afiliação, data de publicação e palavras-chave. Após encontrar as publicações, deve ser possível ordená-las pelos títulos ou pelas datas de publicação.

#### Analisar Publicações por Autor
O programa deve listar os autores, permitindo ao utilizador visualizar as publicações correspondentes a um
dado autor. Esta listagem deve ser ordenada pela frequência de publicações e/ou por ordem alfabética.



imagem sem as respostas (antes de selecionar a opção)




#### Analisar Publicações por Palavras-Chave
O programa deve permitir a visualização das palavras-chave existentes no conjunto de dados, possibilitando que o utilizador visualize as publicações correspondentes a uma dada palavra-chave. As palavras-chave devem ser ordenadas pela sua frequência e/ou por ordem alfabética.




imagem sem as respostas (antes de selecionar a opção)



#### Estatísticas das Publicações
O programa deve exibir estatísticas referentes às publicações presentes no conjunto de dados, apresentando gráficos para os seguintes tópicos:
* Distribuição de publicações por ano.
* Distribuição de publicações por mês de um determinado ano.
* Número de publicações por autor (top 20 autores).
* Distribuição de publicações de um autor por anos.
* Distribuição de palavras-chave pela sua frequência (top 20 palavras-chave).
* Distribuição de palavras-chave mais frequentes por ano.




imagem sem as respostas (antes de selecionar a opção)




#### Armazenamento dos Dados
O programa deve guardar as informações alteradas ou adicionadas em memória no ficheiro de suporte.

#### Importação de Dados
O programa deve permitir que, a qualquer momento, seja possível importar novos registros de outro conjunto de dados com a mesma estrutura mencionada anteriormente.

#### Exportação Parcial de Dados
O programa deve permitir exportar os registos resultantes de uma pesquisa para um ficheiro.

### Interface gráfica

#### Carregar Base de dados

De acordo com os requisitos estabelecidos no enunciado, a funcionalidade de carregamento da base de dados (BD) a partir de um arquivo de texto, com extensão JSON, é fundamental para a operação do sistema.




imagem



Ao acionar o botão "Carregar Base de Dados" na interface principal, será aberta uma nova janela solicitando ao usuário que procure no seu Browser a base de dados que deseja utilizar, sendo esta de formato, obrigatoriamente, JSON. A leitura e carregamento desses dados ocorrerão em seguida.
É crucial ressaltar que o botão "Carregar"permanecerá inativo até que o usuário selecione um arquivo de base de dados válido.
Uma vez que a base de dados tenha sido carregada com sucesso, uma mensagem de confirmação será exibida na interface principal, garantindo ao usuário que a operação foi concluída com êxito. Esta abordagem visa assegurar a integridade e a validade dos dados utilizados pelo sistema.

#### Gravar Base de dados
A aplicação possibilita a gravação da base de dados utilizada, sendo este processo crucial para o pleno funcionamento das demais funcionalidades. Enquanto a base de dados não for salva, uma janela de erro será exibida na interface para lembrar o utilizador da necessidade de salvar a base de dados antes de prosseguir com as operações da aplicação.



imagem




Após a gravação bem-sucedida da base de dados, uma mensagem de confirmação será exibida na interface, comunicando ao utilizador que a operação foi concluída com êxito. Essa mensagem de confirmação tem o objetivo de proporcionar ao utilizador a certeza de que os dados foram salvos com sucesso e estão prontos para serem utilizados nas funcionalidades subsequentes da aplicação.
Essa abordagem visa garantir a consistência e a segurança dos dados, promovendo uma experiência de utilização mais fluida e eficiente.




imagem




#### Adicionar Nova Publicação
Ao clicar no botão "Inserir nova tarefa", uma nova janela será aberta, apresentando diversos campos destinados ao preenchimento de informações relacionadas à tarefa a ser adicionada.




imagem




#### Pesquisar Publicação
A aplicação oferece uma funcionalidade que permite a consulta de uma tarefa com base em critérios como título, autor, afiliação, data e keywords. 




imagem



#### Listar Autores
O programa inclui uma funcionalidade de listagem de autores acessada através do botão "Listar Autores" na interface principal.
Nesta opção, é possível escolher entre diversas opções, tais como ordenar por ordem alfabética e ordenar por número de ocorrências.




imagem




#### Editar Publicação
Para editar uma publicação, introduzir o título da publicação a qual pretende editar.




iamgem 




Após a publicação já ter sido localizada, vai aparecer esta janela na qual lhe permitirá editar todos os parâmetros da publicação permitida.




imagem




#### Eliminar publicação
O programa oferece uma função para eliminar tarefas. Assim , ao clicar no botão "Eliminar Publicações", o utilizador terá de passar para um processo de pesquisa e consulta da tarefa que deseja eliminar, onde pode identificar a publicação a partir de vários parâmetros com título, autor, afiliação, data e keywords. 




imagem




Depois de identificar a tarefa desejada, o utilizador deve clicar nessa mesma tarefa para esta ser eliminada com sucesso.





imagem



#### Análise de keywords
O programa inclui uma funcionalidade de listagem de autores acessada através do botão "Análise de keywords" na interface principal.
Nesta opção, é possível escolher entre diversas opções, tais como ordenar por ordem alfabética e ordenar por número de ocorrências.




imagem




#### Análise Estatística

Após carregar no botão “Estatísticas” irá aparecer uma nova janela em que aparecem todas as possibilidades de gráficos, sendo elas  distribuição de publicações por ano, distribuição de publicações por mês de um determinado ano, número de publicações por autor (top 20 autores), publicações de um autor por anos, palavras-chave pela sua frequência (top 20 palavras-chave) e por palavras-chave mais frequentes por ano.




imagem



##### Distribuição de publicações por ano
O programa é capaz de exibir um gráfico com a distribuição de publicações por ano.




imagem 




##### Distribuição mensal de publicações
O programa é capaz de exibir um gráfico com a distribuição mensal de publicações num dado ano.




imagem




#### Número de publicação por autor (Top20)

O programa é capaz de exibir um gráfico com o número de publicações de um autor, mas apenas o Top20




imagem





##### Distribuição de publicações por ano de um dado autor

O programa é capaz de exibir um gráfico com a distribuição de publicações por ano após ser selecionado um autor específico.



imagem




##### Distribuição de palavras-chave pela sua frequência

O programa é capaz de exibir um gráfico com a distribuição das palavras-chave pela sua frequência.




imagem





##### Número de palavras-chave num dado ano (Top20)

O programa é capaz de exibir um gráfico com o número de palavras-chave após ser selecionado um
determinado ano.




imagem



## Desafios e Soluções

Durante o desenvolvimento do projeto, a equipa deparou-se com alguns desafios, que foram solucionados de diversas formas, recorrendo ao engenho e conhecimento dos integrantes, bem como a técnicas lecionadas no decorrer da disciplina. Alguns dos desafios foram:

Não usar ‘break’ no decorrer da interface gráfica - No sentido de não utilizar a função ‘break’ para encerramento de janelas, a equipa recorreu a elementos como ‘continue’, e loops ‘while’ recorrentes, assim como a função ‘window.close()’;

Formatação da interface gráfica - Para uma melhor apresentação e capacidade intuitiva da interface gráfica, uma das necessidades seria uma boa formatação. Para isto, foi necessário implementar elementos como ‘expand_x/y = True’, ‘window.Maximize()’, e páginas “scrollable”.

Dificuldades em acessar e manipular a base e dados - Durante o projeto, a equipa teve de garantir que, em qualquer situação, a base de dados poderia ser corretamente manipulada, mesmo no caso de um ficheiro corrompido ou de um documento incompleto ou mal-formatado.

## Conclusão

O objetivo deste projeto consistia no desenvolvimento de uma aplicação que visa gerir o sistema de gestão de publicações científicas. Consideramos ter conseguido elaborar com sucesso uma aplicação capaz de executar todos os requisitos propostos. A criação da mesma exigiu inúmeras horas de trabalho e pesquisa, exacerbadas pela existência de diversos problemas inesperados, que levaram a múltiplas tentativas-erro.

Apesar disso, consideramos esta aplicação funcional com uma interface de fácil uso e interpretação. Para o desenvolvimento dos algoritmos, foram essenciais todas as ferramentas adquiridas nesta UC, incluindo a manipulação de estruturas de dados e a construção de interfaces gráficas, complementadas pela pesquisa na internet para contrariar eventuais adversidades.

Assim, podemos concluir que este projeto se revelou extremamente útil na consolidação da matéria abordada na UC, aplicando-a num contexto mais prático e adequado ao dia-a-dia. Além disso, permitiu-nos compreender a utilidade, inter-relação e importância das ferramentas adquiridas na UC.
