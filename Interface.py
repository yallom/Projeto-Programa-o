import json
import matplotlib.pyplot as matp
import PySimpleGUI as sg
from typing import Dict, List
from textwrap import wrap


class SistemaPubs:
    #Sistema principal para gestão de publicações científicas
    def __init__(self):
        self.publicacoes = []
        self.ficheiro_padrao = "ata_medica_papers.json"
        self.carregar_base_dados()

    def carregar_base_dados(self, nome_ficheiro: str = None) -> bool:
        #Carrega a base de dados do ficheiro JSON
        try:
            with open(nome_ficheiro or self.ficheiro_padrao, 'r', encoding='utf-8') as f:
                self.publicacoes = json.load(f)
            print(f"Base de dados carregada com sucesso!")
            return True
        except FileNotFoundError:
            print(f"Ficheiro não encontrado.")
            return False
        except json.JSONDecodeError:
            print(f"Erro na formatação do ficheiro JSON.")
            return False

    def guardar_base_dados(self, nome_ficheiro: str = None) -> bool:
        #Guarda a base de dados num ficheiro JSON
        try:
            with open(nome_ficheiro or self.ficheiro_padrao, 'w', encoding='utf-8') as f:
                json.dump(self.publicacoes, f, ensure_ascii=False, indent=4)
            print(f"Base de dados guardada com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao guardar a base de dados: {e}")
            return False

    def criar_publicacao(self, dados: Dict) -> bool:
        #Cria uma nova publicação na base de dados
        try:
            # Validação básica dos dados
            campos_obrigatorios = ['title', 'abstract', 'keywords', 'authors', 'doi', 'pdf', 'publish_date', 'url']
            if not all(campo in dados for campo in campos_obrigatorios):
                print("Dados incompletos para criar publicação")
                return False
            
            # Validação dos autores
            for autor in dados['authors']:
                if not all(campo in autor for campo in ['name', 'affiliation', 'orcid']):
                    print("Dados de autor incompletos")
                    return False

            self.publicacoes.append(dados)
            return True
        except Exception as e:
            print(f"Erro ao criar publicação: {e}")
            return False

    def editarPaper(self, titulo, title, abstract, keywords, authors, data): #função de edição de artigos
        for i in self.publicacoes:
            if i["title"] == titulo: #verifica se cada artigo é o que se pretende alterar
                artigo = i
        if title == "s": #se o utilizador quiser alterar o titulo escreve "s"
            title = input("Qual deve ser o novo título?")
            self.publicacoes[self.publicacoes.index(artigo)]["title"] = title
        if abstract == "s": #se o utilizador quiser alterar a sinpose escreve "s"
            abstract = input("Qual deve ser a nova sinpose?")
            self.publicacoes[self.publicacoes.index(artigo)]["abstract"] = abstract
        if keywords == "s": #se o utilizador quiser alterar as palavras-chave escreve "s"
            keywords = input("Quais devem ser as novas palavras-chave?")
            self.publicacoes[self.publicacoes.index(artigo)]["keywords"] = keywords
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
                    self.publicacoes[self.publicacoes.index(artigo)]["authors"].append(pessoa) #insere o autor no artigo
            elif resposta == "r": #se o utilizador quiser remover um autor escreve "r"
                print(self.publicacoes[self.publicacoes.index(artigo)]["authors"]) #mostra ao utilizador os autores no artigo
                removido = int(input("Qual o número do autor que pretende remover? (1-x)"))
                self.publicacoes[self.publicacoes.index(artigo)]["authors"].remove(self.publicacoes[self.publicacoes.index(artigo)]["authors"][removido - 1]) #remove o autor escolhido pelo utilizador
            elif resposta == "e": #se o utilizador quiser editar um autor escreve "e"
                print(self.publicacoes[self.publicacoes.index(artigo)]["authors"])
                alterado = int(input("qual o número do autor que pretende alterar? (1-x)"))
                modo = input("Pretende alterar o nome, a afiliação, ou ambos? (1,2,3)") 
                if modo == "1":  #se o utilizador quiser alterar o nome do autor
                    novonome = input("Escolha um novo nome!")
                    self.publicacoes[self.publicacoes.index(artigo)]["authors"][alterado - 1]["name"] = novonome
                elif modo == "2":  #se o utilizador quiser alterar a afiliação do autor
                    novaafiliacao = input("Escolha uma nova afiliação!")
                    self.publicacoes[self.publicacoes.index(artigo)]["authors"][alterado - 1]["affiliation"] = novaafiliacao
                elif modo == "3":  #se o utilizador quiser alterar o nome e afiliação do autor
                    novonome = input("Escolha um novo nome!")
                    self.publicacoes[self.publicacoes.index(artigo)]["authors"][alterado - 1]["name"] = novonome
                    novaafiliacao = input("Escolha uma nova afiliação!")
                    self.publicacoes[self.publicacoes.index(artigo)]["authors"][alterado - 1]["affiliation"] = novaafiliacao
        if data == "s": #se o utilizador quiser alterar a data de publicação escreve "s"
            data = input("Qual deve ser a nova data de publicação?")
            self.publicacoes[self.publicacoes.index(artigo)]["publish_date"] = data

        return f"Processo concluido com sucesso: {self.publicacoes[self.publicacoes.index(artigo)]}"
    
    def searchSpecific(self,title):
        try:
            for artigo in self.publicacoes:
                if 'title' in artigo:
                    if artigo['title'] == title:
                        return artigo
            print('Artigo não encontrado!')
            return {}
        except Exception as e:
            print(f"Erro ao eliminar publicação: {e}")
            return {}
        
    def eliminar_publicacao(self, titulo: str) -> bool:
        #Elimina uma publicação da base de dados
        try:
            for pub in self.publicacoes:
                if pub['title'] == titulo:
                    self.publicacoes.remove(pub)
                    return True
            return False
        except Exception as e:
            print(f"Erro ao eliminar publicação: {e}")
            return False


    def eliminar_publicacao_interface(self):
        layout_search = [
            [sg.Text('Pesquisar por:')],
            [sg.Radio('Título', 'SEARCH', key='titulo', default=True),
            sg.Radio('Autor', 'SEARCH', key='autor'),
            sg.Radio('Afiliação', 'SEARCH', key='afiliacao'),
            sg.Radio('Data', 'SEARCH', key='data'),
            sg.Radio('Keywords', 'SEARCH', key='keywords')],
            [sg.Text('Termo de pesquisa:'), sg.Input(key='search_term')],
            [sg.Button('Pesquisar',button_color=('white', '#2B5B84')), sg.Button('Cancelar',button_color=('white', '#2B5B84'))]
        ]
        
        window_search = sg.Window('Pesquisar Publicação para Eliminar', layout_search, location=(None, None), resizable=True, finalize=True)
        window_search.set_min_size((400, 150))
        
        while True:
            event, values = window_search.read()
            
            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window_search.close()
                return
                
            if event == 'Pesquisar':
                criterio = next(k for k, v in values.items() if v and k in ['titulo', 'autor', 'afiliacao', 'data', 'keywords'])
                resultados = self.pesquisar_publicacoes(criterio, values['search_term'])
                
                if not resultados:
                    sg.popup('Nenhuma publicação encontrada!')
                    continue
                    
                layout_results = [[sg.Text('Publicações Encontradas:', font=('Helvetica', 12, 'bold'))]]
                for pub in resultados:
                    title_text = f"Título: {pub['title']}\nAutores: {', '.join(a['name'] for a in pub['authors'])}"
                    layout_results.append([
                        sg.Multiline(title_text, size=(50, 2), disabled=True),
                        sg.Button('Eliminar', key=f"DEL_{pub['title']}",button_color=('white', '#2B5B84'))
                    ])
                layout_results.append([sg.Button('Fechar',button_color=('white', '#2B5B84'))])
                
                scrollable_layout = [[sg.Column(layout_results, scrollable=True, vertical_scroll_only=True, size=(600, 400))]]
                
                window_results = sg.Window('Resultados da Pesquisa', 
                                        scrollable_layout, 
                                        location=(None, None),
                                        resizable=True,
                                        finalize=True)
                window_results.set_min_size((650, 450))
                
                while True:
                    event_res, _ = window_results.read()
                    if event_res in (sg.WIN_CLOSED, 'Fechar'):
                        break
                        
                    if event_res.startswith('DEL_'):
                        title = event_res[4:]
                        if sg.popup_yes_no('Tem certeza que deseja eliminar esta publicação?') == 'Yes':
                            if self.eliminar_publicacao(title):
                                sg.popup('Publicação eliminada com sucesso!')
                                window_results.close()
                                break
                            else:
                                sg.popup('Erro ao eliminar publicação!')
                
                window_results.close()
        
            window_search.close()

    def pesquisar_publicacoes(self, criterio, valor) -> List[Dict]:
        #Pesquisa publicações por diferentes critérios
        resultados = []
        try:
            if criterio == "titulo":
                for i in self.publicacoes:
                    if "title" in i: #verifica se o artigo tem título
                        if valor in i["title"] :
                            resultados.append(i)
            elif criterio == "autor":
                for i in self.publicacoes:     
                    for x in i["authors"]: 
                        if "name" in x: #verifica se o autor tem nome
                            if x["name"] == valor:
                                resultados.append(i)
            elif criterio == "afiliacao":
                for i in self.publicacoes:
                    for x in i["authors"]:
                        if "affiliation" in x: #verifica se o autor tem afiliação
                            if x["affiliation"] == valor:
                                resultados.append(i)
            elif criterio == "data":
                for i in self.publicacoes:  
                    if "publish_date" in i: #verifica se o artigo tem data de publicação
                        if valor in i["publish_date"]: 
                            resultados.append(i)
            elif criterio == "keywords":
                for i in self.publicacoes:
                    keywords = i.get('keywords', '').strip()
                    keywords_list = [k.strip() for k in keywords.split(',') if k.strip()]
                    if valor in keywords_list:
                        resultados.append(i)
            return resultados
        except Exception as e:
            print(f"Erro na pesquisa: {e}")
            return []

    def ordenar_resultados(self, resultados: List[Dict], criterio: str) -> List[Dict]:
        #Ordena os resultados por título ou data
        try:
            if criterio == "titulo":
                return sorted(resultados, key=lambda x: x['title'])
            elif criterio == "data":
                return sorted(resultados, key=lambda x: x['publish_date'])
            return resultados
        except Exception as e:
            print(f"Erro ao ordenar resultados: {e}")
            return resultados

    def analisar_autores(self, ordenacao) -> List[tuple]:
        contagem_autores = {}
        try:
            for pub in self.publicacoes:
                # Verifica se 'authors' existe e é uma lista
                if 'authors' in pub and isinstance(pub['authors'], list):
                    for autor in pub['authors']:
                        if isinstance(autor, dict) and 'name' in autor:
                            nome = autor['name']
                            if nome not in contagem_autores:
                                contagem_autores[nome] = {'Ocorrências': 1, 'Artigos': [pub['title']]}
                            else:
                                contagem_autores[nome]['Ocorrências'] += 1
                                contagem_autores[nome]['Artigos'].append(pub['title'])
                else:
                    print(f"Formato inválido em 'authors': {pub.get('authors')}")

            # Ordena conforme solicitado
            if ordenacao == "alfabetica":
                return sorted(contagem_autores.items())
            elif ordenacao == "frequencia":
                return sorted(contagem_autores.items(), 
                            key=lambda x: x[1]['Ocorrências'], 
                            reverse=True)
        except Exception as e:
            print(f"Erro na análise de autores: {e}")
            return []



    def analisar_keywords(self, ordenacao) -> List[tuple]:
        #Análise de palavras-chave e suas ocorrências
        listkeys = {}
        for i in self.publicacoes:
            if "keywords" in i:
                for x in i["keywords"].split(","): #prepara os dados para análise, cada vírgula representa uma separação nas keywords
                    x = x.strip() #retira espaços em branco no início e no fim das palavras-chave, para " criança" e "criança" não serem contadas como variáveis diferentes
                    if x not in listkeys: #verifica se a keyword já foi adicionada à lista
                        listkeys[str(x)] = {"Ocorrências" : 1,
                                            "Artigos" : [i["title"]]} #cria um novo dicionário dentro de listkeys, que tem o nome da keyword atual, e define o número de ocorrências como 1, adicionando o artigo presente à lista de artigos
                    else:
                        listkeys[str(x)]["Ocorrências"] += 1 #+1 ao número de ocorrências da keyword
                        listkeys[str(x)]["Artigos"].append(i["title"]) #adiciona o titulo do artigo a lista de artigos desta keyword
        
            # Ordena conforme solicitado
        if ordenacao == "alfabetica":
            return sorted(listkeys.items(), key=lambda x: x[0])
        elif ordenacao == "frequencia":  # frequencia
            return sorted(listkeys.items(), 
                        key=lambda x: x[1]['Ocorrências'], 
                        reverse=True)


    def graph(self, tipo, escolha: str = None):
        if tipo == "1":
            listdatas = {}
            for i in self.publicacoes:
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

        if tipo == "2":
            listdatas = {}
            for i in self.publicacoes:
                if "publish_date" in i:
                    x = i["publish_date"] #x= YYYY/MM/DD
                    if x[0:4] == escolha and x[5:7] not in listdatas: #verifica se o mês em que o artigo foi publicado já existe em listadatas e se o artigo pertence ao ano correto
                        listdatas[x[5:7]] = 1
                    elif x[0:4] == escolha:
                        listdatas[x[5:7]] += 1
            if listdatas == []:
                return False
            matp.title("Distribuição de artigos num ano")
            matp.xlabel("MESES")
            matp.ylabel("Publicações")
            listaordenada = sorted(listdatas.items(), key = lambda param: param[0])
            autores = [i[0] for i in listaordenada]
            Publicações = [int(i[1]) for i in listaordenada]
            matp.plot(autores, Publicações, label = "Nº de Artigos", color = "r", marker = "o") #cor do grafico = "red"
            matp.legend()
            matp.show()
        
        if tipo == "3":
            listatop = self.analisar_autores("frequencia") #cria uma lista dos autores com mais publicações
            listatop20 = listatop[:20] #escolhe os 20 autores com mais publicações
            listatop20.reverse()
            matp.title("Distribuição de artigos por autor (Top 20)")
            matp.xlabel("Autor")
            matp.ylabel("Publicações")
            datas = [i[0] for i in listatop20]
            Publicações = [int(i[1]['Ocorrências']) for i in listatop20]
            matp.plot(datas, Publicações, label = "Nº de Artigos", color = "r", marker = "o")
            matp.legend()
            matp.show()

        if tipo == "4":
            listinha = self.pesquisar_publicacoes('autor',escolha) #cria uma lista com os artigos de um autor
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

        if tipo == "5":
            listinha = self.analisar_keywords("frequencia")[:20]#cria uma lista das top 20 keywords em termos de utilização
            matp.title("Distribuição de ocorrências de palavras-chave")
            matp.xlabel("Palavras-chave")
            matp.ylabel("Publicações")
            listinha.reverse() #inverte o sentido da lista de keywords
            print (listinha)
            keys = [i[0] for i in listinha]
            Publicações = [int(i[1]['Ocorrências']) for i in listinha]
            matp.plot(keys, Publicações, label = "Nº de Artigos", color = "b", marker = "o")
            matp.legend()
            matp.show()

        if tipo == "6":
            listapares = {}
            for i in self.publicacoes:
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
            matp.title("Top 20 Palavras-chave")
            matp.xlabel("Palavras-chave")
            matp.ylabel("Ocorrências")
            anos = [int(i[0]) for i in listaanos2]
            keys = [i[1][0][0] for i in listaanos2]
            matp.plot(anos, keys, label = "Nº de Artigos", color = "b", marker = "o")
            matp.legend()
            matp.show()

    def exportar_resultados(self, resultados: List[Dict], nome_ficheiro: str) -> bool:
        #Exporta resultados de pesquisa para um ficheiro
        try:
            with open(nome_ficheiro, 'w', encoding='utf-8') as f:
                json.dump(resultados, f, ensure_ascii=False, indent=4)
            print(f"Resultados exportados com sucesso para {nome_ficheiro}")
            return True
        except Exception as e:
            print(f"Erro ao exportar resultados: {e}")
            return False
