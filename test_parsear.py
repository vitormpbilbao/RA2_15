"""
Testes de Integração do Parser LL(1)
Fase 2 do Compilador

Testes que validam o parser com a gramática real do Aluno 1
e tokens reais do Aluno 3.

Execute este arquivo para testar a integração completa:
    python test_parsear.py
"""

import sys
from pathlib import Path

# Adicionar caminho da branch aluno-1 ao Python path (para importar gramatica)
sys.path.insert(0, str(Path(__file__).parent))

from parsear import parsear, agruparTokensPorComando
from lerArquivo import lerTokenStr

# Caminho absoluto do diretório do script
SCRIPT_DIR = Path(__file__).parent


def teste_agrupamento_simples():
    """Teste básico de agrupamento de tokens."""
    print("\n[TESTE 1] Agrupamento simples de tokens")

    tokens = [
        {"tipo": "PARENTESIS", "valor": "("},
        {"tipo": "NUMERO", "valor": "1"},
        {"tipo": "PARENTESIS", "valor": ")"},
        {"tipo": "PARENTESIS", "valor": "("},
        {"tipo": "NUMERO", "valor": "2"},
        {"tipo": "PARENTESIS", "valor": ")"},
    ]

    comandos = agruparTokensPorComando(tokens)

    assert len(comandos) == 2, f"Esperava 2 comandos, encontrou {len(comandos)}"
    assert len(comandos[0]) == 3
    assert len(comandos[1]) == 3

    print(" Agrupamento funciona corretamente")
    print(f"   Entrada: {len(tokens)} tokens")
    print(f"   Saída: {len(comandos)} comandos agrupados")


def teste_agrupamento_aninhado():
    """Teste agrupamento com comandos aninhados."""
    print("\n[TESTE 2] Agrupamento com aninhamento")

    tokens = [
        {"tipo": "PARENTESIS", "valor": "("},
        {"tipo": "PARENTESIS", "valor": "("},
        {"tipo": "NUMERO", "valor": "1"},
        {"tipo": "NUMERO", "valor": "2"},
        {"tipo": "OPERADOR", "valor": "+"},
        {"tipo": "PARENTESIS", "valor": ")"},
        {"tipo": "NUMERO", "valor": "3"},
        {"tipo": "OPERADOR", "valor": "*"},
        {"tipo": "PARENTESIS", "valor": ")"},
    ]

    comandos = agruparTokensPorComando(tokens)

    assert len(comandos) == 1, f"Esperava 1 comando, encontrou {len(comandos)}"
    assert len(comandos[0]) == 9

    print(" Agrupamento com aninhamento funciona")
    print(f"   Entrada: {len(tokens)} tokens")
    print(f"   Saída: {len(comandos)} comando com {len(comandos[0])} tokens")


def teste_com_lerTokenStr():
    """Teste integração com lerTokenStr do Aluno 3."""
    print("\n[TESTE 3] Integração com lerTokenStr")

    try:
        token_file = SCRIPT_DIR / "token.txt"
        tokens = lerTokenStr(str(token_file))
        if not tokens:
            print(" Arquivo token.txt vazio ou não encontrado")
            return

        comandos = agruparTokensPorComando(tokens)

        print(f" Tokens lidos: {len(tokens)}")
        print(f" Comandos agrupados: {len(comandos)}")

        for i, cmd in enumerate(comandos[:3], 1):
            print(f"   Comando {i}: {len(cmd)} tokens")

    except FileNotFoundError:
        print(" Arquivo token.txt não encontrado")


def teste_parsear_completo():
    """Teste parsing completo com gramática real."""
    print("\n[TESTE 4] Parsing completo com gramática")

    try:
        token_file = SCRIPT_DIR / "token.txt"
        tokens = lerTokenStr(str(token_file))
        if not tokens:
            print(" Arquivo token.txt vazio")
            return

        print(f"Parseando {len(tokens)} tokens...")
        resultado = parsear(tokens)

        print(f"\nResultado: {resultado['resumo']}\n")

        if resultado["sucesso"]:
            print(" PARSING BEM-SUCEDIDO!")
        else:
            print(" PARSING COM ERROS")
            for res in resultado["resultados"]:
                if res["erros"]:
                    print(f"\n   Comando {res['numero_comando']}:")
                    for erro in res["erros"]:
                        print(f"     - {erro['mensagem']}")

    except FileNotFoundError:
        print(" Arquivo token.txt não encontrado")
    except ImportError:
        print(" Gramática não disponível (aluno-1 não importada)")


def teste_com_arquivo_teste():
    """Teste com arquivos de teste do Aluno 3."""
    print("\n[TESTE 5] Teste com arquivo teste1fase2.txt")

    try:
        teste_file = SCRIPT_DIR / "teste1fase2.txt"
        # Ler manualmente o arquivo de teste
        with open(teste_file, "r") as f:
            conteudo = f.read()

        linhas = [
            i.strip()
            for i in conteudo.split("\n")
            if i.strip() and not i.strip().startswith("#")
        ]

        print(f"Arquivo teste1fase2.txt tem {len(linhas)} comandos")
        for i, linha in enumerate(linhas[:5], 1):
            print(f"   {i}. {linha}")

        print(" Arquivo de teste lido com sucesso")

    except FileNotFoundError:
        # arquivo de teste do aluno 3
        print(" Arquivo teste1fase2.txt não encontrado")


if __name__ == "__main__":
    print("TESTES DE INTEGRAÇÃO - PARSER LL(1) - ALUNO 2")

    try:
        teste_agrupamento_simples()
        teste_agrupamento_aninhado()
        teste_com_lerTokenStr()
        teste_parsear_completo()
        teste_com_arquivo_teste()

        print("\nBATERIA DE TESTES CONCLUÍDA")

    except Exception as e:
        print(f"\n ERRO NOS TESTES: {e}")
        import traceback

        traceback.print_exc()
