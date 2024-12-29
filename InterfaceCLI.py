import Projeto as p

level = (-1)
while level != (0):
    print("""Menu de Utilizador
      [1] Pesquisar publicações
      [2] Listar autores
      [3] Listar Keywords
      [4] Criar Publicação
      [5] Eliminar Publicação
      [6] Guardar Ficheiro
      [0] Fechar Menu""")
    level = int(input("Escolha a opção: "))
    if level == 1:
        aux = p.searchPaper(4)
        print(aux)
    elif level == 2:
        print(p.listarauth(1))
    elif level == 3:
        print(p.listarkeywords("2"))
    elif level == 4:
        abstract=input("Escreva o abstrato do artigo: ")
        keywords=input("Escreva as palavras chave do artigo: ")
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
    elif level == 5:
        p.elimPaper()
    elif level == 6:
        p.guardaFicheiro()