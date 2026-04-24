"""
Testes de Integração do Parser LL(1)
Fase 2 do Compilador - Aluno 2

Testes que validam o parser com tokens sintetizados.

Execute este arquivo para testar:
    python test_parsear.py
"""

import sys
from pathlib import Path

# Adicionar caminho ao path
sys.path.insert(0, str(Path(__file__).parent))

from parsear import parsear, agruparTokensPorComando, ParserLL1

try:
    from gramatica import calcularFirst, calcularFollow, construirTabelaLL1
except Exception as e:
    print(f"Erro ao importar módulos: {e}")
    gramatica = {
        "Programa": [["PARENTESIS_ESQ", "START", "PARENTESIS_DIR", "ListaOuFim"]],
        "ListaOuFim": [["PARENTESIS_ESQ", "ConteudoOuFim"]],
        "ConteudoOuFim": [
            ["END", "PARENTESIS_DIR"],
            ["Conteudo", "PARENTESIS_DIR", "ListaOuFim"],
        ],
        "Comando": [["PARENTESIS_ESQ", "Conteudo", "PARENTESIS_DIR"]],
        "Conteudo": [["Elemento", "RestoConteudo"]],
        "RestoConteudo": [["Elemento", "Cauda"], ["RES"], ["EPSILON"]],
        "Cauda": [["OPERADOR"], ["MEM"], ["IF"], ["WHILE"]],
        "Elemento": [["NUMERO"], ["VARIAVEL"], ["Comando"]],
    }


def criar_token(tipo, valor):
    """Helper para criar token."""
    return {"tipo": tipo, "valor": valor}


def criar_tokens_programa_simples(expressao_tokens):
    """Encapsula uma expressão em (START) ... (END)"""
    tokens = [
        criar_token("PARENTESIS", "("),
        criar_token("NUMERO", "START"),
        criar_token("PARENTESIS", ")"),
    ]
    tokens.extend(expressao_tokens)
    tokens.extend(
        [
            criar_token("PARENTESIS", "("),
            criar_token("NUMERO", "END"),
            criar_token("PARENTESIS", ")"),
        ]
    )
    return tokens


def teste_agrupamento_basico():
    """Teste 1: Agrupamento básico de tokens."""
    print("\nTESTE 1: Agrupamento básico de tokens\n")

    tokens = [
        criar_token("PARENTESIS", "("),
        criar_token("NUMERO", "1"),
        criar_token("PARENTESIS", ")"),
        criar_token("PARENTESIS", "("),
        criar_token("NUMERO", "2"),
        criar_token("PARENTESIS", ")"),
    ]

    comandos = agruparTokensPorComando(tokens)

    assert len(comandos) == 2, "Esperava 2 comandos"
    print("OK Agrupamento simples: OK (%d comandos)" % len(comandos))

    return True


def teste_agrupamento_aninhado():
    """Teste 2: Agrupamento com aninhamento."""
    print("\nTESTE 2: Agrupamento com aninhamento\n")

    tokens = [
        criar_token("PARENTESIS", "("),
        criar_token("NUMERO", "1"),
        criar_token("PARENTESIS", "("),
        criar_token("NUMERO", "2"),
        criar_token("PARENTESIS", ")"),
        criar_token("PARENTESIS", ")"),
    ]

    comandos = agruparTokensPorComando(tokens)

    assert len(comandos) == 1, "Esperava 1 comando aninhado"
    assert len(comandos[0]) == 6, "Esperava 6 tokens no comando"
    print("OK Agrupamento aninhado: OK")

    return True


