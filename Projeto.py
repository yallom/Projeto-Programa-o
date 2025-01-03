#PROJETO PROGRAMAÇÃO
import os
import json #importa o formato do documento do dataset
import matplotlib.pyplot as matp #importa as funcionalidades do matplotlib

Paper_file = []

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def carregaFicheiro(nome): #função de importação de datasets
    try:
        with open(nome, "r", encoding="utf-8") as file:
            ficheiro = json.load(file) #json.load é a função de importação de ficheiros json
        print(f"Ficheiro '{nome}' carregado com sucesso!")
        return ficheiro
    except FileNotFoundError: #se o ficheiro não for encontrado
        print(f"Ficheiro '{nome}' não encontrado.")
        return []
    except json.JSONDecodeError: #se o ficheiro não estiver bem formatado
        print(f"Ficheiro '{nome}' não é um JSON válido.")
        return []

Paper_file = carregaFicheiro("ata_medica_papers.json")

def guardaFicheiro(nome, dados): #função de exportação de datasets
    try:
        with open(nome, "w", encoding="utf-8") as file:
            json.dump(dados, file, ensure_ascii=False, indent=4) #guarda os dados num ficheiro de nome "nome". ensure_ascii=False significa que podemos meter simbolos especiais (~), indent significa que cria uma margem pequena no inicio do ficheiro
        print(f"Ficheiro '{nome}' guardado com sucesso!")
    except Exception as e: #para qualquer erro, mostra ao utilizador o erro que ocorreu
        print(f"Erro a guardar ficheiro '{nome}': {e}")


def exportSearch(nome, dados): #função de exportação de uma lista de pesquisa
    try:
        with open(nome, "w", encoding="utf-8") as file:
            json.dump(dados, file, ensure_ascii=False, indent=4)
        print(f"Resultados de pesquisa exportados para o ficheiro '{nome}'!")
    except Exception as e:
        print(f"Erro a exportar resultados de pesquisa para '{nome}': {e}")

def insPaper(abstract, keywords, autores, link1, pdf, data, title, link2): #função de criação de artigos
    Paper = {"abstract": abstract,
             "keywords": keywords,
             "authors": autores,
             "doi" : link1,
             "pdf" : pdf,
             "publish_date" : data,
             "title" : title,
             "url" : link2} #cria um dicionario com todos os dados relevantes a um artigo
    Paper_file.append(Paper) #insere o artigo no ficheiro (sem o guardar)
    return "Paper publicado com sucesso!"

def editarPaper(titulo, title, abstract, keywords, authors, data): #função de edição de artigos
    for i in Paper_file:
        if i["title"] == titulo: #verifica se cada artigo é o que se pretende alterar
            artigo = i
    if title == "s": #se o utilizador quiser alterar o titulo escreve "s"
        title = input("Qual deve ser o novo título?")
        Paper_file[Paper_file.index(artigo)]["title"] = title
    if abstract == "s": #se o utilizador quiser alterar a sinpose escreve "s"
        abstract = input("Qual deve ser a nova sinpose?")
        Paper_file[Paper_file.index(artigo)]["abstract"] = abstract
    if keywords == "s": #se o utilizador quiser alterar as palavras-chave escreve "s"
        keywords = input("Quais devem ser as novas palavras-chave?")
        Paper_file[Paper_file.index(artigo)]["keywords"] = keywords
    if authors == "s": #se o utilizador quiser alterar os autores escreve "s"
        resposta = input("Deseja adicionar, remover, ou editar algum autor? (a/r/e)")
        if resposta == "a": #se o utilizador quiser adicionar um autor escreve "a"
            numauth = int(input("Quantos autores quer adicionar?"))
            while numauth > 0: #conta o número de autores que já foram adicionados
                autor = input("Nomeie um autor")
                afiliação = input("Qual a afiliação desse autor?")
                pessoa = {"name" : autor,
                          "affiliation" : afiliação} #cria um dicionário com toda a informação relevante a um autor
                numauth -= 1
                Paper_file[Paper_file.index(artigo)]["authors"].append(pessoa) #insere o autor no artigo
        elif resposta == "r": #se o utilizador quiser remover um autor escreve "r"
            print(Paper_file[Paper_file.index(artigo)]["authors"]) #mostra ao utilizador os autores no artigo
            removido = int(input("Qual o número do autor que pretende remover? (1-x)"))
            Paper_file[Paper_file.index(artigo)]["authors"].remove(Paper_file[Paper_file.index(artigo)]["authors"][removido - 1]) #remove o autor escolhido pelo utilizador
        elif resposta == "e": #se o utilizador quiser editar um autor escreve "e"
            print(Paper_file[Paper_file.index(artigo)]["authors"])
            alterado = int(input("qual o número do autor que pretende alterar? (1-x)"))
            modo = input("Pretende alterar o nome, a afiliação, ou ambos? (1,2,3)") 
            if modo == "1":  #se o utilizador quiser alterar o nome do autor
                novonome = input("Escolha um novo nome!")
                Paper_file[Paper_file.index(artigo)]["authors"][alterado - 1]["name"] = novonome
            elif modo == "2":  #se o utilizador quiser alterar a afiliação do autor
                novaafiliacao = input("Escolha uma nova afiliação!")
                Paper_file[Paper_file.index(artigo)]["authors"][alterado - 1]["affiliation"] = novaafiliacao
            elif modo == "3":  #se o utilizador quiser alterar o nome e afiliação do autor
                novonome = input("Escolha um novo nome!")
                Paper_file[Paper_file.index(artigo)]["authors"][alterado - 1]["name"] = novonome
                novaafiliacao = input("Escolha uma nova afiliação!")
                Paper_file[Paper_file.index(artigo)]["authors"][alterado - 1]["affiliation"] = novaafiliacao
    if data == "s": #se o utilizador quiser alterar a data de publicação escreve "s"
        data = input("Qual deve ser a nova data de publicação?")
        Paper_file[Paper_file.index(artigo)]["publish_date"] = data

    return f"Processo concluido com sucesso: {Paper_file[Paper_file.index(artigo)]}"

