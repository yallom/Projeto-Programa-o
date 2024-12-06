#PROJETO PROGRAMAÇÃO

import json
import matplotlib

Paper_file = []

def carregaFicheiro(nome):
    with open(nome, "r", encoding = "utf-8") as file:
        ficheiro = json.load(file)
    return ficheiro

Paper_file = carregaFicheiro("ata_medica_papers.json")

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
            removido = int(input(f"{print(Paper_file[Paper_file.index(artigo)]["authors"])}, qual o número do autor que pretende remover? (1-x)"))
            Paper_file[Paper_file.index(artigo)]["authors"].remove(Paper_file[Paper_file.index(artigo)]["authors"][removido - 1])
        elif resposta == "e":
            alterado = int(input(f"{print(Paper_file[Paper_file.index(artigo)]["authors"])}, qual o número do autor que pretende alterar? (1-x)"))
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
                if i["publish_date"] == data:
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
    if resposta == "1":
        listaordenada = "\n" + str(sorted(listinha, key=lambda artigo: artigo["title"]))
    elif resposta == "2":
        listaordenada = "\n" + str(sorted(listinha, key=lambda artigo: artigo["data"]))
    return listaordenada

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

