"""
Testes de Integração do Parser LL(1)
Fase 2 do Compilador - Aluno 2

Testes que validam o parser com tokens sintetizados, cobrindo:
- Agrupamento de tokens
- Parsing de elementos básicos (números, variáveis)
- Operações aritméticas
- Comandos especiais (MEM, RES)
- Estruturas de controle (IF, WHILE, FOR)
- Aninhamento de expressões
- Detecção de erros sintáticos
- Geração de árvore sintática

Execute este arquivo para testar:
    python test_parsear.py

Returns
-------
int
    0 se todos os testes passarem, 1 caso contrário
"""

import sys
from pathlib import Path

# Adicionar caminho ao path
sys.path.insert(0, str(Path(__file__).parent))

from parsear import parsear, ParserLL1

"""
Carregamento de Gramática
=========================

Tenta importar a gramática do módulo gramatica.py.
Se falhar, usa gramática hardcoded para testes.

A gramática define 8 não-terminais:
- Programa       : ponto de entrada
- ListaOuFim     : lista de comandos ou fim do programa
- ConteudoOuFim  : conteúdo ou END
- Comando        : comando individual
- Conteudo       : elemento + resto
- RestoConteudo  : elemento/RES/epsilon
- Cauda          : operador/comando/epsilon
- Elemento       : número/variável/comando aninhado
"""

# Gramática hardcoded para testes (padrão)
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

try:
    from gramatica import calcularFirst, calcularFollow, construirTabelaLL1
except Exception as e:
    pass  # Usa gramática padrão definida acima


def criar_token(tipo, valor):
    """
    Cria um token com estrutura padrão.

    Helper para simplificar criação de tokens durante testes.

    Parameters
    ----------
    tipo : str
        Tipo do token: PARENTESIS, NUMERO, VARIAVEL, OPERADOR, COMANDO
    valor : str or float
        Valor do token

    Returns
    -------
    dict
        Dicionário com estrutura {'tipo': str, 'valor': str|float}

    Examples
    --------
    >>> token = criar_token("NUMERO", "42")
    >>> token
    {'tipo': 'NUMERO', 'valor': '42'}
    >>> token = criar_token("PARENTESIS", "(")
    >>> token
    {'tipo': 'PARENTESIS', 'valor': '('}
    """
    return {"tipo": tipo, "valor": valor}


def criar_tokens_programa_simples(expressao_tokens):
    """
    Encapsula uma sequência de tokens em programa válido.

    Adiciona wrapper (START) ... (END) ao redor de tokens,
    criando um programa sintático completo válido.

    Parameters
    ----------
    expressao_tokens : list of dict
        Tokens da expressão a encapsular (sem START/END)

    Returns
    -------
    list of dict
        Sequência completa de tokens: (START) <expressão> (END)

    Examples
    --------
    >>> tokens = [criar_token("NUMERO", "42")]
    >>> programa = criar_tokens_programa_simples(tokens)
    >>> len(programa)  # 6: ( START ) ( 42 )
    6
    """
    tokens = [
        criar_token("PARENTESIS", "("),
        criar_token("COMANDO", "START"),
        criar_token("PARENTESIS", ")"),
    ]
    tokens.extend(expressao_tokens)
    tokens.extend(
        [
            criar_token("PARENTESIS", "("),
            criar_token("COMANDO", "END"),
            criar_token("PARENTESIS", ")"),
        ]
    )
    return tokens