def searchPaper(resposta: int): #função de pesquisa de artigos
    listapesquisa = []
    if resposta == 1: #se o utilizador quiser pesquisar por titulo
        title = input("Insira um título para pesquisar!")
        for i in Paper_file:
            if "title" in i: #verifica se o artigo tem título
                if i["title"] == title:
                    listapesquisa.append(i)

    elif resposta == 2: #se o utilizador quiser pesquisar por palavras-chave
        keywords = input("Insira palavras-chave para pesquisar!" )       
        for i in Paper_file:
            if "keywords" in i: #verifica se o artigo tem palavras-chave
                if keywords in i["keywords"].split(","):
                    listapesquisa.append(i)
                    
    elif resposta == 3: #se o utilizador quiser pesquisar por data de publicação
        data = input("Insira uma data para pesquisar!" )
        for i in Paper_file:  
            if "publish_date" in i: #verifica se o artigo tem data de publicação
                if data in i["publish_date"]: 
                    listapesquisa.append(i)


    elif resposta == 4: #se o utilizador quiser pesquisar por autor
        author = input("Insira um autor para pesquisar!" )  
        for i in Paper_file:     
            for x in i["authors"]: 
                if "name" in x: #verifica se o autor tem nome
                    if x["name"] == author:
                        listapesquisa.append(i)

    elif resposta == 5: #se o utilizador quiser pesquisar por afiliação
        affiliation = input("Insira uma afiliação para pesquisar!" )  
        for i in Paper_file:
            for x in i["authors"]:
                if "affiliation" in x: #verifica se o autor tem afiliação
                    if x["affiliation"] == affiliation:
                        listapesquisa.append(i)

    else:  #se o utilizador não submeter uma opção válida
        return "Essa resposta não é valida!"
    
    if len(listapesquisa) > 0: #verifica se algum ficheiro foi encontrado com os parametros estabelecidos
        return listapesquisa
    else:
        return "Nenhum ficheiro encontrado!"