#ORIGINAL CODE

def criar_interface_grafica():
    sg.theme('LightBlue2')
    
    TITLE_FONT = ('Helvetica', 24, 'bold')
    BUTTON_FONT = ('Helvetica', 11)
    LABEL_FONT = ('Helvetica', 11)
    HEADER_FONT = ('Helvetica', 14, 'bold')
    
    BUTTON_SIZE = (25, 2)
    PADDING = (10, 10)
    
    PRIMARY_COLOR = '#2B5B84'    # Dark Blue
    SECONDARY_COLOR = '#A5D8FF'  # Light Blue
    WHITE = '#FFFFFF'
    BLACK = '#000000'

    title_section = [
        [sg.Text('Sistema de Gestão de Publicações Científicas', 
                font=TITLE_FONT, 
                justification='center', 
                pad=((0, 0), (20, 30)))]
    ]
    
    button_sections = [
        [sg.Button('Carregar Base de Dados', size=BUTTON_SIZE, font=BUTTON_FONT, pad=PADDING, button_color=(WHITE, PRIMARY_COLOR)),
         sg.Button('Guardar Base de Dados', size=BUTTON_SIZE, font=BUTTON_FONT, pad=PADDING, button_color=(WHITE, PRIMARY_COLOR))],
        
        [sg.Button('Adicionar Publicação', size=BUTTON_SIZE, font=BUTTON_FONT, pad=PADDING, button_color=(BLACK, SECONDARY_COLOR)),
         sg.Button('Editar Publicação', size=BUTTON_SIZE, font=BUTTON_FONT, pad=PADDING, button_color=(BLACK, SECONDARY_COLOR))],
        
        [sg.Button('Pesquisar Publicações', size=BUTTON_SIZE, font=BUTTON_FONT, pad=PADDING, button_color=(WHITE, PRIMARY_COLOR)),
         sg.Button('Listar Autores', size=BUTTON_SIZE, font=BUTTON_FONT, pad=PADDING, button_color=(WHITE, PRIMARY_COLOR))],
        
        [sg.Button('Análise de Keywords', size=BUTTON_SIZE, font=BUTTON_FONT, pad=PADDING, button_color=(BLACK, SECONDARY_COLOR)),
         sg.Button('Estatísticas', size=BUTTON_SIZE, font=BUTTON_FONT, pad=PADDING, button_color=(BLACK, SECONDARY_COLOR))],
        
        [sg.Button('Eliminar Publicação', size=BUTTON_SIZE, font=BUTTON_FONT, pad=PADDING, button_color=(WHITE, PRIMARY_COLOR)),
         sg.Button('Sair', size=BUTTON_SIZE, font=BUTTON_FONT, pad=PADDING, button_color=(WHITE, PRIMARY_COLOR))]
    ]
    
    layout = [
        [sg.Column(title_section, element_justification='center', expand_x=True)],
        [sg.HorizontalSeparator(pad=((0, 0), (0, 20)))],
        [sg.Column(button_sections, element_justification='center', expand_x=True)]
    ]
    
    window = sg.Window('Sistema de Publicações', 
                      layout,
                      finalize=True,
                      size=(800, 600),
                      resizable=True,
                      element_justification='center')
    window.set_min_size((700, 500))
    
    return window