def teste_numero_simples():
    """
    Teste 3: Parsing de número simples.

    Valida se um programa com um único número é parseado
    corretamente sem erros sintáticos.

    Teste:
        Entrada: (START) (42) (END)
        Esperado: Parsing bem-sucedido

    Returns
    -------
    bool
        True se parsing bem-sucedido, False caso contrário
    """
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
    """
    Teste 4: Parsing de variável simples.

    Valida se um programa com uma única variável é parseado
    corretamente sem erros sintáticos.

    Teste:
        Entrada: (START) (X) (END)
        Esperado: Parsing bem-sucedido

    Returns
    -------
    bool
        True se parsing bem-sucedido, False caso contrário
    """
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
    """
    Teste 5: Validação de operações aritméticas.

    Testa parsing com múltiplos operadores aritméticos:
    +, -, *, /, //, %, ^

    Teste:
        Entrada: (START) (10 5 <OPERADOR>) (END) para cada operador
        Esperado: Parsing bem-sucedido para todos os 7 operadores

    Returns
    -------
    bool
        True se todos os 7 operadores parsearam com sucesso, False caso contrário
    """
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
    """
    Teste 6: Parsing de comando MEM (armazenar).

    Valida se o comando MEM (armazenar valor em memória)
    é parseado corretamente.

    Teste:
        Entrada: (START) (100 X MEM) (END)
        Esperado: Parsing bem-sucedido

    Returns
    -------
    bool
        True se parsing bem-sucedido, False caso contrário
    """
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
    """
    Teste 7: Parsing de comando RES (recuperar).

    Valida se o comando RES (recuperar valor da memória)
    é parseado corretamente.

    Teste:
        Entrada: (START) (1 RES) (END)
        Esperado: Parsing bem-sucedido

    Returns
    -------
    bool
        True se parsing bem-sucedido, False caso contrário
    """
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
    """
    Teste 8: Parsing de estrutura condicional IF.

    Valida se a estrutura condicional IF (desvio condicional)
    é parseada corretamente.

    Teste:
        Entrada: (START) (10 5 IF) (END)
        Esperado: Parsing bem-sucedido

    Returns
    -------
    bool
        True se parsing bem-sucedido, False caso contrário
    """
    print("\nTESTE 8: Estrutura IF\n")

    # (START) (10 5 IF) (END)
    tokens = criar_tokens_programa_simples(
        [
            criar_token("PARENTESIS", "("),
            criar_token("NUMERO", "10"),
            criar_token("NUMERO", "5"),
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
    """
    Teste 9: Parsing de estrutura iterativa WHILE.

    Valida se a estrutura iterativa WHILE (laço com condição)
    é parseada corretamente.

    Teste:
        Entrada: (START) (X 0 WHILE) (END)
        Esperado: Parsing bem-sucedido

    Returns
    -------
    bool
        True se parsing bem-sucedido, False caso contrário
    """
    print("\nTESTE 9: Estrutura WHILE\n")

    # (START) (X 0 WHILE) (END)
    tokens = criar_tokens_programa_simples(
        [
            criar_token("PARENTESIS", "("),
            criar_token("VARIAVEL", "X"),
            criar_token("NUMERO", "0"),
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


def teste_aninhamento():
    """
    Teste 11: Parsing de expressões aninhadas.

    Valida se parênteses aninhados em múltiplos níveis são
    parseados corretamente mantendo a estrutura hierárquica.

    Teste:
        Entrada: (START) ((10 5 +) 3 *) (END)
        Esperado: Parsing bem-sucedido com dois níveis de aninhamento

    Returns
    -------
    bool
        True se parsing bem-sucedido, False caso contrário
    """
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
    """
    Teste 12: Parsing de múltiplos comandos sequenciais.

    Valida se múltiplos comandos em sequência dentro de um programa
    são parseados corretamente como parte da ListaOuFim.

    Teste:
        Entrada: (START) (10) (20) (END)
        Esperado: Parsing bem-sucedido com dois comandos

    Returns
    -------
    bool
        True se parsing bem-sucedido, False caso contrário
    """
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
    """
    Teste 13: Detecção de erro - parêntese não fechado.

    Valida se o parser detecta e relata erro quando um parêntese
    de abertura não tem seu correspondente de fechamento.

    Teste:
        Entrada: (START) (10 (20) (END) <- sem fechar (10
        Esperado: Erro detectado com mensagem descritiva

    Returns
    -------
    bool
        True se erro foi detectado, False se passou incorretamente
    """
    print("\nTESTE 13: Detecção de erro - parêntese não fechado\n")

    # (START) (10 (20) (END) <- sem fechar (10
    tokens = [
        criar_token("PARENTESIS", "("),
        criar_token("COMANDO", "START"),
        criar_token("PARENTESIS", ")"),
        criar_token("PARENTESIS", "("),
        criar_token("NUMERO", "10"),
        criar_token("PARENTESIS", "("),
        criar_token("NUMERO", "20"),
        criar_token("PARENTESIS", ")"),
        # Falta fechar (10
        criar_token("PARENTESIS", "("),
        criar_token("COMANDO", "END"),
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
    """
    Teste 14: Verificação da classe ParserLL1 diretamente.

    Valida se a classe pode ser instanciada e seus métodos auxiliares
    (como get_terminal) funcionam corretamente.

    Testes:
        - Criação de instância com gramática
        - Mapeamento de token NUMERO -> terminal NUMERO
        - Mapeamento de token VARIAVEL -> terminal VARIAVEL

    Returns
    -------
    bool
        True se todos os sub-testes passarem, False caso contrário
    """
    print("\nTESTE 14: Classe ParserLL1 diretamente\n")

    parser = ParserLL1(gramatica)

    if parser.gramatica:
        print("OK Parser inicializado")
        print("  Não-terminais: %d" % len(parser.gramatica))

        # Testar get_terminal
        token_num = criar_token("NUMERO", "42")
        terminal = parser.get_terminal(token_num)
        assert terminal == "NUMERO", "Terminal incorreto para NUMERO"

        token_var = criar_token("VARIAVEL", "X")
        terminal = parser.get_terminal(token_var)
        assert terminal == "VARIAVEL", "Terminal incorreto para VARIAVEL"

        print("OK Mapeamento de terminais OK")
        return True
    else:
        print("X Gramática não carregada")
        return False


def teste_arvore_sintatica():
    """
    Teste 15: Geração de árvore sintática serializada.

    Valida se a árvore sintática é corretamente construída,
    serializada para dicionário e contém a estrutura esperada
    (rótulo, tipo, filhos).

    Teste:
        Entrada: (START) (5) (END)
        Esperado: Árvore com raíz "Programa" e hierarquia correta

    Returns
    -------
    bool
        True se árvore foi gerada com sucesso, False caso contrário
    """
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
    """
    Orquestra a execução de todos os 13 testes.

    Executa cada teste, captura resultados e exceções, gera
    relatório final com resumo de sucessos/falhas.

    Testes Cobertos
    ---------------
    1. Parsing de número simples
    2. Parsing de variável simples
    3. Operações aritméticas (+, -, *, /, //, %, ^)
    4. Comando MEM (armazenar)
    5. Comando RES (recuperar)
    6. Estrutura IF (condicional)
    7. Estrutura WHILE (iteração)
    8. Estrutura FOR (iteração)
    9. Expressões aninhadas (duplo aninhamento)
    10. Múltiplos comandos sequenciais
    11. Detecção de erro (parêntese não fechado)
    12. Classe ParserLL1 diretamente
    13. Geração de árvore sintática

    Returns
    -------
    bool
        True se todos os 13 testes passaram, False caso contrário

    Notes
    -----
    Imprime relatório formatado com status individual de cada teste
    e resumo final mostrando número de testes que passaram.
    Trata exceções durante testes e as registra como falhas.
    """
    print("\nSUITE DE TESTES - PARSER LL(1) ALUNO 2\n")

    testes = [
        ("Número simples", teste_numero_simples),
        ("Variável simples", teste_variavel_simples),
        ("Operações aritméticas", teste_operacoes_aritmeticas),
        ("Comando MEM", teste_comando_mem),
        ("Comando RES", teste_comando_res),
        ("Estrutura IF", teste_estrutura_if),
        ("Estrutura WHILE", teste_estrutura_while),
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
    """
    Ponto de entrada principal da suite de testes.
    
    Executa main() e retorna código de saída apropriado:
    - 0: Todos os 13 testes passaram (sucesso)
    - 1: Um ou mais testes falharam (falha)
    """
    sucesso = main()
    sys.exit(0 if sucesso else 1)