def searchPaper2(sublista: list, resposta: int): #função de pesquisa de artigos
    listapesquisa = []
    if resposta == 1: #se o utilizador quiser pesquisar por titulo
        title = input("Insira um título para pesquisar!")
        for i in sublista:
            if "title" in i: #verifica se o artigo tem título
                if i["title"] == title:
                    listapesquisa.append(i)

    elif resposta == 2: #se o utilizador quiser pesquisar por palavras-chave
        keywords = input("Insira palavras-chave para pesquisar!" )       
        for i in sublista:
            if "keywords" in i: #verifica se o artigo tem palavras-chave
                if keywords in i["keywords"].split(","):
                    listapesquisa.append(i)
                    
    elif resposta == 3: #se o utilizador quiser pesquisar por data de publicação
        data = input("Insira uma data para pesquisar!" )
        for i in sublista:  
            if "publish_date" in i: #verifica se o artigo tem data de publicação
                if data in i["publish_date"]: 
                    listapesquisa.append(i)


    elif resposta == 4: #se o utilizador quiser pesquisar por autor
        author = input("Insira um autor para pesquisar!" )  
        for i in sublista:     
            for x in i["authors"]: 
                if "name" in x: #verifica se o autor tem nome
                    if x["name"] == author:
                        listapesquisa.append(i)

    elif resposta == 5: #se o utilizador quiser pesquisar por afiliação
        affiliation = input("Insira uma afiliação para pesquisar!" )  
        for i in sublista:
            for x in i["authors"]:
                if "affiliation" in x: #verifica se o autor tem afiliação
                    if x["affiliation"] == affiliation:
                        listapesquisa.append(i)

    else:  #se o utilizador não submeter uma opção válida
        return "Essa resposta não é valida!"
    
    if len(listapesquisa) > 0: #verifica se algum ficheiro foi encontrado com os parametros estabelecidos
        return listapesquisa
    else:
        return "Nenhum ficheiro encontrado!"

def eliminar_publicacao(titulo: str) -> bool:
    #Elimina uma publicação da base de dados
    try:
        for pub in Paper_file:
            if pub['title'] == titulo:
                Paper_file.remove(pub)
                return True
        else: 
            return False
    except Exception as e:
        print(f"Erro ao eliminar publicação: {e}")
        return False

def elimPaper():
    pesquisa = []
    print("""Menu de Eliminação
      [1] Pesquisar por título
      [2] Pesquisar por palavras-chave
      [3] Pesquisar por data
      [4] Pesquisar por autor
      [5] Pesquisar por afiliação""")
    resposta = int(input("Escolha uma opção: "))
    pesquisa = searchPaper(resposta)
    while len(pesquisa) > 9:
        print(f"""O resultado da pesquisa retornou {len(pesquisa)} items. Adicione outro critério de pesquisa.
            [1] Pesquisar por título
            [2] Pesquisar por palavras-chave
            [3] Pesquisar por data
            [4] Pesquisar por autor
            [5] Pesquisar por afiliação""")
        resposta = int(input("Escolha uma opção: "))
        pesquisa = searchPaper2(pesquisa, resposta)
    if type(pesquisa) != type(["a", "b", "c"]):
        print(pesquisa)
        print("A pesquisa não retornou nenhum paper que possa ser eliminado.")
        return 0
    else:
        print("Menu de Eliminação")
        for i in range(len(pesquisa)):
            print(f"[{i+1}] {pesquisa[i]["title"]}")
        print("\n" + "[0] Cancelar operação")
        resposta = int(input("Escolha o paper a eliminar: "))-1
        while resposta not in range(len(pesquisa)):
            if resposta == -1: return 0
            else:
                resposta = int(input("Escolha inválida. Tente outra vez: "))-1
        target = pesquisa[resposta]
        Paper_file.remove(target)
        return 0



#resposta = input("Escolha")
#listinha = searchPaper(resposta)
#print (listinha)

#2def ordenarPaper(resposta):
    #if resposta == "1":
        #listaordenada = "\n" + str(sorted(listinha, key=lambda artigo: artigo["title"]))
    #elif resposta == "2":
        #listaordenada = "\n" + str(sorted(listinha, key=lambda artigo: artigo["data"]))
    #return listaordenada

#print(ordenarPaper("1"))

def listarauth(resposta: int, limit: int = -1): #função de listar autores
    listauth = {}
    if limit == -1: limit = 100000
    for i in range(min(limit, len(Paper_file))):
        authors = Paper_file[i]["authors"]
        for x in authors:
            if x["name"] not in listauth: #verifica se o autor já foi adicionado à lista
                listauth[str(x["name"])] = 1 #adiciona o autor à lista e define o número de ocorreências como 1
            else:
                listauth[str(x["name"])] += 1 #acrescenta 1 ao número de ocorrências do autor, se este já estiver na lista
    if resposta == "1": #o utilizador escolhe de que forma quer ordenar os dados: 1-por número de artigos por autor (maior->menor), 2-por ordem alfabética dos autores
        listaordenada = sorted(listauth.items(), key = lambda autor: autor[1], reverse = True) #função normal lambda
    elif resposta == "2":
        listaordenada = sorted(listauth.items(), key = lambda autor: autor[0])
    else:
        return listauth
    return listaordenada

