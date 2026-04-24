# Nome | apelido no Github | link do Github
# Andrei de Carvalho Bley | andrei-bley | https://github.com/andrei-bley
# Vinicius Cordeiro Vogt | vinivaldox | https://github.com/vinivaldox
# Vitor Matias Percegona Bilbao | vitormpbilbao | https://github.com/vitormpbilbao

# Grupo: RA1 15
from dataclasses import dataclass

COMANDOS = {"MEM", "RES"}
KEYWORDS = {"START", "END", "IF", "IFELSE", "WHILE", "FOR"}

@dataclass
class Token:
    """Representa um token reconhecido pelo analisador léxico.

    Um token é a unidade mínima de significado sintático em uma expressão RPN.
    Cada token possui um tipo (NUMERO, OPERADOR, etc.) e um valor específico.

    Attributes
    ----------
    tipo : str
        Tipo do token. Valores possíveis: 'NUMERO', 'OPERADOR', 'PARENTESIS',
        'COMANDO', 'VARIAVEL', 'KEYWORD'
    valor : str
        Valor literal do token. Exemplos: '3', '+', '(', 'MEM', 'A'

    Examples
    --------
    >>> token = Token('NUMERO', '42')
    >>> token.tipo
    'NUMERO'
    >>> token.valor
    '42'
    >>> token.to_dict()
    {'tipo': 'NUMERO', 'valor': '42'}
    """

    tipo: str  # "NUMERO", "OPERADOR", "PARENTESIS", "COMANDO", "VARIAVEL", "KEYWORD"
    valor: str  # O valor real do token. Exemplo, "3", "+", "(", "MEM"

    def to_dict(self) -> dict:
        """Converte o Token para formato dicionário.

        Transforma o objeto Token em um dicionário Python com as mesmas
        informações, útil para serialização ou passagem a outros módulos.

        Returns
        -------
        dict
            Dicionário com chaves 'tipo' e 'valor'

        Examples
        --------
        >>> token = Token('NUMERO', '3.14')
        >>> token.to_dict()
        {'tipo': 'NUMERO', 'valor': '3.14'}
        """
        return {"tipo": self.tipo, "valor": self.valor}


def estado_inicial(caractere: str, contexto: dict) -> str:
    """Estado inicial do DFA - reconhece primeiro caractere de cada token.

    Processa parênteses, espaços, dígitos, letras e operadores simples.
    Para operadores compostos (- e /), transiciona para estados de validação.

    Parameters
    ----------
    caractere : str
        Um caractere individual da entrada
    contexto : dict
        Dicionário com chaves: 'buffer' (acumulador), 'tokens' (lista de tokens gerados)

    Returns
    -------
    str
        Nome do próximo estado como string ('inicial', 'numero', 'letra', etc.)

    Raises
    ------
    ValueError
        Se o caractere é inválido (não reconhecido pelo DFA)
    """

    # paretneses, tem retorno imediato
    if caractere == "(":
        contexto["tokens"].append(Token("PARENTESIS", "("))
        return "inicial"
    elif caractere == ")":
        contexto["tokens"].append(Token("PARENTESIS", ")"))
        return "inicial"

    # ignora espaços e tabs
    elif caractere in " \t":
        return "inicial"

    # digitos de um numero
    elif caractere.isdigit():
        contexto["buffer"] = caractere
        return "numero"

    # letras para um comando ou variavel
    elif caractere.isalpha():
        contexto["buffer"] = caractere
        return "letra"

    # operadores simples, tem retorno imediato
    elif caractere == "+":
        contexto["tokens"].append(Token("OPERADOR", "+"))
        return "inicial"
    elif caractere == "*":
        contexto["tokens"].append(Token("OPERADOR", "*"))
        return "inicial"
    elif caractere == "%":
        contexto["tokens"].append(Token("OPERADOR", "%"))
        return "inicial"
    elif caractere == "^":
        contexto["tokens"].append(Token("OPERADOR", "^"))
        return "inicial"

    # TODO: Ver se tem numero negativo nessa atividade
    # verificar se o "-" é um operador de subtração ou um sinal de número negativo
    elif caractere == "-":
        contexto["buffer"] = "-"
        return "valida_menos"

    # operador complexo, podendo ser "/" ou "//", então precisa de um estado de validação
    elif caractere == "/":
        contexto["buffer"] = "/"
        return "valida_divisao"
    
    #FASE 2 ADAPTAÇÃO PARA KEYWORDS ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    elif caractere == ">":
        contexto["buffer"] = ">"
        return "valida_maior"
    elif caractere == "<":
        contexto["buffer"] = "<"
        return "valida_menor"
    elif caractere == "=":
        contexto["buffer"] = "="
        return "valida_igual"
    elif caractere == "!":
        contexto["buffer"] = "!"
        return "valida_diferente"
    elif caractere == "|":
        contexto["tokens"].append(Token("OPERADOR", "|"))
        return "inicial"
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # entrada invalida
    else:
        msg = f"Caractere inválido: '{caractere}'"
        raise ValueError(msg)


