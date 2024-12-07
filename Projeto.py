#PROJETO PROGRAMAÇÃO

import json
import matplotlib.pyplot as matp

Paper_file = []

def carregaFicheiro(nome):
    try:
        with open(nome, "r", encoding="utf-8") as file:
            ficheiro = json.load(file)
        print(f"Ficheiro '{nome}' carregado com sucesso!")
        return ficheiro
    except FileNotFoundError:
        print(f"Ficheiro '{nome}' não encontrado.")
        return []
    except json.JSONDecodeError:
        print(f"Ficheiro '{nome}' não é um JSON válido.")
        return []
    
Paper_file = carregaFicheiro("ata_medica_papers.json")
    
def guardaFicheiro(nome, dados):
    try:
        with open(nome, "w", encoding="utf-8") as file:
            json.dump(dados, file, ensure_ascii=False, indent=4)
        print(f"Ficheiro '{nome}' guardado com sucesso!")
    except Exception as e:
        print(f"Erro a guardar ficheiro '{nome}': {e}")

def exportSearch(nome, dados):
    try:
        with open(nome, "w", encoding="utf-8") as file:
            json.dump(dados, file, ensure_ascii=False, indent=4)
        print(f"Resultados de pesquisa exportados para o ficheiro '{nome}'!")
    except Exception as e:
        print(f"Erro a exportar resultados de pesquisa para '{nome}': {e}")

def insPaper(abstract, keywords, autores, link1, pdf, data, title, link2):
    Paper = {"abstract": abstract,
             "keywords": keywords,
             "authors": autores,
             "doi" : link1,
             "pdf" : pdf,
             "publish_date" : data,
             "title" : title,
             "url" : link2}
    Paper_file.append(Paper)
    return "Paper publicado com sucesso!"


def editarPaper(titulo, title, abstract, keywords, authors, data):
    for i in Paper_file:
        if i["title"] == titulo:
            artigo = i
    if title == "s":
        title = input("Qual deve ser o novo título?")
        Paper_file[Paper_file.index(artigo)]["title"] = title
    if abstract == "s":
        abstract = input("Qual deve ser a nova sinpose?")
        Paper_file[Paper_file.index(artigo)]["abstract"] = abstract
    if keywords == "s":
        keywords = input("Quais devem ser as novas palavras-chave?")
        Paper_file[Paper_file.index(artigo)]["keywords"] = keywords
    if authors == "s":
        resposta = input("Deseja adicionar, remover, ou editar algum autor? (a/r/e)")
        if resposta == "a":
            autores = []
            numauth = int(input("Quantos autores quer adicionar?"))
            while numauth > 0:
                autor = input("Nomeie um autor")
                afiliação = input("Qual a afiliação desse autor?")
                pessoa = {"name" : autor,
                          "affiliation" : afiliação}
                autores.append(pessoa)
                numauth -= 1
                Paper_file[Paper_file.index(artigo)]["authors"].append(autores)
        elif resposta == "r":
            print(Paper_file[Paper_file.index(artigo)]["authors"])
            removido = int(input("Qual o número do autor que pretende remover? (1-x)"))
            Paper_file[Paper_file.index(artigo)]["authors"].remove(Paper_file[Paper_file.index(artigo)]["authors"][removido - 1])
        elif resposta == "e":
            print(Paper_file[Paper_file.index(artigo)]["authors"])
            alterado = int(input("qual o número do autor que pretende alterar? (1-x)"))
            modo = input("Pretende alterar o nome, a afiliação, ou ambos? (1,2,3)")
            if modo == "1":
                novonome = input("Escolha um novo nome!")
                Paper_file[Paper_file.index(artigo)]["authors"][alterado - 1]["name"] = novonome
            elif modo == "2":
                novaafiliacao = input("Escolha uma nova afiliação!")
                Paper_file[Paper_file.index(artigo)]["authors"][alterado - 1]["affiliation"] = novaafiliacao
            elif modo == "3":
                novonome = input("Escolha um novo nome!")
                Paper_file[Paper_file.index(artigo)]["authors"][alterado - 1]["name"] = novonome
                novaafiliacao = input("Escolha uma nova afiliação!")
                Paper_file[Paper_file.index(artigo)]["authors"][alterado - 1]["affiliation"] = novaafiliacao
    if data == "s":
        data = input("Qual deve ser a nova data de publicação?")
        Paper_file[Paper_file.index(artigo)]["publish_date"] = data

    return f"Processo concluido com sucesso: {Paper_file[Paper_file.index(artigo)]}"

