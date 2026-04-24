def lerTokensDict(nomeArquivo):

    import ast  # converter a string em lista de dicionários

    linhas = []
    with open(nomeArquivo, "r") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if linha:
                tokens = ast.literal_eval(linha)  # converte string para lista de dicts
                linhas.append(tokens)

    return linhas


def is_variavel(token):
    """
    Verifica se o token recebido é uma variavel de memória (apenas letras maiusculas), porem a variável de memória não pode ser RES
    Retorna Falso caso não seja verdade
    """
    if token == "RES":
        return False
    else:
        return token.isalpha() and token.isupper()


def is_numero(token):
    """
    Aqui será verificado se o token é um número tentando converter para float, tanto para padronizar quanto para verificar
    ou seja, se tentar transformar uma letra em float, acusará erro e retornará falso
    """
    try:
        float(token)
        return True
    except ValueError:
        return False


# definindo os operadores válidos
operadores = {"+", "-", "*", "/", "//", "%", "^"}
memoria = {}        
historico = []

#####ERRO com o ALUNO 2, o geren memo nao sabe tratar token do tipo KEYWORD
def executarExpressao(tokens):  # , memoria, historico):
    """
    Monta uma árvore de operações a partir dos tokens do Aluno 1

    """
    pilha = []

    for token in tokens:
        tipo = token["tipo"]
        valor = token["valor"]

        # Parêntese de abertura — empilha como marcador do início
        if tipo == "PARENTESIS" and valor == "(":
            pilha.append("(")

        # Número — empilha como float
        elif tipo == "NUMERO":
            try:
                pilha.append(float(valor))
            except ValueError:
                print(f"ERRO: Número inválido: '{valor}'")
                return None

        # Operador
        elif tipo == "OPERADOR":
            pilha.append(valor)

        # Variável de memória — empilha o nome
        elif tipo == "VARIAVEL":
            pilha.append(valor)

        elif tipo == "COMANDO":
            pilha.append(valor)

        # parêntese de fechamento
        elif tipo == "PARENTESIS" and valor == ")":
            elementos = []

            # Desempilha tudo até encontrar o "("
            while pilha and pilha[-1] != "(":
                elementos.append(pilha.pop())

            if not pilha:
                print("ERRO: parênteses desbalanceados")
                return None

            pilha.pop()  # remove o "("
            elementos.reverse()  # corrige a ordem

            ################# montar os nós para adicionar na pilha com base na regra de formatação###################

            # get_mem é para ler algo na memória
            if len(elementos) == 1 and is_variavel(str(elementos[0])):
                no = {"tipo": "mem_get", "variavel": elementos[0]}

            # buscar algo no histórico
            elif len(elementos) == 2 and elementos[1] == "RES":
                no = {"tipo": "res_get", "indice": elementos[0]}

            # mem_set é quando define um valor na memoria
            elif len(elementos) == 3 and elementos[2] == "MEM":
                no = {
                    "tipo": "mem_set",
                    "valor": elementos[0],
                    "variavel": elementos[1],
                }
            # caso normal a b +
            elif len(elementos) == 3 and elementos[2] in operadores:
                no = {
                    "tipo": "operacao",
                    "op1": elementos[0],
                    "op2": elementos[1],
                    "op": elementos[2],
                }

            else:
                print("ERRO: = inválido:", elementos)
                return None

            pilha.append(no)  # empilha o nó montado

    if len(pilha) != 1:
        print("ERRO: expressão mal formada")
        return None

    return pilha[0]


def validarToken(arvore, numero_token, memoria, historico):
    """
    Interpreta a árvore gerada pelo executarExpressao e reporta o resultado da validação.
    Parametros baseados na árvore gerada, o numero do token para acessar a RES, memoria para saber o que está definido e histórico para registrar tokens processados
    retorna um valorr booleano junto com a mensagem descritiva da validação
    """

    if arvore is None:
        return False, f"Token {numero_token}: inválido"

    if arvore["tipo"] == "mem_set":  # marca a variavel como definida no dic da memoria
        memoria[arvore["variavel"]] = True
        return True, f"Token {numero_token}: memória {arvore['variavel']} definida"

    elif arvore["tipo"] == "mem_get":  # verifica se foi definida
        if arvore["variavel"] not in memoria:
            return False, f"Token {numero_token}: inválido"
        return True, f"Token {numero_token}: leitura da memória {arvore['variavel']}"

    elif arvore["tipo"] == "res_get":  # verifica se existem n resultados anteriores
        n = int(arvore["indice"])
        if n > len(historico):
            return False, f"Token {numero_token}: inválido"
        return (
            True,
            f"Token {numero_token}: referência ao resultado de {n} tokens atrás",
        )

    elif arvore["tipo"] == "operacao":
        return True, f"Token {numero_token}: válido"

    else:
        return False, f"Token {numero_token}: inválido"


if __name__ == "__main__":
    linhas = lerTokensDict("token.txt")
    for i, tokens in enumerate(linhas):
        arvore = executarExpressao(tokens)  # , memoria, historico)
        valido, mensagem = validarToken(arvore, i + 1, memoria, historico)
        print(mensagem)
        if valido:
            historico.append(arvore)
