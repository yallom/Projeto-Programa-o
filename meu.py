import json #importa o formato do documento do dataset
import matplotlib.pyplot as matp #importa as funcionalidades do matplotlib
import tkinter as tk
from tkinter import filedialog, messagebox


# Função de importação de datasets
def carregaFicheiro(nome):
    try:
        with open(nome, "r", encoding="utf-8") as file:
            ficheiro = json.load(file)  # json.load é a função de importação de ficheiros json
        messagebox.showinfo("Sucesso", f"Ficheiro '{nome}' carregado com sucesso!")
        return ficheiro
    except FileNotFoundError:  # se o ficheiro não for encontrado
        messagebox.showerror("Erro", f"Ficheiro '{nome}' não encontrado.")
        return []
    except json.JSONDecodeError:  # se o ficheiro não estiver bem formatado
        messagebox.showerror("Erro", f"Ficheiro '{nome}' não é um JSON válido.")
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


def exportar_pesquisa():
    nome_ficheiro = filedialog.asksaveasfilename(
        title="Exportar Pesquisa",
        defaultextension=".json",
        filetypes=[("Ficheiros JSON", "*.json"), ("Todos os ficheiros", "*.*")]
    )
    if nome_ficheiro:
        resultados_pesquisa = {
            "pesquisa": ["resultado1", "resultado2", "resultado3"],
            "total": 3
        }
        exportSearch(nome_ficheiro, resultados_pesquisa)





# Função para abrir uma nova janela com os dois botões
def abrir_janela_ficheiro():
    nova_janela = Toplevel()
    nova_janela.title("Ficheiro")
    nova_janela.geometry("300x200")

    # Botão para carregar o ficheiro
    botao_carregar = tk.Button(nova_janela, text="Carregar Ficheiro", command=selecionar_ficheiro)
    botao_carregar.pack(pady=10)

    # Botão para guardar o ficheiro
    botao_guardar = tk.Button(nova_janela, text="Guardar Ficheiro", command=salvar_ficheiro)
    botao_guardar.pack(pady=10)





# Função para criação de artigos
def insPaper(abstract, keywords, autores, link1, pdf, data, title, link2):
    Paper = {
        "abstract": abstract,
        "keywords": keywords,
        "authors": autores,
        "doi": link1,
        "pdf": pdf,
        "publish_date": data,
        "title": title,
        "url": link2
    }
    Paper_file.append(Paper)
    return "Paper publicado com sucesso!"


# Função para abrir a janela de criação de artigo
def criar_novo_artigo():
    def publicar_artigo():
        # Obter valores dos campos
        abstract = entry_abstract.get("1.0", tk.END).strip()
        keywords = entry_keywords.get().strip().split(",")  # Divide palavras-chave por vírgula
        autores = entry_autores.get().strip().split(",")  # Divide autores por vírgula
        link1 = entry_doi.get().strip()
        pdf = entry_pdf.get().strip()
        data = entry_data.get().strip()
        title = entry_titulo.get().strip()
        link2 = entry_url.get().strip()

        # Verificar se os campos obrigatórios foram preenchidos
        if not (abstract and title and data):
            messagebox.showerror("Erro", "Campos obrigatórios: Abstract, Título e Data.")
            return

        # Criar o artigo e adicionar ao arquivo global
        mensagem = insPaper(abstract, keywords, autores, link1, pdf, data, title, link2)
        messagebox.showinfo("Sucesso", mensagem)
        nova_janela.destroy()  # Fechar a janela após publicar

    # Criar nova janela para os campos do artigo
    nova_janela = Toplevel()
    nova_janela.title("Criar Novo Artigo")
    nova_janela.geometry("400x500")

    # Campos para inserir os dados
    tk.Label(nova_janela, text="Título:").pack(pady=5)
    entry_titulo = tk.Entry(nova_janela, width=50)
    entry_titulo.pack()

    tk.Label(nova_janela, text="Abstract:").pack(pady=5)
    entry_abstract = tk.Text(nova_janela, height=5, width=50)
    entry_abstract.pack()

    tk.Label(nova_janela, text="Palavras-chave (separadas por vírgula):").pack(pady=5)
    entry_keywords = tk.Entry(nova_janela, width=50)
    entry_keywords.pack()

    tk.Label(nova_janela, text="Autores (separados por vírgula):").pack(pady=5)
    entry_autores = tk.Entry(nova_janela, width=50)
    entry_autores.pack()

    tk.Label(nova_janela, text="DOI:").pack(pady=5)
    entry_doi = tk.Entry(nova_janela, width=50)
    entry_doi.pack()

    tk.Label(nova_janela, text="PDF Link:").pack(pady=5)
    entry_pdf = tk.Entry(nova_janela, width=50)
    entry_pdf.pack()

    tk.Label(nova_janela, text="Data de Publicação:").pack(pady=5)
    entry_data = tk.Entry(nova_janela, width=50)
    entry_data.pack()

    tk.Label(nova_janela, text="URL:").pack(pady=5)
    entry_url = tk.Entry(nova_janela, width=50)
    entry_url.pack()

    # Botão para publicar o artigo
    botao_publicar = tk.Button(nova_janela, text="Publicar Artigo", command=publicar_artigo)
    botao_publicar.pack(pady=20)



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