def listarkeywords(resposta): #função de listar palavras-chave
    listkeys = {}
    for i in Paper_file:
        if "keywords" in i:
            for x in i["keywords"].split(","): #prepara os dados para análise, cada vírgula representa uma separação nas keywords
                x = x.strip() #retira espaços em branco no início e no fim das palavras-chave, para " criança" e "criança" não serem contadas como variáveis diferentes
                if x not in listkeys: #verifica se a keyword já foi adicionada à lista
                    listkeys[str(x)] = {"Ocorrências" : 1,
                                        "Artigos" : [i["title"]]} #cria um novo dicionário dentro de listkeys, que tem o nome da keyword atual, e define o número de ocorrências como 1, adicionando o artigo presente à lista de artigos
                else:
                    listkeys[str(x)]["Ocorrências"] += 1 #+1 ao número de ocorrências da keyword
                    listkeys[str(x)]["Artigos"].append(i["title"]) #adiciona o titulo do artigo a lista de artigos desta keyword
    if resposta == "1":
        listaordenada = sorted(listkeys.items(), key = lambda chave: chave[1]["Ocorrências"], reverse = True) #ordena listkeys, a partir do número de ocorrências de cada keyword (maior->menor)
        listasimplificada = [(i[0], i[1]["Ocorrências"]) for i in listaordenada] #cria uma nova lista, sem os nomes dos artigos de cada keyword

        return listasimplificada
    elif resposta == "2":
        listaordenada = sorted(listkeys.items(), key = lambda chave: chave[0]) #ordena listkeys, por ordem alfabética de keywords
        listasimplificada = [(i[0], i[1]["Ocorrências"]) for i in listaordenada] #cria uma nova lista, sem os nomes dos artigos de cada keyword

        return listasimplificada
    else:
        listasimplificada = [(i[0], i[1]["Ocorrências"]) for i in listkeys] #se nenhuma das opções normais for selecionada, o programa devolve uma lista simplificada, mas não ordenada

        return listasimplificada
    