def estado_numero(caractere: str, contexto: dict) -> str:
    """Estado de acumulação de número - reconhece dígitos e decimais.

    Acumula caracteres no buffer enquanto forem dígitos. Permite um único ponto
    decimal. Termina quando encontra espaço, parêntese, operador ou fim de linha.

    Parameters
    ----------
    caractere : str
        Um caractere individual da entrada
    contexto : dict
        Dicionário com chaves: 'buffer' (número em construção), 'tokens' (tokens finalizados)

    Returns
    -------
    str
        Nome do próximo estado

    Raises
    ------
    ValueError
        Se há dois pontos decimais no número ou caractere inválido
    """
    if caractere.isdigit():
        contexto["buffer"] += caractere
        return "numero"

    # encontrou ponto decimal - valida se já tem um ponto
    elif caractere == ".":
        if "." in contexto["buffer"]:
            msg = f"Número malformado: dois pontos - '{contexto['buffer']}'"
            raise ValueError(msg)
        contexto["buffer"] += caractere
        return "numero"

    # espaço - termina o número
    elif caractere in " \t":
        contexto["tokens"].append(Token("NUMERO", contexto["buffer"]))
        contexto["buffer"] = ""
        return "inicial"

    # parêntese - termina número e processa parêntese
    elif caractere in "()":
        contexto["tokens"].append(Token("NUMERO", contexto["buffer"]))
        contexto["buffer"] = ""
        return "inicial"

    # operador - termina número e processa operador
    elif caractere in "+*/%^|":
        contexto["tokens"].append(Token("NUMERO", contexto["buffer"]))
        contexto["buffer"] = ""
        return "inicial"

    elif caractere == "-":
        contexto["tokens"].append(Token("NUMERO", contexto["buffer"]))
        contexto["buffer"] = ""
        return "valida_menos"

    # "/" - precisa validar se é "/" ou "//"
    elif caractere == "/":
        contexto["tokens"].append(Token("NUMERO", contexto["buffer"]))
        contexto["buffer"] = "/"
        return "valida_divisao"
    
    #Fase 2++++++++++++++++++++++++++++++++++++++++++++++++ operadores relacionais, ex:terminadores de npumero
    elif caractere in "><!=":
        contexto["tokens"].append(Token("NUMERO", contexto["buffer"]))
        contexto["buffer"] = ""
        return estado_inicial(caractere, contexto)

    # inválido
    else:
        msg = f"Caractere inválido em número: '{contexto['buffer']}{caractere}'"
        raise ValueError(msg)


def estado_valida_menos(caractere: str, contexto: dict) -> str:
    """Estado de validação do operator/sinal '-' em RPN.

    Distingue se '-' é operador de subtração ou sinal de número negativo:
    - Se seguido de dígito: número negativo (ex: -5)
    - Se seguido de espaço/parêntese: operador de subtração

    Nota: Em RPN, operadores vêm sempre após operandos. Se houver "-5", é número negativo.

    Parameters
    ----------
    caractere : str
        Próximo caractere após o '-'
    contexto : dict
        Dicionário com chaves: 'buffer' ('-'), 'tokens' (tokens finalizados)

    Returns
    -------
    str
        'numero' para número negativo, 'inicial' para operador

    Raises
    ------
    ValueError
        Se caractere após '-' é inválido
    """
    if caractere.isdigit():
        contexto["buffer"] += caractere  # "-" + dígito
        return "numero"

    elif caractere in " \t":
        contexto["tokens"].append(Token("OPERADOR", "-"))
        contexto["buffer"] = ""
        return "inicial"  # Volta e ignora o espaço

    # "-" SEGUIDO de parêntese = é operador
    elif caractere in "()":
        contexto["tokens"].append(Token("OPERADOR", "-"))
        contexto["buffer"] = "-"
        return "inicial"

    # TODO: inserir validação de ponto aqui para numeros como -.8 ??
    else:
        msg = f"Caractere inválido após '-': '{caractere}'"
        raise ValueError(msg)