def main():
    sistema = SistemaPubs()
    window = criar_interface_grafica()
    
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, 'Sair'):
            sistema.guardar_base_dados()
            break

        if event == 'Carregar Base de Dados':
            layout = [
                [sg.Text("Carregar Ficheiro", font=('Helvetica', 14, 'bold'), pad=(0, 10))],
                [sg.Text("Nome do ficheiro:", font=('Helvetica', 11)), 
                 sg.Input(key='Nome do ficheiro a carregar:', size=(30, 1))],
                [sg.Button('Carregar', button_color=('white', '#2B5B84'), size=(12, 1), font=('Helvetica', 11)),
                 sg.Button('Cancelar', button_color=('black', '#A5D8FF'), size=(12, 1), font=('Helvetica', 11))]
            ]

            janela_load = sg.Window('Carregar Publicação', layout, finalize=True, element_justification='center')
            janela_load.set_min_size((400, 150))

            while True:
                evento_load, valores = janela_load.read()
                if evento_load in (sg.WIN_CLOSED, 'Cancelar'):
                    break
                elif evento_load == "Carregar":
                    fnome = valores['Nome do ficheiro a carregar:']
                    if sistema.carregar_base_dados(fnome):
                        sg.popup("Base de dados carregada com sucesso!", 
                               title="Sucesso",
                               font=('Helvetica', 11),
                               button_color=('white', '#2B5B84'))
                    else:
                        sg.popup("Erro ao carregar a base de dados.", 
                               title="Erro",
                               font=('Helvetica', 11),
                               button_color=('white', '#2B5B84'))
            janela_load.close()
        
        elif event == 'Guardar Base de Dados':
            if sistema.guardar_base_dados():
                sg.popup("Base de dados guardada com sucesso!", 
                        title="Sucesso",
                        font=('Helvetica', 11),
                        button_color=('white', '#2B5B84'))
            else:
                sg.popup("Erro ao guardar a base de dados.", 
                        title="Erro",
                        font=('Helvetica', 11),
                        button_color=('white', '#2B5B84'))
        
        elif event == 'Adicionar Publicação':
            layout = [
                [sg.Text('Adicionar Nova Publicação', font=('Helvetica', 16, 'bold'), pad=(0, 20))],
                [sg.Text('Título:', font=('Helvetica', 11, 'bold')), 
                 sg.Input(key='titulo', size=(40, 1), font=('Helvetica', 11))],
                [sg.Text('Resumo:', font=('Helvetica', 11, 'bold')), 
                 sg.Multiline(key='abstract', size=(40, 5), font=('Helvetica', 11))],
                [sg.Text('Palavras-chave:', font=('Helvetica', 11, 'bold')), 
                 sg.Input(key='keywords', size=(40, 1), font=('Helvetica', 11))],
                [sg.Text('Autores (JSON):', font=('Helvetica', 11, 'bold')), 
                 sg.Multiline(key='authors', size=(40, 4), font=('Helvetica', 11))],
                [sg.Text('DOI:', font=('Helvetica', 11, 'bold')), 
                 sg.Input(key='doi', size=(40, 1), font=('Helvetica', 11))],
                [sg.Text('PDF URL:', font=('Helvetica', 11, 'bold')), 
                 sg.Input(key='pdf', size=(40, 1), font=('Helvetica', 11))],
                [sg.Text('Data:', font=('Helvetica', 11, 'bold')), 
                 sg.Input(key='publish_date', size=(40, 1), font=('Helvetica', 11))],
                [sg.Text('URL:', font=('Helvetica', 11, 'bold')), 
                 sg.Input(key='url', size=(40, 1), font=('Helvetica', 11))],
                [sg.Button('Adicionar', button_color=('white', '#2B5B84'), size=(15, 1), font=('Helvetica', 11)),
                 sg.Button('Cancelar', button_color=('black', '#A5D8FF'), size=(15, 1), font=('Helvetica', 11))]
            ]
            
            janela_add = sg.Window('Adicionar Publicação', layout, finalize=True, element_justification='left')
            janela_add.set_min_size((600, 600))
            while True:
                evento_add, valores_add = janela_add.read()
                if evento_add in(sg.WINDOW_CLOSED, 'Cancelar'):
                    break
                if evento_add == 'Adicionar':
                    try:
                        autores = json.loads(valores_add['authors'])
                        dados = {
                            'title': valores_add['titulo'],
                            'abstract': valores_add['abstract'],
                            'keywords': valores_add['keywords'],
                            'authors': autores,
                            'doi': valores_add['doi'],
                            'pdf': valores_add['pdf'],
                            'publish_date': valores_add['publish_date'],
                            'url': valores_add['url']
                        }

                        if sistema.criar_publicacao(dados):
                            sg.popup("Publicação adicionada com sucesso!", 
                                title="Sucesso",
                                font=('Helvetica', 11),
                                button_color=('white', '#2B5B84'))
                            break
                        else:
                            sg.popup("Erro ao adicionar publicação.", 
                                title="Erro",
                                font=('Helvetica', 11),
                                button_color=('white', '#2B5B84'))
                    except Exception as e:
                        sg.popup(f"Erro: {str(e)}", 
                            title="Erro",
                            font=('Helvetica', 11),
                            button_color=('white', '#2B5B84'))
                janela_add.close()

        elif event == 'Editar Publicação':
            layout = [
                [sg.Text('Título da publicação:', font=('Helvetica', 11)), 
                 sg.Input(key='title', size=(40, 1))],
                [sg.Button('Procurar', button_color=('white', '#2B5B84'), size=(12, 1)),
                 sg.Button('Cancelar', button_color=('black', '#A5D8FF'), size=(12, 1))]
            ]
            janela_edit = sg.Window('Editar Publicação', layout, finalize=True)
            janela_edit.set_min_size((500, 100))

            while True:
                evento_edit, valores_edit = janela_edit.read()
                if evento_edit in (sg.WIN_CLOSED, 'Cancelar'):
                    break
                elif evento_edit == 'Procurar':
                    artigo = sistema.searchSpecific(valores_edit['title'])
                    if artigo:
                        layout_edit = [
                            [sg.Text('Detalhes da Publicação', font=('Helvetica', 16, 'bold'), pad=(0, 20))]
                        ]
                        
                        for key, value in artigo.items():
                            layout_edit.append([
                                sg.Text(f'{key}:', size=(12, 1), font=('Helvetica', 11, 'bold')),
                                sg.Multiline(default_text=str(value), size=(50, 3), key=f'input_{key}',
                                           font=('Helvetica', 11))
                            ])
                        
                        layout_edit.append([
                            sg.Button('Salvar', button_color=('white', '#2B5B84'), size=(12, 1)),
                            sg.Button('Cancelar', button_color=('black', '#A5D8FF'), size=(12, 1))
                        ])
                        
                        janela_edit_2 = sg.Window('Editar Publicação', 
                                                [[sg.Column(layout_edit, scrollable=True, vertical_scroll_only=True)]], 
                                                finalize=True, resizable=True)
                        janela_edit_2.set_min_size((700, 600))
                        
                        while True:
                            evento_edit_2, valores_edit_2 = janela_edit_2.read()
                            if evento_edit_2 in (sg.WIN_CLOSED, 'Cancelar'):
                                break
                            elif evento_edit_2 == 'Salvar':
                                for key in artigo:
                                    artigo[key] = valores_edit_2[f'input_{key}']
                                sg.popup('Alterações salvas com sucesso!',
                                       font=('Helvetica', 11),
                                       button_color=('white', '#2B5B84'))
                                break
                        janela_edit_2.close()
                    else:
                        sg.popup('Artigo não encontrado!',
                               font=('Helvetica', 11),
                               button_color=('white', '#2B5B84'))
            janela_edit.close()

        elif event == 'Pesquisar Publicações':
            layout_pesq = [
                [sg.Text('Critério de Pesquisa:', font=('Helvetica', 11))],
                [sg.Combo(['titulo', 'autor', 'afiliacao', 'data', 'keywords'], 
                         key='criterio', size=(30, 1), font=('Helvetica', 11))],
                [sg.Text('Valor:', font=('Helvetica', 11)), 
                 sg.Input(key='valor', size=(30, 1), font=('Helvetica', 11))],
                [sg.Button('Pesquisar', button_color=('white', '#2B5B84'), size=(12, 1)),
                 sg.Button('Cancelar', button_color=('black', '#A5D8FF'), size=(12, 1))]
            ]
            janela_pesq = sg.Window('Pesquisar Publicações', layout_pesq, finalize=True)
            janela_pesq.set_min_size((400, 150))

            while True:
                evento_pesq, valores_pesq = janela_pesq.read()
                if evento_pesq in (sg.WIN_CLOSED, 'Cancelar'):
                    break

                if evento_pesq == 'Pesquisar':
                    resultados = sistema.pesquisar_publicacoes(valores_pesq['criterio'], valores_pesq['valor'])
                    if resultados:
                        layout_resultados = [
                            [sg.Text('Resultados da Pesquisa:', font=('Helvetica', 14, 'bold'))],
                            [sg.Multiline(json.dumps(resultados, ensure_ascii=False, indent=4),
                                        size=(60, 20), disabled=True, font=('Helvetica', 11))],
                            [sg.Button('Exportar', button_color=('white', '#2B5B84'), size=(12, 1)),
                             sg.Button('Fechar', button_color=('black', '#A5D8FF'), size=(12, 1))]
                        ]
                        janela_resultados = sg.Window('Resultados de Pesquisa', layout_resultados,
                                                    finalize=True, resizable=True)
                        janela_resultados.set_min_size((500, 400))

                        while True:
                            evento_res, _ = janela_resultados.read()
                            if evento_res in (sg.WINDOW_CLOSED, 'Fechar'):
                                break

