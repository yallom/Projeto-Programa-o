import json
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from typing import Dict, List


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

    def atualizar_publicacao(self, titulo: str, dados_novos: Dict) -> bool:
        #Atualiza uma publicação existente
        try:
            for i, pub in enumerate(self.publicacoes):
                if pub['title'] == titulo:
                    # Atualiza apenas os campos fornecidos
                    for campo, valor in dados_novos.items():
                        self.publicacoes[i][campo] = valor
                    return True
            print("Publicação não encontrada")
            return False
        except Exception as e:
            print(f"Erro ao atualizar publicação: {e}")
            return False

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
        #Análise de autores e suas publicações
        contagem_autores = {}
        try:
            # Conta publicações por autor
            for pub in self.publicacoes:
                for autor in pub['authors']:
                    nome = autor['name']
                    if nome not in contagem_autores:
                        contagem_autores[nome] = {'Ocorrências': 1, 'Artigos': [pub['title']]}
                    else:
                        contagem_autores[nome]['Ocorrências'] += 1
                        contagem_autores[nome]['Artigos'].append(pub['title'])

            # Ordena conforme solicitado
            if ordenacao == "alfabetica":
                return sorted(contagem_autores.items())
            elif ordenacao == "frequencia":  # frequencia
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


    def gerar_graficos(self, tipo: str, parametros: Dict = None) -> None:
        #Gera diferentes tipos de gráficos estatísticos
        try:
            plt.figure(figsize=(10, 6))
            
            if tipo == "pub_por_ano":
                # Distribuição de publicações por ano
                anos = {}
                for pub in self.publicacoes:
                    ano = pub['publish_date'][:4]
                    anos[ano] = anos.get(ano, 0) + 1
                
                plt.bar(anos.keys(), anos.values())
                plt.title("Publicações por Ano")
                plt.xlabel("Ano")
                plt.ylabel("Número de Publicações")

            elif tipo == "pub_por_mes" and parametros and 'ano' in parametros:
                # Distribuição de publicações por mês num ano específico
                meses = {}
                ano_alvo = parametros['ano']
                for pub in self.publicacoes:
                    if pub['publish_date'].startswith(ano_alvo):
                        mes = pub['publish_date'][5:7]
                        meses[mes] = meses.get(mes, 0) + 1
                
                plt.bar(meses.keys(), meses.values())
                plt.title(f"Publicações por Mês em {ano_alvo}")
                plt.xlabel("Mês")
                plt.ylabel("Número de Publicações")

            elif tipo == "top_autores":
                # Top 20 autores por número de publicações
                analise = self.analisar_autores()[:20]
                autores = [a[0] for a in analise]
                contagens = [a[1]['Ocorrências'] for a in analise]
                
                plt.bar(autores, contagens)
                plt.title("Top 20 Autores por Número de Publicações")
                plt.xticks(rotation=45, ha='right')
                plt.ylabel("Número de Publicações")

            elif tipo == "pub_autor_anos" and parametros and 'autor' in parametros:
                # Publicações de um autor específico por ano
                autor_alvo = parametros['autor']
                anos = {}
                for pub in self.publicacoes:
                    if any(autor['name'] == autor_alvo for autor in pub['authors']):
                        ano = pub['publish_date'][:4]
                        anos[ano] = anos.get(ano, 0) + 1
                
                plt.bar(anos.keys(), anos.values())
                plt.title(f"Publicações de {autor_alvo} por Ano")
                plt.xlabel("Ano")
                plt.ylabel("Número de Publicações")

            elif tipo == "top_keywords":
                # Top 20 palavras-chave por frequência
                analise = self.analisar_keywords()[:20]
                keywords = [k[0] for k in analise]
                contagens = [k[1]['Ocorrências'] for k in analise]
                
                plt.bar(keywords, contagens)
                plt.title("Top 20 Palavras-chave por Frequência")
                plt.xticks(rotation=45, ha='right')
                plt.ylabel("Frequência")

            elif tipo == "keywords_por_ano":
                # Palavras-chave mais frequentes por ano
                anos_kw = {}
                for pub in self.publicacoes:
                    ano = pub['publish_date'][:4]
                    if ano not in anos_kw:
                        anos_kw[ano] = {}
                    
                    keywords = [k.strip() for k in pub['keywords'].split(',')]
                    for kw in keywords:
                        anos_kw[ano][kw] = anos_kw[ano].get(kw, 0) + 1
                
                # Encontra a palavra-chave mais frequente para cada ano
                top_kw_por_ano = {ano: max(kws.items(), key=lambda x: x[1])[0] 
                                for ano, kws in anos_kw.items()}
                
                plt.bar(top_kw_por_ano.keys(), [1]*len(top_kw_por_ano))
                plt.title("Palavra-chave Mais Frequente por Ano")
                plt.xticks(rotation=45, ha='right')
                
                # Adiciona as palavras-chave como anotações
                for i, (ano, kw) in enumerate(top_kw_por_ano.items()):
                    plt.text(i, 1.1, kw, rotation=45, ha='right')

            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"Erro ao gerar gráfico: {e}")

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