def graph():
    print("""Escolha um gráfico para visualizar:
1) Gráfico de publicações por ano
2) Gráfico de publicações por mês, num ano
3) Gráfico de publicações por autor (Top 20)
4) Gráfico de publicações de um autor ao longo dos anos
5) Gráfico de ocorrências de palavras-chave (Top 20)
6) Lista de palavras-chave com maior ocorrência em cada ano""")
    resposta = input("Que gráfico pretende construir?")

    if resposta == "1":
        listdatas = {}
        for i in Paper_file:
            if "publish_date" in i:
                x = i["publish_date"] #x= YYYY/MM/DD
                if x[0:4] not in listdatas: #verifica se o ano em que o artigo foi publicado já existe em listadatas
                    listdatas[x[0:4]] = 1 #cria uma constante (x[0:4]) e dá-lhe o valor de 1
                else:
                    listdatas[x[0:4]] += 1 #+1 para o número de ocorrências de artigos num ano, se o ano já existir na lista
            elif "publish_date" not in i and "N/A" not in listdatas: #se o artigo não tiver data, e se ainda não houver uma constante de data indefinida em listadatas, cria essa constante e dá-lhe o valor de 1
                listdatas["N/A"] = 1
            else:
                listdatas["N/A"] += 1 #+1 para "N/A"
        matp.title("Distribuição de artigos por ano") #define titulo do grafico
        matp.xlabel("ANOS") #define nome da abcissa
        matp.ylabel("Publicações") #define nome da ordenada
        listaordenada = sorted(listdatas.items(), key = lambda param: param[0]) #ordena a lista de datas, de acordo com o número de publicações por ano (menor->maior)
        datas = [i[0] for i in listaordenada] #cria um alista apenas com os anos, já ordenados
        Publicações = [int(i[1]) for i in listaordenada] #cria uma lista, apenas com as ocorrências, já ordenadas
        matp.plot(datas, Publicações, label = "Nº de Artigos", color = "b", marker = "o") #define x = datas, y = Publicações, nome da variável = "Nº de Artigos", cor do grafico = blue, identificador de dados = círculo ("o")
        matp.legend() #ativa a legenda (nome da variável)
        matp.show() #ativa o gráfico

    if resposta == "2":
        listdatas = {}
        ano = input("Que ano deseja visualizar?")
        for i in Paper_file:
            if "publish_date" in i:
                x = i["publish_date"] #x= YYYY/MM/DD
                if x[0:4] == ano and x[5:7] not in listdatas: #verifica se o mês em que o artigo foi publicado já existe em listadatas e se o artigo pertence ao ano correto
                    listdatas[x[5:7]] = 1
                elif x[0:4] == ano:
                    listdatas[x[5:7]] += 1
        matp.title("Distribuição de artigos num ano")
        matp.xlabel("MESES")
        matp.ylabel("Publicações")
        listaordenada = sorted(listdatas.items(), key = lambda param: param[0])
        autores = [i[0] for i in listaordenada]
        Publicações = [int(i[1]) for i in listaordenada]
        matp.plot(autores, Publicações, label = "Nº de Artigos", color = "r", marker = "o") #cor do grafico = "red"
        matp.legend()
        matp.show()
    
    if resposta == "3":
        listatop = listarauth("1") #cria uma lista dos autores com mais publicações
        listatop20 = listatop[:20] #escolhe os 20 autores com mais publicações
        matp.title("Distribuição de artigos por autor (Top 20)")
        matp.xlabel("Autor")
        matp.ylabel("Publicações")
        listaordenada = sorted(listatop20, key = lambda param: param[1])
        datas = [i[0] for i in listaordenada]
        Publicações = [int(i[1]) for i in listaordenada]
        matp.plot(datas, Publicações, label = "Nº de Artigos", color = "r", marker = "o")
        matp.legend()
        matp.show()

    if resposta == "4":
        listinha = searchPaper("4") #cria uma lista com os artigos de um autor
        listdatas = {}
        for i in listinha:
            if "publish_date" in i:
                x = i["publish_date"]
                if x[0:4] not in listdatas:
                    listdatas[x[0:4]] = 1
                else:
                    listdatas[x[0:4]] += 1
            elif "publish_date" not in i and "N/A" not in listdatas:
                listdatas["N/A"] = 1
            else:
                listdatas["N/A"] += 1
        matp.title("Distribuição de artigos por ano")
        matp.xlabel("ANOS")
        matp.ylabel("Publicações")
        listaordenada = sorted(listdatas.items(), key = lambda param: param[0])
        datas = [i[0] for i in listaordenada]
        Publicações = [int(i[1]) for i in listaordenada]
        matp.plot(datas, Publicações, label = "Nº de Artigos", color = "b", marker = "o")
        matp.legend()
        matp.show()

    if resposta == "5":
        listinha = listarkeywords("1")[:20] #cria uma lista das top 20 keywords em termos de utilização
        matp.title("Distribuição de ocorrências de palavras-chave")
        matp.xlabel("Palavras-chave")
        matp.ylabel("Publicações")
        listinha.reverse() #inverte o sentido da lista de keywords
        print (listinha)
        keys = [i[0] for i in listinha]
        Publicações = [int(i[1]) for i in listinha]
        matp.plot(keys, Publicações, label = "Nº de Artigos", color = "b", marker = "o")
        matp.legend()
        matp.show()

    if resposta == "6":
        listapares = {}
        for i in Paper_file:
            if "publish_date" in i:
                x = i["publish_date"]
                year = x[0:4]
            else:
                year = "N/A"
            if year not in listapares:
                listapares[year] = {}
            if "keywords" in i:
                for n in i["keywords"].split(","):
                    n = n.strip()
                    if n not in listapares[year]:
                        listapares[year][n] = 1
                    else:
                        listapares[year][n] += 1
        listaanos = {}
        for ano, keywords in listapares.items():
            if len(keywords) > 0:
                listaordenada = sorted(keywords.items(), key=lambda param: param[1], reverse=True)
                listaanos[ano] = [listaordenada[0]]
                listaanos2 = sorted(listaanos.items(), key=lambda param: param[0], reverse=True)
        for i in listaanos2:
            print (i)