def estado_valida_divisao(caractere: str, contexto: dict) -> str:
    """Estado de validação do operador '/' vs '//' em RPN.

    Distingue divisão simples (/) de divisão inteira (//):
    - Se seguido de '/': operador // (divisão inteira)
    - Se seguido de outro caractere: operador / (divisão real)

    Parameters
    ----------
    caractere : str
        Próximo caractere após o '/'
    contexto : dict
        Dicionário com chaves: 'buffer' ('/'), 'tokens' (tokens finalizados)

    Returns
    -------
    str
        'inicial' após emitir operador
    """
    if caractere == "/":
        contexto["tokens"].append(Token("OPERADOR", "//"))
        contexto["buffer"] = ""
        return "inicial"
    
    else:
        contexto["tokens"].append(Token("OPERADOR", "/"))
        contexto["buffer"] = ""
        return estado_inicial(caractere, contexto)


def estado_letra(caractere: str, contexto: dict) -> str:
    """Estado de acumulação de comando/variável - reconhece sequências de letras.

    Acumula caracteres alfabéticos no buffer. Termina quando encontra espaço,
    parêntese, operador ou fim de línea. Pode transicionar para validação de
    '-' ou '/' para reprocessamento.

    Parameters
    ----------
    caractere : str
        Um caractere individual da entrada
    contexto : dict
        Dicionário com chaves: 'buffer' (letras acumuladas), 'tokens' (tokens finalizados)

    Returns
    -------
    str
        Nome do próximo estado

    Raises
    ------
    ValueError
        Se caractere após sequência de letras é inválido
    """
    if caractere.isalpha():
        contexto["buffer"] += caractere
        return "letra"

    elif caractere in " \t":
        _criar_token_comando_ou_variavel(contexto)
        return "inicial"

    elif caractere in "()+-*/%^|":
        _criar_token_comando_ou_variavel(contexto)
        return estado_inicial(caractere, contexto)

    # "/" precisa validar se é "//"
    elif caractere == "/":
        _criar_token_comando_ou_variavel(contexto)
        contexto["buffer"] = "/"
        return "valida_divisao"

    # "-" precisa validar se é número negativo ou operador
    elif caractere == "-":
        _criar_token_comando_ou_variavel(contexto)
        contexto["buffer"] = ""
        return "valida_menos"
    # Fase 2:operadores relacinais como terminadores de palavra+++++++++++++++++++++++++++++++
    elif caractere in "><!=":
        _criar_token_comando_ou_variavel(contexto)
        return estado_inicial(caractere, contexto)
    
    else:
        msg = f"Caractere inválido em comando: '{contexto['buffer']}{caractere}'"
        raise ValueError(msg)


#Fase 2: novos estados

def estado_valida_maior(caractere: str, contexto: dict) -> str:
    """Estado de validação do '>': pode ser '>' ou '>='.

    '>'  → maior que
    '>=' → maior ou igual

    Parameters
    ----------
    caractere : str
        Caractere após o '>'
    contexto : dict
        Dicionário com 'buffer' e 'tokens'

    Returns
    -------
    str
        Próximo estado
    """
    if caractere == "=":
        contexto["tokens"].append(Token("OPERADOR", ">="))
        contexto["buffer"] = ""
        return "inicial"
    else:
        # '>' simples: emite e reprocessa o caractere atual
        contexto["tokens"].append(Token("OPERADOR", ">"))
        contexto["buffer"] = ""
        return estado_inicial(caractere, contexto)


def estado_valida_menor(caractere: str, contexto: dict) -> str:
    """Estado de validação do '<': pode ser '<' ou '<='.

    '<'  → menor que
    '<=' → menor ou igual

    Parameters
    ----------
    caractere : str
        Caractere após o '<'
    contexto : dict
        Dicionário com 'buffer' e 'tokens'

    Returns
    -------
    str
        Próximo estado
    """
    if caractere == "=":
        contexto["tokens"].append(Token("OPERADOR", "<="))
        contexto["buffer"] = ""
        return "inicial"
    else:
        contexto["tokens"].append(Token("OPERADOR", "<"))
        contexto["buffer"] = ""
        return estado_inicial(caractere, contexto)

def estado_valida_igual(caractere: str, contexto: dict) -> str:
    """Estado de validação do '=': deve formar '=='.

    A linguagem não tem atribuição com '=' — isso é feito via MEM.
    Portanto '=' isolado é sempre erro léxico.

    Parameters
    ----------
    caractere : str
        Caractere após o primeiro '='
    contexto : dict
        Dicionário com 'buffer' e 'tokens'

    Returns
    -------
    str
        Próximo estado

    Raises
    ------
    ValueError
        Se '=' não for seguido de outro '='
    """
    if caractere == "=":
        contexto["tokens"].append(Token("OPERADOR", "=="))
        contexto["buffer"] = ""
        return "inicial"
    else:
        raise ValueError(
            "Erro léxico: '=' isolado não é válido. Use '==' para comparação."
        )


