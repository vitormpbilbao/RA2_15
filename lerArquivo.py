import ast

def lerTokenStr(nomeArquivo):
    """
    Lê o arquivo de tokens, corrige quebras de linha no meio dos dicionários
    e converte o texto bruto em uma lista
    """
    try:
        with open(nomeArquivo, "r", encoding="utf-8") as arquivo:
            # le
            conteudo = arquivo.read()
            # tira as quebras de linha
            conteudo_limpo = conteudo.replace("\n", "")
            # coloca virgula entre os tokens
            conteudo_limpo = conteudo_limpo.replace("][", "],[")
            # envolve em colchetes
            texto_final = f"[{conteudo_limpo}]"
            # tranforma a string
            lista_de_listas = ast.literal_eval(texto_final)
            # achata para lista unica
            tokens_finais = []
            for sublista in lista_de_listas:
                tokens_finais.extend(sublista)

            print(f"Arquivo '{nomeArquivo}' lido e convertido com sucesso!")
            return tokens_finais

    except FileNotFoundError:
        print(
            f"Erro, não foi possível abrir o arquivo '{nomeArquivo}'. Verifique o caminho."
        )
        return []
    except Exception as e:
        print(f"Erro ao tentar converter o conteúdo do arquivo: {e}")
        return []
