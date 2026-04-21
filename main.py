# Nome | apelido no Github | link do Github
# Andrei de Carvalho Bley | TODO: inserir usuario/apelido do github aqui
# Vinicius Cordeiro Vogt | vinivaldox | https://github.com/vinivaldox
# Vitor Matias Percegona Bilbao | TODO: inserir usuario/apelido do github aqui

# Grupo: RA1 15
# Aluno 4: Interface do Usuário e Integração Final

import sys
from analisador_lexico import parseExpressao, ler_teste
from gerarAssembly import gerarAssembly
from geren_memo import executarExpressao, validarToken, memoria, historico


def exibirResultados(resultados: list) -> None:
    """Exibe os resultados das expressões.

    Parameters
    ----------
    resultados : list
        Lista de resultados (dict ou float)
    """
    print("\n" + "=" * 70)
    print("RESULTADOS DAS EXPRESSOES")
    print("=" * 70)

    for i, resultado in enumerate(resultados, 1):
        if resultado is not None:
            # Se for dict, mostra o tipo
            if isinstance(resultado, dict):
                tipo = resultado.get("tipo", "desconhecido")
                print(f"Linha {i}: {tipo}")
            else:
                # Se for número, mostra com 1 casa decimal
                try:
                    print(f"Linha {i}: {float(resultado):.1f}")
                except Exception:
                    print(f"Linha {i}: {resultado}")
        else:
            print(f"Linha {i}: ERRO")

    print("=" * 70 + "\n")


def salvarAssembly(assembly: str, nome_arquivo: str = "saida.s") -> None:
    """Salva código Assembly em arquivo.

    Parameters
    ----------
    assembly : str
        Código Assembly a salvar
    nome_arquivo : str
        Nome do arquivo de saída
    """
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(assembly)
        print(f"Assembly salvo em: {nome_arquivo}")
    except IOError as e:
        print(f"Erro ao salvar Assembly: {e}")


def main():
    """Função principal - Integra todos os alunos.

    Fluxo:
    1. Lê arquivo (Aluno 1)
    2. Para cada linha:
       a. Tokeniza (Aluno 1)
       b. Executa (Aluno 2)
       c. Gera Assembly (Aluno 3)
    3. Exibe e salva resultados (Aluno 4)
    """

    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo_teste.txt>")
        sys.exit(1)

    nome_arquivo = sys.argv[1]

    print(f"\n{'=' * 70}")
    print("COMPILADOR RPN → ASSEMBLY ARMv7")
    print(f"{'=' * 70}")
    print(f"Arquivo: {nome_arquivo}\n")

    try:
        # Lê arquivo (Aluno 1)
        linhas = ler_teste(nome_arquivo)
        print(f"{len(linhas)} linhas lidas\n")

        resultados = []
        todos_tokens_dicts = []
        tokens_por_linha = []  # Armazena tokens de cada linha
        assembly_completo = ""

        # Processa cada linha
        for i, linha in enumerate(linhas, 1):
            print(f"Linha {i}: {linha}")

            try:
                # ===== ALUNO 1: Tokenização =====
                tokens_obj = parseExpressao(linha)
                # Converte Token objects para dicts
                tokens_dicts = [t.to_dict() for t in tokens_obj]
                tokens_por_linha.append(tokens_dicts)  # Armazena para salvar depois
                todos_tokens_dicts.extend(tokens_dicts)

                print(f"Tokenização OK ({len(tokens_obj)} tokens)")

                # ===== ALUNO 2: Execução =====
                arvore = executarExpressao(tokens_dicts)  # , memoria, historico)
                valido, mensagem = validarToken(arvore, i, memoria, historico)

                if valido:
                    resultados.append(arvore)
                    if arvore:
                        historico.append(arvore)
                    print(f"{mensagem}")
                else:
                    print(f"{mensagem}")
                    resultados.append(None)

            except Exception as e:
                print(f"Erro: {e}")
                resultados.append(None)

        # ===== ALUNO 3: Geração Assembly =====
        try:
            if todos_tokens_dicts:
                assembly_completo = gerarAssembly(todos_tokens_dicts)
                print("\n Assembly gerado")
        except Exception as e:
            print(f"\n Erro ao gerar Assembly: {e}")

        # ===== ALUNO 4: Exibição e Salvamento =====
        # Exibe resultados
        if resultados:
            exibirResultados(resultados)

        # Salva Assembly
        if assembly_completo:
            salvarAssembly(assembly_completo, "saida.s")

        # Salva tokens em arquivo
        try:
            with open("token.txt", "w", encoding="utf-8") as f:
                for tokens_linha in tokens_por_linha:
                    f.write(str(tokens_linha) + "\n")
            print("Arquivo de tokens salvo: token.txt")
        except Exception as e:
            print(f"Erro ao salvar tokens: {e}")

        print("Compilação concluída!\n")

    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