def estado_valida_diferente(caractere: str, contexto: dict) -> str:
    """Estado de validação do '!': deve formar '!='.

    '!' sozinho não tem uso na linguagem.

    Parameters
    ----------
    caractere : str
        Caractere após o '!'
    contexto : dict
        Dicionário com 'buffer' e 'tokens'

    Returns
    -------
    str
        Próximo estado

    Raises
    ------
    ValueError
        Se '!' não for seguido de '='
    """
    if caractere == "=":
        contexto["tokens"].append(Token("OPERADOR", "!="))
        contexto["buffer"] = ""
        return "inicial"
    else:
        raise ValueError(
            f"Erro léxico: '!' deve ser seguido de '=' para '!='. "
            f"Encontrado: '!{caractere}'"
        )






def _criar_token_comando_ou_variavel(contexto: dict):
    """Emite token de COMANDO ou VARIÁVEL conforme o buffer.

    Verifica se o conteúdo do buffer é um comando conhecido (MEM, RES)
    ou uma variável genérica. Limpa o buffer após emissão.

    Parameters
    ----------
    contexto : dict
        Dicionário com chaves: 'buffer' (nome em construção), 'tokens' (lista de tokens)

    Returns
    -------
    None
        Modifica o contexto adicionando token e limpando buffer
    """
    if not contexto["buffer"]:
        return

#Fase 2: adaptação para reconhecer keywords ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    palavra = contexto["buffer"].upper()

    if palavra in COMANDOS:
        contexto["tokens"].append(Token("COMANDO", palavra))
    elif palavra in KEYWORDS:
        contexto["tokens"].append(Token("KEYWORD", palavra))
    else:
        contexto["tokens"].append(Token("VARIAVEL", palavra))

    contexto["buffer"] = ""


def parseExpressao(linha: str) -> list:
    """Processa uma linha completa através do DFA (Autômato Finito Determinístico).

    Orquestrador principal que itembra cada caractere da entrada, mantendo estado
    atual e contexto, até tokenizar completamente a linha de expressão RPN.
    Emite qualquer token pendente no buffer ao final.

    Parameters
    ----------
    linha : str
        Uma linha de expressão RPN a ser tokenizada

    Returns
    -------
    list
        Lista de objetos Token reconhecidos na expressão

    Examples
    --------
    >>> tokens = parseExpressao("( 5 A MEM )")
    >>> len(tokens)
    5
    >>> tokens[0].tipo
    'PARENTESIS'
    """
    contexto = {"buffer": "", "tokens": []}
    estado_atual = "inicial"

    # Mapeia nome do estado para sua função
    estados = {
        "inicial": estado_inicial,
        "numero": estado_numero,
        "letra": estado_letra,
        "valida_menos": estado_valida_menos,
        "valida_divisao": estado_valida_divisao,
        "valida_maior": estado_valida_maior,          # fase 2: operador relacional '>'
        "valida_menor": estado_valida_menor,          # fase 2: operador relacional '<'
        "valida_igual": estado_valida_igual,          # Fase 2: operador relacional '=='
        "valida_diferente": estado_valida_diferente,  # ase 2: operador relacional '!='
    }

    # Processa cada caractere da linha
    for caractere in linha:
        # Pega a função do estado atual
        funcao_estado = estados[estado_atual]
        # Chama a função e recebe o próximo estado (como string)
        estado_atual = funcao_estado(caractere, contexto)

    # Ao final da linha, emite token pendente no buffer (se houver)
    if contexto["buffer"]:
        # Verifica se é número ou comando/variável
        if contexto["buffer"][0].isdigit() or (
            contexto["buffer"][0] == "-" and len(contexto["buffer"]) > 1
        ):
            contexto["tokens"].append(Token("NUMERO", contexto["buffer"]))
        else:
            _criar_token_comando_ou_variavel(contexto)

    return contexto["tokens"]