def searchPaper(resposta):
    listapesquisa = []
    if resposta == "1":
        title = input("Insira um título para pesquisar!")
        for i in Paper_file:
            if "title" in i:
                if i["title"] == title:
                    listapesquisa.append(i)

    elif resposta == "2":
        keywords = input("Insira palavras-chave para pesquisar!" )       
        for i in Paper_file:
            if "keywords" in i:
                if keywords in i["keywords"].split(","):
                    listapesquisa.append(i)
                    
    elif resposta == "3":        
        data = input("Insira uma data para pesquisar!" )
        for i in Paper_file:  
            if "publish_date" in i:
                if data in i["publish_date"]: 
                    listapesquisa.append(i)


    elif resposta == "4":
        author = input("Insira um autor para pesquisar!" )  
        for i in Paper_file:     
            for x in i["authors"]:
                if "name" in x:
                    if x["name"] == author:
                        listapesquisa.append(i)

    elif resposta == "5":
        affiliation = input("Insira uma afiliação para pesquisar!" )  
        for i in Paper_file:
            for x in i["authors"]:
                if "affiliation" in x:
                    if x["affiliation"] == affiliation:
                        listapesquisa.append(i)

    else:
        return "Essa resposta não é valida!"
    
    if len(listapesquisa) > 0:
        return listapesquisa
    else:
        return "Nenhum ficheiro encontrado!"

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

def listarauth(resposta):
    listauth = {}
    for i in Paper_file:
        for x in i["authors"]:
            if x["name"] not in listauth:
                listauth[str(x["name"])] = 1
            else:
                listauth[str(x["name"])] += 1
    if resposta == "1":
        listaordenada = sorted(listauth.items(), key = lambda autor: autor[1], reverse = True)
    elif resposta == "2":
        listaordenada = sorted(listauth.items(), key = lambda autor: autor[0])
    else:
        return listauth
    return listaordenada

def listarkeywords(resposta):
    listkeys = {}
    for i in Paper_file:
        if "keywords" in i:
            for x in i["keywords"].split(","):
                x = x.strip()
                if x not in listkeys:
                    listkeys[str(x)] = {"Ocorrências" : 1,
                                        "Artigos" : [i["title"]]}
                else:
                    listkeys[str(x)]["Ocorrências"] += 1
                    listkeys[str(x)]["Artigos"].append(i["title"])
    if resposta == "1":
        listaordenada = sorted(listkeys.items(), key = lambda chave: chave[1]["Ocorrências"], reverse = True)
        listasimplificada = [(i[0], i[1]["Ocorrências"]) for i in listaordenada]

        return listasimplificada
    elif resposta == "2":
        listaordenada = sorted(listkeys.items(), key = lambda chave: chave[0])
        listasimplificada = [(i[0], i[1]["Ocorrências"]) for i in listaordenada]

        return listasimplificada
    else:
        listasimplificada = [(i[0], i[1]["Ocorrências"]) for i in listkeys]

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

    if resposta == "2":
        listdatas = {}
        ano = input("Que ano deseja visualizar?")
        for i in Paper_file:
            if "publish_date" in i:
                x = i["publish_date"]
                if x[0:4] == ano and x[5:7] not in listdatas:
                    listdatas[x[5:7]] = 1
                elif x[0:4] == ano:
                    listdatas[x[5:7]] += 1
        matp.title("Distribuição de artigos num ano")
        matp.xlabel("MESES")
        matp.ylabel("Publicações")
        listaordenada = sorted(listdatas.items(), key = lambda param: param[0])
        autores = [i[0] for i in listaordenada]
        Publicações = [int(i[1]) for i in listaordenada]
        matp.plot(autores, Publicações, label = "Nº de Artigos", color = "r", marker = "o")
        matp.legend()
        matp.show()
    
    if resposta == "3":
        listatop = listarauth("1")
        listatop20 = listatop[:20]
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
        listinha = searchPaper("4")
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
        listinha = listarkeywords("1")[:20]
        matp.title("Distribuição de ocorrências de palavras-chave")
        matp.xlabel("Palavras-chave")
        matp.ylabel("Publicações")
        listinha.reverse()
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
        for i in listaanos.items():
            print (i)

def guardarFicheiro(nome):
    with open(nome, "w", encoding = "utf-8") as file:
        file = Paper_file
    return "nice :)"

#Como deixar o utilizador alterar o ficheiro raiz? Começar em "wr" ou "r+" ???
#Como deixar o utilizador escolher que ficheiro utiliza para as operações, se tiver mais de um aberto? Reestruturar codigo, tendo como argumento de todas as funções a especificaçãao de que ficheiro se quer usar?
#Exportar para um novo ficheiro

def guardarPesquisa(nome, param):
    with open(nome, "w", encoding = "utf-8") as file:
        file = param
        return file
        
graph()
graph()
graph()
graph()
#escolha = input("escolha")

#if escolha = "2":
#    abstrato = input("Descreva a sinopse do seu artigo!")
#    keywords = input("Escolha as palavras-chave para o seu artigo!")
#    autores = []
#    numauth = int(input("Quantos autores tem o artigo?"))
#    while numauth > 0:
#        autor = input("Nomeie um autor")
#        afiliação = input("Qual a afiliação desse autor?")
#        pessoa = {"name" : autor,
#                "affiliation" : afiliação}
#        autores.append(pessoa)
#        numauth -= 1
#    link = input("Introduza o seu link DOI!")
#    imagem = input("Introduza o link para o pdf do documento!")
#    data = input("Introduza a data de hoje!")
#    titulo = input("Qual o título do artigo?")
#    url = input("Introduza o link para a página do artigo!")
#
#    print(insPaper(abstrato, keywords, autores, link, imagem, data, titulo, url))