def teste_numero_simples():
    """Teste 3: Parsing de número simples."""
    print("\nTESTE 3: Parsing de número simples\n")

    # (START) (42) (END)
    tokens = criar_tokens_programa_simples(
        [
            criar_token("PARENTESIS", "("),
            criar_token("NUMERO", "42"),
            criar_token("PARENTESIS", ")"),
        ]
    )

    resultado = parsear(tokens, gramatica)

    if resultado["sucesso"]:
        print("OK Número simples: OK")
        print("  Resumo: %s" % resultado["resumo"])
        return True
    else:
        print("X Número simples: FALHOU")
        if resultado["resultados"]:
            print("  Erros: %s" % resultado["resultados"][0].get("erros"))
        return False


def teste_variavel_simples():
    """Teste 4: Parsing de variável simples."""
    print("\nTESTE 4: Parsing de variável simples\n")

    # (START) (X) (END)
    tokens = criar_tokens_programa_simples(
        [
            criar_token("PARENTESIS", "("),
            criar_token("VARIAVEL", "X"),
            criar_token("PARENTESIS", ")"),
        ]
    )

    resultado = parsear(tokens, gramatica)

    if resultado["sucesso"]:
        print("OK Variável simples: OK")
        print("  Resumo: %s" % resultado["resumo"])
        return True
    else:
        print("X Variável simples: FALHOU")
        return False


def teste_operacoes_aritmeticas():
    """Teste 5: Operações aritméticas."""
    print("\nTESTE 5: Operações aritméticas\n")

    operadores = ["+", "-", "*", "/", "//", "%", "^"]
    sucessos = 0

    for op in operadores:
        # (START) (10 5 op) (END)
        tokens = criar_tokens_programa_simples(
            [
                criar_token("PARENTESIS", "("),
                criar_token("NUMERO", "10"),
                criar_token("NUMERO", "5"),
                criar_token("OPERADOR", op),
                criar_token("PARENTESIS", ")"),
            ]
        )

        resultado = parsear(tokens, gramatica)

        if resultado["sucesso"]:
            print("OK Operador '%s': OK" % op)
            sucessos += 1
        else:
            print("X Operador '%s': FALHOU" % op)

    return sucessos == len(operadores)


def teste_comando_mem():
    """Teste 6: Comando MEM (armazenar)."""
    print("\nTESTE 6: Comando MEM\n")

    # (START) (100 X MEM) (END)
    tokens = criar_tokens_programa_simples(
        [
            criar_token("PARENTESIS", "("),
            criar_token("NUMERO", "100"),
            criar_token("VARIAVEL", "X"),
            criar_token("COMANDO", "MEM"),
            criar_token("PARENTESIS", ")"),
        ]
    )

    resultado = parsear(tokens, gramatica)

    if resultado["sucesso"]:
        print("OK Comando MEM: OK")
        return True
    else:
        print("X Comando MEM: FALHOU")
        return False


def teste_comando_res():
    """Teste 7: Comando RES (recuperar)."""
    print("\nTESTE 7: Comando RES\n")

    # (START) (1 RES) (END)
    tokens = criar_tokens_programa_simples(
        [
            criar_token("PARENTESIS", "("),
            criar_token("NUMERO", "1"),
            criar_token("COMANDO", "RES"),
            criar_token("PARENTESIS", ")"),
        ]
    )

    resultado = parsear(tokens, gramatica)

    if resultado["sucesso"]:
        print("OK Comando RES: OK")
        return True
    else:
        print("X Comando RES: FALHOU")
        return False


def teste_estrutura_if():
    """Teste 8: Estrutura IF."""
    print("\nTESTE 8: Estrutura IF\n")

    # (START) (10 5 > IF) (END)
    tokens = criar_tokens_programa_simples(
        [
            criar_token("PARENTESIS", "("),
            criar_token("NUMERO", "10"),
            criar_token("NUMERO", "5"),
            criar_token("OPERADOR", ">"),
            criar_token("COMANDO", "IF"),
            criar_token("PARENTESIS", ")"),
        ]
    )

    resultado = parsear(tokens, gramatica)

    if resultado["sucesso"]:
        print("OK Estrutura IF: OK")
        return True
    else:
        print("X Estrutura IF: FALHOU")
        return False