# Função para abrir a janela de edição de artigos
def editar_artigo():
    def carregar_artigo():
        titulo = simpledialog.askstring("Editar Artigo", "Digite o título do artigo:")
        if not titulo:
            return
        artigo = next((i for i in Paper_file if i["title"] == titulo), None)
        if not artigo:
            messagebox.showerror("Erro", f"Artigo com título '{titulo}' não encontrado.")
            return

        # Preencher os campos com os dados existentes
        entry_titulo.delete(0, tk.END)
        entry_titulo.insert(0, artigo["title"])
        entry_abstract.delete("1.0", tk.END)
        entry_abstract.insert("1.0", artigo["abstract"])
        entry_keywords.delete(0, tk.END)
        entry_keywords.insert(0, ", ".join(artigo["keywords"]))
        entry_autores.delete(0, tk.END)
        entry_autores.insert(0, ", ".join([a["name"] for a in artigo["authors"]]))
        entry_data.delete(0, tk.END)
        entry_data.insert(0, artigo["publish_date"])

    def salvar_artigo():
        titulo = entry_titulo.get()
        abstract = entry_abstract.get("1.0", tk.END).strip()
        keywords = entry_keywords.get().strip()
        autores = entry_autores.get().strip()
        data = entry_data.get().strip()

        mensagem = editarPaper(
            titulo,
            titulo if titulo else "n",
            abstract if abstract else "n",
            keywords if keywords else "n",
            autores if autores else "n",
            data if data else "n"
        )
        messagebox.showinfo("Resultado", mensagem)
        nova_janela.destroy()

    # Criar a nova janela para edição
    nova_janela = Toplevel()
    nova_janela.title("Editar Artigo")
    nova_janela.geometry("400x500")

    tk.Label(nova_janela, text="Título:").pack(pady=5)
    entry_titulo = tk.Entry(nova_janela, width=50)
    entry_titulo.pack()

    tk.Label(nova_janela, text="Abstract:").pack(pady=5)
    entry_abstract = tk.Text(nova_janela, height=5, width=50)
    entry_abstract.pack()

    tk.Label(nova_janela, text="Palavras-chave (separadas por vírgula):").pack(pady=5)
    entry_keywords = tk.Entry(nova_janela, width=50)
    entry_keywords.pack()

    tk.Label(nova_janela, text="Autores (separados por vírgula):").pack(pady=5)
    entry_autores = tk.Entry(nova_janela, width=50)
    entry_autores.pack()

    tk.Label(nova_janela, text="Data de Publicação:").pack(pady=5)
    entry_data = tk.Entry(nova_janela, width=50)
    entry_data.pack()

    # Botões para carregar e salvar alterações
    tk.Button(nova_janela, text="Carregar Artigo", command=carregar_artigo).pack(pady=10)
    tk.Button(nova_janela, text="Salvar Alterações", command=salvar_artigo).pack(pady=10)




def abrir_janela_artigos():
    nova_janela = Toplevel()
    nova_janela.title("Gerenciamento de Artigos")
    nova_janela.geometry("300x200")

    # Botões na janela de artigos
    tk.Button(nova_janela, text="Criar Novo Artigo", command=criar_novo_artigo).pack(pady=10)
    tk.Button(nova_janela, text="Editar Artigo", command=editar_artigo).pack(pady=10)
    tk.Button(nova_janela, text="Pesquisar Artigo", command=pesquisar_artigo).pack(pady=10)





def listarauth(resposta): #função de listar autores
    listauth = {}
    for i in Paper_file:
        for x in i["authors"]:
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

