# ==========================================
# Responsável: Vitor Matias, Andrei Bley e Vinicius Cordeiro
# ==========================================
import sys
from analisador_lexico import lerTokens                     #aluno3
from gramatica import construirGramatica                    #aluno1
from parsear import parsear                                 #aluno2
from gerarAssembly import gerarArvore, gerarAssembly, imprimir_arvore, salvar_arvore_json #aluno4

def main():
    #verifica se o nome do arquivo foi passado como argumento
    if len(sys.argv) < 2:
        print("Uso correto: python main.py <arquivo_teste.txt>")
        sys.exit(1)
    nome_arquivo = sys.argv[1]
    print(f"\n{'=' * 50}")
    print("COMPILADOR RPN -> ASSEMBLY ARMv7 (Fase 2)")
    print(f"{'=' * 50}\n")

    try:
        # ==========================================
        # PASSO 1: ANALISADOR LÉXICO
        # ==========================================
        print("[1/5] Tokenizando arquivo fonte...")
        # O lerTokens devolve uma lista de listas de tokens
        tokens_brutos = lerTokens(nome_arquivo)
        
        # O Parser espera uma lista plana, então nós "achatamos" a lista aqui
        tokens_planificados = [token for linha in tokens_brutos for token in linha]
        print(f"OK! {len(tokens_planificados)} tokens lidos.\n")
        # ==========================================
        # PASSO 2: A PLANTA DA LINGUAGEM
        # ==========================================
        print("[2/5] Carregando a Gramática LL(1)...")
        gramatica = construirGramatica()
        print("OK! Gramática fatorada carregada.\n")

        # ==========================================
        # PASSO 3: ANALISADOR SINTÁTICO
        # ==========================================
        print("[3/5] Executando Análise Sintática (Parsing)...")
        resultado_parser = parsear(tokens_planificados, gramatica)
        
        # Mostra erros, se houver
        if not resultado_parser["sucesso"]:
            print("[ERRO] O código possui erros sintáticos:")
            for r in resultado_parser["resultados"]:
                if not r["sucesso"]:
                    for erro in r["erros"]:
                        print(f"      -> {erro['mensagem']}")
            sys.exit(1)
        print(f"OK! {resultado_parser['resumo']}.\n")
        # ==========================================
        # PASSO 4: ÁRVORE SINTÁTICA
        # ==========================================
        print("[4/5] Gerando Árvore Sintática (AST)...")
        arvores = gerarArvore(resultado_parser)
        salvar_arvore_json(arvores, "arvore.json")
        
        print("OK! Árvore salva em 'arvore.json'. Primeira estrutura:")
        if arvores and arvores[0] is not None:
            print(imprimir_arvore(arvores[0], prefixo="        "))
        print("")

        # ==========================================
        # PASSO 5: GERAÇÃO DE CÓDIGO
        # ==========================================
        print("[5/5] Traduzindo para Assembly ARMv7...")
        codigo_assembly = gerarAssembly(arvores)
        
        with open("saida.s", "w", encoding="utf-8") as f:
            f.write(codigo_assembly)
        print("OK! Código salvo no arquivo 'saida.s'.\n")

        print(f"{'=' * 50}")
        print("COMPILAÇÃO CONCLUÍDA")
        print(f"{'=' * 50}\n")

    except Exception as e:
        print(f"\n ERRO: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()