def criar_interface_grafica():
    sg.theme('LightGrey1')  # Modern, clean theme
    
    title_font = ('Helvetica', 24, 'bold')
    button_font = ('Helvetica', 12, 'bold')
    padding = (10, 10)
    button_size = (25, 2)
    
    title_section = [
        [sg.Text('Sistema de Gestão de Publicações Científicas', 
                font=title_font, 
                justification='center', 
                pad=((0, 0), (20, 30)))]
    ]
    
    data_section = [
        [sg.Button('Carregar Base de Dados', 
                  size=button_size, 
                  font=button_font, 
                  pad=padding,
                  button_color=('white', '#2B5B84')),
         sg.Button('Guardar Base de Dados', 
                  size=button_size, 
                  font=button_font, 
                  pad=padding,
                  button_color=('white', '#2B5B84'))]
    ]
    
    manage_section = [
        [sg.Button('Adicionar Publicação', 
                  size=button_size, 
                  font=button_font, 
                  pad=padding,
                  button_color=('white', '#2B5B84')),
         sg.Button('Editar Publicação', 
                  size=button_size, 
                  font=button_font, 
                  pad=padding,
                  button_color=('white', '#2B5B84'))]
    ]
    
    search_section = [
        [sg.Button('Pesquisar Publicações', 
                  size=button_size, 
                  font=button_font, 
                  pad=padding,
                  button_color=('white', '#2B5B84')),
         sg.Button('Listar Autores', 
                  size=button_size, 
                  font=button_font, 
                  pad=padding,
                  button_color=('white', '#2B5B84'))]
    ]
    
    analysis_section = [
        [sg.Button('Análise de Keywords', 
                  size=button_size, 
                  font=button_font, 
                  pad=padding,
                  button_color=('white', '#2B5B84')),
         sg.Button('Estatísticas', 
                  size=button_size, 
                  font=button_font, 
                  pad=padding,
                  button_color=('white', '#2B5B84'))]
    ]
    
    action_section = [
        [sg.Button('Eliminar Publicação', 
                  size=button_size, 
                  font=button_font, 
                  pad=padding,
                  button_color=('white', '#2B5B84')),
         sg.Button('Sair', 
                  size=button_size, 
                  font=button_font, 
                  pad=padding,
                  button_color=('white', '#2B5B84'))]
    ]
    
    layout = [
        [sg.Column(title_section, element_justification='center', expand_x=True)],
        [sg.HorizontalSeparator(pad=((0, 0), (0, 20)))],
        [sg.Column(data_section, element_justification='center', expand_x=True)],
        [sg.Column(manage_section, element_justification='center', expand_x=True)],
        [sg.Column(search_section, element_justification='center', expand_x=True)],
        [sg.Column(analysis_section, element_justification='center', expand_x=True)],
        [sg.Column(action_section, element_justification='center', expand_x=True)]
    ]
    
    window = sg.Window('Sistema de Publicações', 
                      layout,
                      finalize=True,
                      size=(800, 600),
                      resizable=True,
                      element_justification='center')
    window.set_min_size((700, 500))
    
    return window