def mostrar_lista_autores():
    def listar():
        resposta = combo_ordem.get()
        autores_ordenados = listarauth(resposta)

        # Exibir a lista de autores na área de texto
        resultado_text.delete("1.0", tk.END)  # Limpa o texto anterior
        if autores_ordenados:
            for autor, count in autores_ordenados:
                resultado_text.insert(tk.END, f"Autor: {autor}, Artigos: {count}\n")
        else:
            resultado_text.insert(tk.END, "Nenhum autor encontrado.\n")

    # Criar a nova janela para listar autores
    nova_janela = Toplevel()
    nova_janela.title("Listar Autores")
    nova_janela.geometry("400x400")

    # Opções para ordenar a lista
    tk.Label(nova_janela, text="Escolha a forma de ordenar os autores:").pack(pady=10)

    combo_ordem = tk.StringVar()
    tk.Radiobutton(nova_janela, text="Por número de artigos (Maior -> Menor)", variable=combo_ordem, value="1").pack(anchor=tk.W)
    tk.Radiobutton(nova_janela, text="Por ordem alfabética", variable=combo_ordem, value="2").pack(anchor=tk.W)

    # Botão para listar autores
    tk.Button(nova_janela, text="Listar Autores", command=listar).pack(pady=10)

    # Área de texto para exibir os resultados
    resultado_text = tk.Text(nova_janela, height=10, width=50)
    resultado_text.pack(pady=10)


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




# Função para abrir a janela de "Listar Palavras-Chave"
def abrir_lista_keywords():
    nova_janela = Toplevel()
    nova_janela.title("Listar Palavras-Chave")

    def mostrar_lista(opcao):
        lista = listarkeywords(opcao)

        resultado.delete(1.0, tk.END)  # Limpa a área de texto
        for item in lista:
            resultado.insert(tk.END, f"{item[0]}: {item[1]}\n")

    # Botões para escolher a opção de ordenação
    tk.Button(nova_janela, text="Ordenar por Ocorrências", command=lambda: mostrar_lista("1")).pack(pady=5)
    tk.Button(nova_janela, text="Ordenar por Ordem Alfabética", command=lambda: mostrar_lista("2")).pack(pady=5)
    tk.Button(nova_janela, text="Lista Simplificada", command=lambda: mostrar_lista("3")).pack(pady=5)

    # Área de texto para mostrar os resultados
    resultado = tk.Text(nova_janela, width=50, height=20)
    resultado.pack()




# Função para abrir a janela "Listar"
def abrir_janela_listar():
    nova_janela = Toplevel()
    nova_janela.title("Opções de Listagem")
    nova_janela.geometry("300x150")

    # Botão para listar autores
    tk.Button(nova_janela, text="Listar Autores", command=mostrar_lista_autores).pack(pady=20)

    # Botão para listar palavras-chave
    tk.Button(nova_janela, text="Listar Palavras-Chave", command=abrir_lista_keywords).pack(pady=20)



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


graph()
graph()
graph()
graph()




# Função para abrir a janela de gráficos
def abrir_janela_graficos():
    nova_janela = Toplevel()
    nova_janela.title("Opções de Gráficos")
    nova_janela.geometry("300x300")

    # Botões para cada gráfico
    tk.Button(nova_janela, text="Gráfico de publicações por ano", command=lambda: graph()).pack(pady=10)
    tk.Button(nova_janela, text="Gráfico de publicações por mês em um ano", command=lambda: graph()).pack(pady=10)
    tk.Button(nova_janela, text="Gráfico de publicações por autor (Top 20)", command=lambda: graph()).pack(pady=10)
    tk.Button(nova_janela, text="Gráfico de publicações de um autor ao longo dos anos", command=lambda: graph()).pack(pady=10)
    tk.Button(nova_janela, text="Gráfico de ocorrências de palavras-chave (Top 20)", command=lambda: graph()).pack(pady=10)
    tk.Button(nova_janela, text="Lista de palavras-chave por ano", command=lambda: graph()).pack(pady=10)



def fechar():
    print("Fechando o programa...")
    janela.quit()  # Isso encerra o mainloop e fecha a aplicação.

janela = tk.Tk()
janela.title("Exemplo de quit")


# Configurar a interface principal
def criar_interface_principal():
    janela = tk.Tk()
    janela.title("Janela Principal")
    janela.geometry("300x150")

    # Botão para abrir a janela de "Ficheiro"
    botao_ficheiro = tk.Button(janela, text="Ficheiro", command=abrir_janela_ficheiro)
    botao_ficheiro.pack(pady=10)

    # Botão para exportar pesquisa
    botao_exportar = tk.Button(janela, text="Exportar", command=exportar_pesquisa)
    botao_exportar.pack(pady=10)

    # Botão para abrir a janela artigo
    botao_artigo = tk.Button(janela, text="Artigo", command=abrir_janela_artigos)
    botao_artigo.pack(pady=10)

    # Botão "Listar" na janela principal
    botao_listar = tk.Button(janela, text="Listar", command=abrir_janela_listar)
    botao_listar.pack(pady=10)

    # Botão "Gráficos" para abrir a janela de gráficos
    botao_graficos = tk.Button(janela, text="Gráficos", command=abrir_janela_graficos)
    botao_graficos.pack(pady=10)

    # Botão "Exit" para sair do programa
    botao_exit = tk.Button(janela, text="Exit", command=janela.quit)
    botao_exit.pack(pady=10)

    janela.mainloop()