def criar_interface_grafica():
    #Cria a interface gráfica do sistema
    sg.theme('LightGrey1')
    
    layout_principal = [
        [sg.Text('Sistema de Gestão de Publicações Científicas', font=('Helvetica', 20))],
        [sg.Button('Carregar Base de Dados', size=(20, 1)), 
         sg.Button('Guardar Base de Dados', size=(20, 1))],
        [sg.Button('Adicionar Publicação', size=(20, 1)), 
         sg.Button('Editar Publicação', size=(20, 1))],
        [sg.Button('Pesquisar Publicações', size=(20, 1)), 
         sg.Button('Listar Autores', size=(20, 1))],
        [sg.Button('Análise de Keywords', size=(20, 1)), 
         sg.Button('Estatísticas', size=(20, 1))],
        [sg.Button('Sair', size=(20, 1))]
    ]
    
    return sg.Window('Sistema de Publicações', layout_principal, finalize=True)

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
                [sg.Button('Carregar'), sg.Button('Cancelar')]
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
                [sg.Text('Título:'), sg.Input(key='titulo')],
                [sg.Text('Resumo:'), sg.Multiline(key='abstract')],
                [sg.Text('Palavras-chave (separadas por vírgula):'), sg.Input(key='keywords')],
                [sg.Text('Autores (JSON, ex: [{"name": "Autor", "affiliation": "Univ", "orcid": "0000"}]):'), sg.Multiline(key='authors')],
                [sg.Text('DOI:'), sg.Input(key='doi')],
                [sg.Text('PDF URL:'), sg.Input(key='pdf')],
                [sg.Text('Data de Publicação (YYYY-MM-DD):'), sg.Input(key='publish_date')],
                [sg.Text('URL do Artigo:'), sg.Input(key='url')],
                [sg.Button('Adicionar'), sg.Button('Cancelar')]
            ]
            janela_add = sg.Window('Adicionar Publicação', layout)
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
        
        elif event == 'Pesquisar Publicações':
            layout = [
                [sg.Text('Critério de Pesquisa:'), sg.Combo(['titulo', 'autor', 'afiliacao', 'data', 'keywords'], key='criterio')],
                [sg.Text('Valor:'), sg.Input(key='valor')],
                [sg.Button('Pesquisar'), sg.Button('Cancelar')]
            ]
            janela_pesq = sg.Window('Pesquisar Publicações', layout)
            evento_pesq, valores_pesq = janela_pesq.read()
            if evento_pesq == 'Pesquisar':
                resultados = sistema.pesquisar_publicacoes(valores_pesq['criterio'], valores_pesq['valor'])
                sg.popup_scrolled(json.dumps(resultados, ensure_ascii=False, indent=4), title="Resultados da Pesquisa")
            janela_pesq.close()

        elif event == 'Listar Autores':
            layout = [
                [sg.Text("Escolha o método de ordenação:")],
                [sg.Button("Ordenar por ordem alfabética"), sg.Button("Ordenar por número de ocorrências"), sg.Button("Cancelar")]
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
                [sg.Button("Ordenar por ordem alfabética"), sg.Button("Ordenar por número de ocorrências"), sg.Button("Cancelar")]
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
                [sg.Text('Tipo de Estatística:'), sg.Combo(['pub_por_ano', 'pub_por_mes', 'top_autores', 'top_keywords', 'keywords_por_ano'], key='tipo')],
                [sg.Text('Parâmetros (JSON):'), sg.Input(key='parametros')],
                [sg.Button('Gerar Gráfico'), sg.Button('Cancelar')]
            ]
            janela_est = sg.Window('Gerar Estatísticas', layout)
            evento_est, valores_est = janela_est.read()
            if evento_est == 'Gerar Gráfico':
                parametros = json.loads(valores_est['parametros']) if valores_est['parametros'] else {}
                sistema.gerar_graficos(valores_est['tipo'], parametros)
            janela_est.close()
    
    window.close()

if __name__ == "__main__":
    main()