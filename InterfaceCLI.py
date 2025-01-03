import Projeto as p

level = (-1)
while level != (0):
    print("""Menu de Utilizador
      [1] Carregar Base de Dados
      [2] Adicionar Publicação    
      [3] Pesquisar Publicação
      [4] Análise de Palavras-Chave
      [5] Guardar base de Dados
      [6] Editar Publicação
      [7] Eliminar Publicação
      [8] Listar Autores
      [9] Estatísticas""")

    level = int(input("Escolha a opção: "))
    if level == 1:
        nome = input("Insira o nome do ficheiro que pretende carregar: ")
        p.carregaFicheiro(nome)
    elif level == 2:
        abstract=input("Escreva o abstrato do artigo: ")
        keywords=input("Escreva as palavras-chave do artigo: ")
        autores=[]
        nomeautor = "abc"
        aux = 1
        print("Para interromper a introdução de mais autores, definir nome de novo autor como 0.")
        while nomeautor[0] != "0":
            nomeautor = input(f"Inserir o nome do autor {aux}: ")
            afiliação = input(f"Inserir a afiliação do autor {aux}: ")
            if nomeautor[0] == 0 and aux == 1:
                print("O artigo tem de ter pelo menos um autor.")
                nomeautor = "abc"
            elif nomeautor[0] == "0" and aux != 1:
                aux += 1
            else:
                autores.append({"name": nomeautor, "affiliation": afiliação})
                aux += 1
        link1=input("Insira o link para o DOI do artigo: ")
        pdf=input("Insira o link para um ficheiro pdf do artigo: ")
        data=input("Escreva a data de publicação do artigo: ")
        title=input("Escreva o título do artigo: ")
        link2=input("Insira o link para o artigo: ")
        p.insPaper(abstract, keywords, autores, link1, pdf, data, title, link2)
    elif level == 3:
        print("""Menu de Eliminação
      [1] Pesquisar por título
      [2] Pesquisar por palavras-chave
      [3] Pesquisar por data
      [4] Pesquisar por autor
      [5] Pesquisar por afiliação""")
        resposta = int(input("Que opção pretende tomar: "))
        aux = p.searchPaper(resposta)
        print(aux)
    elif level == 4:
        print(p.listarkeywords("2"))
    elif level == 5:
        nome = input("Escreva o nome do ficheiro que vai guardar: ")
        p.guardaFicheiro(f"{nome}.json", p.Paper_file)
    elif level == 6:        
        titulo = p.searchPaper(1)[0]["title"]
        title = input("Deseja alterar o título do artigo? s/n: ")
        abstract = input("Deseja alterar o abstrato do artigo? s/n: ")
        keywords = input("Deseja alterar as palavras-chave do artigo? s/n: ")
        authors = input("Deseja alterar os autores do artigo? s/n: ")
        data = input("Deseja alterar a data do artigo? s/n: ")
        p.editarPaper(titulo, title, abstract, keywords, authors, data)
    elif level == 7:
        titulo = input("Escreva o titulo do artigo que vai eliminar: ")
        if p.eliminar_publicacao(titulo):
            print(f"""O artigo "{titulo}" foi eliminado.""")
        else:
            print(f"""O artigo "{titulo}" não foi encontrado.""")
    elif level == 8:
        print(p.listarauth(1))
    elif level == 9:
        p.graph()