def ler_teste(nome_arquivo: str) -> list:
    """Abre arquivo .txt e retorna lista de linhas não-vazias.

    Lê todas as linhas de um arquivo de texto, remove espaços em branco
    das pontas e filtra linhas vazias.

    Parameters
    ----------
    nome_arquivo : str
        Nome do arquivo a ser lido. Deve ter extensão .txt

    Returns
    -------
    list
        Lista de strings representando as linhas do arquivo, sem espaços das pontas

    Raises
    ------
    ValueError
        Se o arquivo não possui extensão .txt
    FileNotFoundError
        Se o arquivo não existe

    Examples
    --------
    >>> linhas = ler_arquivo('teste_1.txt')
    >>> len(linhas)
    10
    >>> linhas[0]
    '( 5 A MEM )'
    """

    if not nome_arquivo.endswith(".txt"):
        msg = f"O nome do arquivo '{nome_arquivo}' é inválido. O nome do arquivo deve conter a extensão .txt"
        raise ValueError(msg)

    with open(nome_arquivo, "r", encoding="utf-8") as f:
        linhas = [linha.strip() for linha in f.readlines() if linha.strip()]
    return linhas





#Fase  2 adaptação para interface com o parser (Aluno 3) ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def lerTokens(arquivo: str) -> list:
    """Lê o arquivo fonte e retorna lista de listas de tokens.

    Abre o arquivo .txt linha a linha, descarta linhas vazias e comentários
    (linhas começando com '#'), e tokeniza cada instrução usando o DFA
    estendido. Cada sublista corresponde a uma instrução do programa.

    Esta é a função de interface do Aluno 3 com o Aluno 2 (parsear).

    Parameters
    ----------
    arquivo : str
        Caminho para o arquivo de código-fonte (.txt)

    Returns
    -------
    list
        Lista de listas de dicionários:
        [
          [{'tipo': 'KEYWORD',    'valor': 'START'}, ...],
          [{'tipo': 'PARENTESIS', 'valor': '('}, ...],
          ...
          [{'tipo': 'KEYWORD',    'valor': 'END'}, ...],
        ]

    Raises
    ------
    ValueError
        Se o arquivo não tiver extensão .txt
    FileNotFoundError
        Se o arquivo não existir

    Examples
    --------
    >>> tokens = lerTokens('teste_fase2_1.txt')
    >>> tokens[0]
    [{'tipo': 'PARENTESIS', 'valor': '('}, {'tipo': 'KEYWORD', 'valor': 'START'}, ...]
    """
    if not arquivo.endswith(".txt"):
        raise ValueError(
            f"Arquivo inválido: '{arquivo}'. O arquivo deve ter extensão .txt"
        )

    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            linhas_brutas = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: '{arquivo}'")

    resultado = []
    erros = []

    for numero_linha, linha_bruta in enumerate(linhas_brutas, start=1):
        linha = linha_bruta.strip()

        # ignora linhas vazias e comentários
        if not linha or linha.startswith("#"):
            continue

        try:
            tokens_obj = parseExpressao(linha)
            tokens_dicts = [t.to_dict() for t in tokens_obj]
            if tokens_dicts:
                resultado.append(tokens_dicts)
        except ValueError as erro:
            erros.append(str(erro))
            print(f"  [ERRO LÉXICO] Linha {numero_linha}: {erro}")

    if erros:
        print(f"\n  Total de erros léxicos: {len(erros)}")

    return resultado


if __name__ == "__main__":
    # Testa operadores relacionais novos da Fase 2
    print("++ Operadores Relacionais ++")
    for linha in ["( A B > )", "( A B >= )", "( A B < )", "( A B <= )", "( A B == )", "( A B != )"]:
        tokens = [t.to_dict() for t in parseExpressao(linha)]
        print(f"  {linha} → {tokens}")

    # Testa keywords de controle
    print("\n++ Keywords de Controle ++")
    for linha in ["(START)", "(END)", "( A B > ) IF", "( A B > ) IFELSE", "( A B < ) WHILE"]:
        tokens = [t.to_dict() for t in parseExpressao(linha)]
        print(f"  {linha} → {tokens}")

    # Testa erros léxicos
    print("\n++ Erros Léxicos ++")
    for linha in ["( A @ B + )", "( A = B )", "( A ! B )", "( 3..14 + )"]:
        try:
            parseExpressao(linha)
            print(f"  [FALHOU] '{linha}' deveria gerar erro")
        except ValueError as e:
            print(f"  [OK] '{linha}' → {e}")

    # Testa lerTokens com os arquivos
    print("\n++lerTokens com arquivos ++")
    for nome in ["teste_fase2_1.txt", "teste_fase2_2.txt", "teste_fase2_3.txt"]:
        try:
            lista = lerTokens(nome)
            print(f"  {nome}: {len(lista)} instruções tokenizadas")
        except FileNotFoundError:
            print(f"  {nome}: arquivo não encontrado")