def main():
    #Função principal que inicia o sistema
    sistema = SistemaPubs()
    window = criar_interface_grafica()
    
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Sair':
            sistema.guardar_base_dados()
            break

        if event == 'Carregar Base de Dados':
            layout = [
                [sg.Text("Carregar Ficheiro")],
                [sg.Input(key='Nome do ficheiro a carregar:')],
                [sg.Button('Carregar',button_color=('white', '#2B5B84')), sg.Button('Cancelar',button_color=('white', '#2B5B84'))]
            ]

            janela_load = sg.Window('Carregar Publicação', layout)
            while True:
                evento_load, valores = janela_load.read()
                if evento_load in (sg.WIN_CLOSED, 'Cancelar'):
                    break
                elif evento_load == "Carregar":
                    fnome = valores['Nome do ficheiro a carregar:']
                    if sistema.carregar_base_dados(fnome):
                        sg.popup("Base de dados carregada com sucesso!", title="Sucesso")
                    else:
                        sg.popup("Erro ao carregar a base de dados.", title="Erro")
        
        elif event == 'Guardar Base de Dados':
            if sistema.guardar_base_dados():
                sg.popup("Base de dados guardada com sucesso!", title="Sucesso")
            else:
                sg.popup("Erro ao guardar a base de dados.", title="Erro")
        
        elif event == 'Adicionar Publicação':
            layout = [
                [sg.Text('Título:', font=('Helvetica',12,'bold')), sg.Input(key='titulo',size=(20,8),expand_x=True)],
                [sg.Text('Resumo:', font=('Helvetica',12,'bold')), sg.Multiline(key='abstract',size=(20,5),expand_x=True)],
                [sg.Text('Palavras-chave\n (separadas por vírgula):', font=('Helvetica',12,'bold')), sg.Input(key='keywords',size=(20,8),expand_x=True)],
                [sg.Text('Autores (JSON, \n ex: [{"name": "Autor", \n "affiliation": "Univ",\n "orcid": "0000"}]):', font=('Helvetica',12,'bold')), sg.Multiline(key='authors',size=(20,5),expand_x=True)],
                [sg.Text('DOI:', font=('Helvetica',12,'bold')), sg.Input(key='doi',size=(20,8),expand_x=True)],
                [sg.Text('PDF URL:', font=('Helvetica',12,'bold')), sg.Input(key='pdf',size=(20,8),expand_x=True)],
                [sg.Text('Data de Publicação\n (YYYY-MM-DD):', font=('Helvetica',12,'bold')), sg.Input(key='publish_date',size=(20,8),expand_x=True)],
                [sg.Text('URL do Artigo:', font=('Helvetica',12,'bold')), sg.Input(key='url',size=(20,8),expand_x=True)],
                [sg.Button('Adicionar',button_color=('white', '#2B5B84')), sg.Button('Cancelar',button_color=('white', '#2B5B84'))]
            ]
            janela_add = sg.Window('Adicionar Publicação', layout, finalize=True, size=(800,430))
            #janela_add.Maximize()
            evento_add, valores_add = janela_add.read()
            if evento_add == 'Adicionar':
                try:
                    # Validação e conversão dos dados
                    autores = json.loads(valores_add['authors'])  # Tenta converter autores para JSON
                    if not isinstance(autores, list):
                        raise ValueError("Autores devem ser uma lista de objetos JSON.")
                    
                    dados = {
                        'title': valores_add['titulo'],
                        'abstract': valores_add['abstract'],
                        'keywords': valores_add['keywords'],
                        'authors': autores,
                        'doi': valores_add['doi'],
                        'pdf': valores_add['pdf'],
                        'publish_date': valores_add['publish_date'],
                        'url': valores_add['url']
                    }

                    # Tenta criar a publicação
                    if sistema.criar_publicacao(dados):
                        sg.popup("Publicação adicionada com sucesso!", title="Sucesso")
                    else:
                        sg.popup("Erro ao adicionar publicação. Verifique os dados.", title="Erro")
                except json.JSONDecodeError:
                    sg.popup("Formato inválido para os autores. Insira um JSON válido.", title="Erro")
                except ValueError as ve:
                    sg.popup(str(ve), title="Erro")
                except Exception as e:
                    sg.popup(f"Erro inesperado: {e}", title="Erro")
            janela_add.close()
        
        elif event == 'Editar Publicação':
            layout = [
                [sg.Text('Título da publicação que deseja editar:'), sg.Input(key='title')],
                [sg.Button('Procurar',button_color=('white', '#2B5B84')), sg.Button('Cancelar',button_color=('white', '#2B5B84'))]
            ]
            janela_edit = sg.Window('Editar Publicação', layout)
            while True:
                evento_edit, valores_edit = janela_edit.read()
                if evento_edit in (sg.WIN_CLOSED, 'Cancelar'):  # Trata fechamento ou cancelamento
                    break
                elif evento_edit == 'Procurar':
                    artigo = {}
                    for i in sistema.publicacoes:
                        if i["title"] == valores_edit['title']:  # Verifica se o artigo é o que se pretende alterar
                            artigo = i
                            break

                    if artigo != {}:
                        # Criar layout dinâmico com campos editáveis para o artigo
                        layout_editar = []

                        layout_editar.append([sg.Text()])

                        for chave, valor in artigo.items():
                            layout_editar.append([
                                sg.Text(f'{chave.upper()}:', size=(10, 1), font=('Helvetica', 20, 'bold'), justification = 'left'),  # Key label
                                sg.Multiline(default_text=str(valor), size=(182, 5), expand_x=True, disabled=True), sg.Stretch()  # Wrap text
                            ])

                        
                        layout_editar.append([sg.Text()])
                        layout_editar.append([sg.Text()])
                        # Adiciona campos de entrada editáveis
                        layout_editar.extend([
                            [sg.Text(f"Novo {chave}:", font=('Helvetica',12,'bold')), sg.Input(default_text=str(valor), key=f'input_{chave}', size=(30, 50), expand_x=True)]
                            for chave, valor in artigo.items()
                        ])

                        layout_editar.append([sg.Text()])

                        # Botões de confirmação e cancelamento
                        layout_editar.append([sg.Button('Confirmar', size =(20,2), font=('Helvetica',12,'bold'),button_color=('white', '#2B5B84')), sg.Button('Cancelar', size=(20,2), font=('Helvetica',12,'bold'),button_color=('white', '#2B5B84'))])

                        # Envolve o layout em um sg.Column para torná-lo scrollable
                        scrollable_layout = [
                            [sg.Column(layout_editar, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True)]  # Scrollable column
                        ]

                        # Cria a janela com o layout scrollable
                        janela_edit_2 = sg.Window('Editar Publicação', scrollable_layout, finalize=True, resizable=True)
                        janela_edit_2.Maximize()
                        while True:
                            evento_edit_2, valores_edit_2 = janela_edit_2.read()
                            if evento_edit_2 in (sg.WIN_CLOSED, 'Cancelar'):  # Trata fechamento ou cancelamento
                                break
                            elif evento_edit_2 == 'Confirmar':
                                # Atualiza o artigo diretamente na base de dados
                                for chave in valores_edit_2:
                                    artigo[chave] = valores_edit_2.get[f'input_{chave}']
                                sg.popup("Alterações salvas com sucesso!", title="Sucesso")
                                break
                        janela_edit_2.close()
                    else:
                        sg.popup('Artigo não encontrado!')
            janela_edit.close()


        elif event == 'Pesquisar Publicações':
            resultados = {}
            layout_pesq = [
                [sg.Text('Critério de Pesquisa:'), sg.Combo(['titulo', 'autor', 'afiliacao', 'data', 'keywords'], key='criterio')],
                [sg.Text('Valor:'), sg.Input(key='valor')],
                [sg.Button('Pesquisar',button_color=('white', '#2B5B84')), sg.Button('Cancelar',button_color=('white', '#2B5B84'))]
            ]
            janela_pesq = sg.Window('Pesquisar Publicações', layout_pesq)

            while True:
                evento_pesq, valores_pesq = janela_pesq.read()
                if evento_pesq in (sg.WIN_CLOSED, 'Cancelar'):  # Encerrar a janela
                    break

                if evento_pesq == 'Pesquisar':
                    # Realiza a pesquisa
                    resultados = sistema.pesquisar_publicacoes(valores_pesq['criterio'], valores_pesq['valor'])

                    if resultados:
                        # Exibe os resultados
                        layout_resultados = [
                            [sg.Text('Resultados da Pesquisa:')],
                            [sg.Multiline(json.dumps(resultados, ensure_ascii=False, indent=4), size=(60, 20), disabled=True,expand_x=True,expand_y=True)],
                            [sg.Button('Exportar Resultados',button_color=('white', '#2B5B84')), sg.Button('Fechar',button_color=('white', '#2B5B84'))]
                        ]
                        janela_resultados = sg.Window('Resultados de Pesquisa', layout_resultados, finalize=True)
                        janela_resultados.Maximize()

                        while True:
                            evento_res, _ = janela_resultados.read()
                            if evento_res in (sg.WIN_CLOSED, 'Fechar'):
                                janela_resultados.close()
                                break

                            if evento_res == 'Exportar Resultados':
                                # Pergunta se deseja exportar
                                layout_exportar = [
                                    [sg.Text('Nome do arquivo para exportar os resultados:')],
                                    [sg.Input(key='fnome'), sg.FileSaveAs(file_types=(("JSON Files", "*.json"),))],
                                    [sg.Button('Exportar',button_color=('white', '#2B5B84')), sg.Button('Cancelar',button_color=('white', '#2B5B84'))]
                                ]
                                janela_exportar = sg.Window('Exportar Resultados', layout_exportar)

                                evento_exp, valores_exp = janela_exportar.read()
                                if evento_exp in (sg.WIN_CLOSED, 'Cancelar'):
                                    janela_exportar.close()
                                    continue

                                if evento_exp == 'Exportar':
                                    # Exporta os resultados para o arquivo especificado
                                    nome_arquivo = valores_exp.get('fnome', '').strip()
                                    if nome_arquivo:
                                        try:
                                            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                                                json.dump(resultados, f, ensure_ascii=False, indent=4)
                                            sg.popup("Resultados exportados com sucesso!", title="Sucesso")
                                        except Exception as e:
                                            sg.popup(f"Erro ao exportar resultados: {e}", title="Erro")
                                    else:
                                        sg.popup("Por favor, insira um nome de arquivo válido.", title="Erro")
                                    janela_exportar.close()

            janela_pesq.close()


        elif event == 'Listar Autores':
            layout = [
                [sg.Text("Escolha o método de ordenação:")],
                [sg.Button("Ordenar por ordem alfabética",button_color=('white', '#2B5B84')), sg.Button("Ordenar por número de ocorrências",button_color=('white', '#2B5B84')), sg.Button("Cancelar",button_color=('white', '#2B5B84'))]
            ]
            janela_auth = sg.Window('Análise de Palavras-Chave', layout)
            
            while True:
                evento_auth, _ = janela_auth.read()
                if evento_auth in (sg.WIN_CLOSED, 'Cancelar'):  # Trata fechamento ou cancelamento
                    break
                elif evento_auth == 'Ordenar por ordem alfabética':
                    analise_auth = sistema.analisar_autores("alfabetica")
                    sg.popup_scrolled(
                        json.dumps(analise_auth, ensure_ascii=False, indent=4),
                        title="Análise de Autores - Ordem Alfabética"
                    )
                elif evento_auth == 'Ordenar por número de ocorrências':
                    analise_auth = sistema.analisar_autores("frequencia")
                    sg.popup_scrolled(
                        json.dumps(analise_auth, ensure_ascii=False, indent=4),
                        title="Análise de Autores - Número de Ocorrências"
                    )
            janela_auth.close()
            
        
        elif event == 'Análise de Keywords':
            layout = [
                [sg.Text("Escolha o método de ordenação:")],
                [sg.Button("Ordenar por ordem alfabética",button_color=('white', '#2B5B84')), sg.Button("Ordenar por número de ocorrências",button_color=('white', '#2B5B84')), sg.Button("Cancelar",button_color=('white', '#2B5B84'))]
            ]
            janela_keys = sg.Window('Análise de Palavras-Chave', layout)
            
            while True:
                evento_keys, _ = janela_keys.read()
                if evento_keys in (sg.WIN_CLOSED, 'Cancelar'):  # Trata fechamento ou cancelamento
                    break
                elif evento_keys == 'Ordenar por ordem alfabética':
                    analise_keywords = sistema.analisar_keywords("alfabetica")
                    sg.popup_scrolled(
                        json.dumps(analise_keywords, ensure_ascii=False, indent=4),
                        title="Análise de Keywords - Ordem Alfabética"
                    )
                elif evento_keys == 'Ordenar por número de ocorrências':
                    analise_keywords = sistema.analisar_keywords("frequencia")
                    sg.popup_scrolled(
                        json.dumps(analise_keywords, ensure_ascii=False, indent=4),
                        title="Análise de Keywords - Número de Ocorrências"
                    )
            janela_keys.close()
        
        elif event == 'Estatísticas':
            layout = [
                [sg.Text('Tipo de Estatística:')],
                [sg.Button('Publicações por ano',button_color=('white', '#2B5B84')), sg.Button('Publicações por mês, num ano',button_color=('white', '#2B5B84'))],
                [sg.Button('Top 20 autores',button_color=('white', '#2B5B84')), sg.Button('Publicações de um autor',button_color=('white', '#2B5B84'))],
                [sg.Button('Top 20 keywords',button_color=('white', '#2B5B84')), sg.Button('Keywords por ano',button_color=('white', '#2B5B84'))],
                [sg.Button('Cancelar',button_color=('white', '#2B5B84'))]
            ]
            janela_est = sg.Window('Gerar Estatísticas', layout)
            evento_est, valores_est = janela_est.read()
            if evento_est in (sg.WINDOW_CLOSED or 'Cancelar'):
                break
            elif evento_est == 'Publicações por ano':
                sistema.graph("1")
            elif evento_est == 'Publicações por mês, num ano':
                layout = [
                    [sg.Text('Ano que deseja visualizar:'),sg.Input(key = 'ano')],
                    [sg.Button('Visualizar',button_color=('white', '#2B5B84')), sg.Button('Cancelar',button_color=('white', '#2B5B84'))]
                ]
                janela_stat = sg.Window('Estatísticas', layout)
                evento_stat, valor_stat = janela_stat.read()
                if evento_stat in (sg.WINDOW_CLOSED or 'Cancelar'):
                    break
                elif evento_stat == 'Visualizar':
                    sistema.graph('2',valor_stat['ano'])
            elif evento_est == 'Top 20 autores':
                sistema.graph('3')
            elif evento_est == 'Publicações de um autor':
                layout = [
                    [sg.Text('Autor que deseja visualizar:'),sg.Input(key = 'autor')],
                    [sg.Button('Visualizar',button_color=('white', '#2B5B84')), sg.Button('Cancelar',button_color=('white', '#2B5B84'))]
                ]
                janela_stat = sg.Window('Estatísticas', layout)
                evento_stat, valor_stat = janela_stat.read()
                if evento_stat in (sg.WINDOW_CLOSED or 'Cancelar'):
                    break
                elif evento_stat == 'Visualizar':
                    sistema.graph('4',valor_stat['autor'])
            elif evento_est == 'Top 20 keywords':
                sistema.graph('5')
            elif evento_est == 'Keywords por ano':
                sistema.graph('6')
            janela_est.close()

        elif event == 'Eliminar Publicação':
            sistema.eliminar_publicacao_interface()
    
    window.close()

if __name__ == "__main__":
    main()