def teste_estrutura_while():
    """Teste 9: Estrutura WHILE."""
    print("\nTESTE 9: Estrutura WHILE\n")

    # (START) (X 0 < WHILE) (END)
    tokens = criar_tokens_programa_simples(
        [
            criar_token("PARENTESIS", "("),
            criar_token("VARIAVEL", "X"),
            criar_token("NUMERO", "0"),
            criar_token("OPERADOR", "<"),
            criar_token("COMANDO", "WHILE"),
            criar_token("PARENTESIS", ")"),
        ]
    )

    resultado = parsear(tokens, gramatica)

    if resultado["sucesso"]:
        print("OK Estrutura WHILE: OK")
        return True
    else:
        print("X Estrutura WHILE: FALHOU")
        return False


def teste_estrutura_for():
    """Teste 10: Estrutura FOR."""
    print("\nTESTE 10: Estrutura FOR\n")

    # (START) (I 1 10 FOR) (END)
    tokens = criar_tokens_programa_simples(
        [
            criar_token("PARENTESIS", "("),
            criar_token("VARIAVEL", "I"),
            criar_token("NUMERO", "1"),
            criar_token("NUMERO", "10"),
            criar_token("COMANDO", "FOR"),
            criar_token("PARENTESIS", ")"),
        ]
    )

    resultado = parsear(tokens, gramatica)

    if resultado["sucesso"]:
        print("OK Estrutura FOR: OK")
        return True
    else:
        print("X Estrutura FOR: FALHOU")
        return False


def teste_aninhamento():
    """Teste 11: Expressões aninhadas."""
    print("\nTESTE 11: Expressões aninhadas\n")

    # (START) ((10 5 +) 3 *) (END)
    tokens = criar_tokens_programa_simples(
        [
            criar_token("PARENTESIS", "("),
            criar_token("PARENTESIS", "("),
            criar_token("NUMERO", "10"),
            criar_token("NUMERO", "5"),
            criar_token("OPERADOR", "+"),
            criar_token("PARENTESIS", ")"),
            criar_token("NUMERO", "3"),
            criar_token("OPERADOR", "*"),
            criar_token("PARENTESIS", ")"),
        ]
    )

    resultado = parsear(tokens, gramatica)

    if resultado["sucesso"]:
        print("OK Aninhamento duplo: OK")
        return True
    else:
        print("X Aninhamento duplo: FALHOU")
        return False


def teste_multiplos_comandos():
    """Teste 12: Múltiplos comandos."""
    print("\nTESTE 12: Múltiplos comandos\n")

    # (START) (10) (20) (END)
    tokens = criar_tokens_programa_simples(
        [
            criar_token("PARENTESIS", "("),
            criar_token("NUMERO", "10"),
            criar_token("PARENTESIS", ")"),
            criar_token("PARENTESIS", "("),
            criar_token("NUMERO", "20"),
            criar_token("PARENTESIS", ")"),
        ]
    )

    resultado = parsear(tokens, gramatica)

    if resultado["sucesso"]:
        print("OK Múltiplos comandos: OK")
        print("  Resumo: %s" % resultado["resumo"])
        return True
    else:
        print("X Múltiplos comandos: FALHOU")
        return False


def teste_erro_parentesis_nao_fechado():
    """Teste 13: Erro - parêntese não fechado."""
    print("\nTESTE 13: Detecção de erro - parêntese não fechado\n")

    # (START) (10 (20) (END) <- sem fechar (10
    tokens = [
        criar_token("PARENTESIS", "("),
        criar_token("NUMERO", "START"),
        criar_token("PARENTESIS", ")"),
        criar_token("PARENTESIS", "("),
        criar_token("NUMERO", "10"),
        criar_token("PARENTESIS", "("),
        criar_token("NUMERO", "20"),
        criar_token("PARENTESIS", ")"),
        # Falta fechar (10
        criar_token("PARENTESIS", "("),
        criar_token("NUMERO", "END"),
        criar_token("PARENTESIS", ")"),
    ]

    resultado = parsear(tokens, gramatica)

    if not resultado["sucesso"]:
        print("OK Erro detectado: parêntese não fechado")
        if resultado["resultados"]:
            erros = resultado["resultados"][-1].get("erros", [])
            if erros:
                print("  Mensagem: %s" % erros[0]["mensagem"])
        return True
    else:
        print("X Erro não foi detectado")
        return False


def teste_parser_ll1_direto():
    """Teste 14: Classe ParserLL1 direta."""
    print("\nTESTE 14: Classe ParserLL1 diretamente\n")

    parser = ParserLL1(gramatica)

    if parser.gramatica:
        print("OK Parser inicializado")
        print("  Não-terminais: %d" % len(parser.gramatica))

        # Testar obterTerminal
        token_num = criar_token("NUMERO", "42")
        terminal = parser.obterTerminal(token_num)
        assert terminal == "NUMERO", "Terminal incorreto para NUMERO"

        token_var = criar_token("VARIAVEL", "X")
        terminal = parser.obterTerminal(token_var)
        assert terminal == "VARIAVEL", "Terminal incorreto para VARIAVEL"

        print("OK Mapeamento de terminais OK")
        return True
    else:
        print("X Gramática não carregada")
        return False


def teste_arvore_sintatica():
    """Teste 15: Geração de árvore sintática."""
    print("\nTESTE 15: Geração de árvore sintática\n")

    tokens = criar_tokens_programa_simples(
        [
            criar_token("PARENTESIS", "("),
            criar_token("NUMERO", "5"),
            criar_token("PARENTESIS", ")"),
        ]
    )

    resultado = parsear(tokens, gramatica)

    if resultado["sucesso"] and resultado["resultados"]:
        arvore = resultado["resultados"][0].get("arvore")
        if arvore:
            print("OK Árvore sintática gerada")
            print("  Raiz: '%s'" % arvore["rotulo"])
            print("  Tipo: %s" % arvore["tipo"])
            print("  Filhos: %d" % len(arvore["filhos"]))
            return True

    print("X Árvore sintática não gerada")
    return False


def main():
    """Executa todos os testes."""
    print("\nSUITE DE TESTES - PARSER LL(1) ALUNO 2\n")

    testes = [
        ("Agrupamento básico", teste_agrupamento_basico),
        ("Agrupamento aninhado", teste_agrupamento_aninhado),
        ("Número simples", teste_numero_simples),
        ("Variável simples", teste_variavel_simples),
        ("Operações aritméticas", teste_operacoes_aritmeticas),
        ("Comando MEM", teste_comando_mem),
        ("Comando RES", teste_comando_res),
        ("Estrutura IF", teste_estrutura_if),
        ("Estrutura WHILE", teste_estrutura_while),
        ("Estrutura FOR", teste_estrutura_for),
        ("Aninhamento", teste_aninhamento),
        ("Múltiplos comandos", teste_multiplos_comandos),
        ("Erro - parêntese não fechado", teste_erro_parentesis_nao_fechado),
        ("Parser LL(1) direto", teste_parser_ll1_direto),
        ("Árvore sintática", teste_arvore_sintatica),
    ]

    resultados = []

    for nome, teste_func in testes:
        try:
            resultado = teste_func()
            resultados.append((nome, resultado))
        except Exception as e:
            print("X Exceção: %s" % str(e))
            resultados.append((nome, False))

    # Resumo final
    print("\nRESUMO DOS TESTES\n")

    sucessos = sum(1 for _, r in resultados if r)
    total = len(resultados)

    for nome, resultado in resultados:
        status = "OK" if resultado else "X"
        print("%s %s" % (status, nome))

    print(f"\nTOTAL: {sucessos}/{total} testes passaram\n")

    return sucessos == total


if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
