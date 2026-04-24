# Nome | apelido no Github | link do Github
# Andrei de Carvalho Bley | andrei-bley | https://github.com/andrei-bley
# Vinicius Cordeiro Vogt | vinivaldox | https://github.com/vinivaldox
# Vitor Matias Percegona Bilbao | vitormpbilbao | https://github.com/vitormpbilbao

# Grupo: RA2 15
"""
Fase 2 do Compilador: Análise Sintática Descendente
Descrição:
    Implementa um parser LL(1) não-recursivo usando algoritmo de pilha
    para validar tokens contra a gramática fornecida pelo Aluno 1.
"""

from dataclasses import dataclass, field


@dataclass
class NoArvore:
    rotulo: str  # Programa, Comando, Elemento
    tipo: str  # terminal ou nao_terminal
    valor: str | None = None  # Valor para terminais
    # importa construtor de lista vazia para evitar mutabilidade compartilhada (onibus fantasma)
    filhos: list["NoArvore"] = field(default_factory=list)

    # represenacao str de saida
    def __repr__(self) -> str:
        if self.tipo == "terminal":
            return f"NoArvore({self.rotulo}, '{self.valor}')"
        else:
            return f"NoArvore({self.rotulo}, filhos={len(self.filhos)})"


@dataclass
class ErroSintatico:
    numero_comando: int  # Qual comando tem erro
    indice_token: int  # Posição no token do comando
    esperado: str  # O que era esperado
    encontrado: str  # O que foi encontrado
    mensagem: str  # Mensagem descritiva completa

    # represenacao str de saida
    def __repr__(self) -> str:
        return f"ErroSintatico(cmd={self.numero_comando}[{self.indice_token}]: {self.mensagem})"


class ParserLL1:
    def __init__(self):
        # TODO, ESSE METODO É MEIO ESTRANHO, melhor parametrizar isso aqui
        # Verifica import da gramatica ja que não existe um arquivo de gramatica.py nessa branch
        try:
            from gramatica import construirGramatica  # pyright: ignore[reportMissingImports]

            self.gramatica = construirGramatica()
        except ImportError:
            print("Aviso: gramatica.py não encontrado. Usando gramática vazia.")
            self.gramatica = {}

        # Estado do parser
        self.tokens_atuais = []  # Tokens sendo processados
        self.indice_token = 0  # Posição atual no buffer
        self.pilha_analise = []  # Pilha de símbolos para análise
        self.derivacoes = []  # Histórico de derivações (debug)
        self.arvore = None  # Árvore sintática resultante
        self.erros = []  # Lista de erros encontrados
        self.numero_comando = 0  # Qual comando está sendo processado

    def get_terminal(self, token: dict) -> str:
        if not token:
            return "$"

        tipo = token.get("tipo", "")
        valor = token.get("valor", "")

        if tipo == "PARENTESIS":
            return "PARENTESIS_ESQ" if valor == "(" else "PARENTESIS_DIR"
        elif tipo == "NUMERO":
            return "NUMERO"
        elif tipo == "VARIAVEL":
            return "VARIAVEL"
        elif tipo == "OPERADOR":
            return "OPERADOR"
        elif tipo == "COMANDO":
            # Retorna o valor específico: MEM, RES, IF, WHILE, IFELSE
            return valor
        else:
            return "DESCONHECIDO"

    def _is_terminal(self, simbolo: str) -> bool:
        # TODO: Verificar se isso aqui vai mudar deopis que a gramatica e a tokenizacao estiverem implementadas
        terminais = {
            "PARENTESIS_ESQ",
            "PARENTESIS_DIR",
            "NUMERO",
            "VARIAVEL",
            "OPERADOR",
            "START",
            "END",
            "MEM",
            "RES",
            "IF",
            "IFELSE",
            "WHILE",
            "FOR",
            "$",
        }
        return simbolo in terminais

    def _next_token(self) -> dict | None:
        if self.indice_token < len(self.tokens_atuais):
            return self.tokens_atuais[self.indice_token]
        return None

    def _get_next_token(self) -> dict | None:
        token = self._next_token()
        if token:
            self.indice_token += 1
        return token

    def _add_erro(self, esperado: str, encontrado: str):
        erro = ErroSintatico(
            numero_comando=self.numero_comando,
            indice_token=self.indice_token,
            esperado=esperado,
            encontrado=encontrado,
            mensagem=f"Cmd {self.numero_comando}[{self.indice_token}]: "
            f"Esperado '{esperado}', encontrado '{encontrado}'",
        )
        self.erros.append(erro)

    def _add_derivacao(self, derivacao: str):
        self.derivacoes.append(derivacao)

    def _serializar_arvore(self, no: NoArvore | None) -> dict | None:
        # Basicamente um to dict
        if not no:
            return None

        return {
            "rotulo": no.rotulo,
            "tipo": no.tipo,
            "valor": no.valor,
            "filhos": [self._serializar_arvore(filho) for filho in no.filhos],
        }

    def _selecionar_regra(self, terminal: str, regras: list) -> list | None:
        """Seleciona a regra correta baseada em FIRST/FOLLOW."""
        for regra in regras:
            if not regra:
                continue

            primeiro_simbolo = regra[0]

            if self._is_terminal(primeiro_simbolo):
                if primeiro_simbolo == terminal:
                    return regra
            elif primeiro_simbolo == "EPSILON":
                return regra
            else:
                return regra

        return None

    def parsearComando(self, tokens: list[dict], num_comando: int) -> dict:
        # TODO MELHORAR A DOCSTR
        # TODO ATUALIZAR ESSA FUNÇÃO DEPOIS QUE A GRAMÁTICA ESTIVER DEFINIDA, JA QUE ISSO VAI MUDAR MUITO O FLUXO DO PARSER
        """
        Algoritmo LL(1) não-recursivo com pilha.

        Algoritmo:
        1. Inicializar pilha com ['$', 'Programa']
        2. Enquanto pilha não vazia:
           a. Se topo == terminal: combinar com entrada
           b. Se topo == não-terminal: consultar gramática
           c. Se topo == '$': verificar EOF
        """
        self.tokens_atuais = tokens
        self.indice_token = 0
        self.numero_comando = num_comando
        self.pilha_analise = ["$", "Programa"]
        self.derivacoes = []
        self.erros = []
        self.arvore = NoArvore("Programa", "nao_terminal")

        while self.pilha_analise:
            topo = self.pilha_analise[-1]
            token_atual = self._next_token()
            terminal_atual = self.get_terminal(token_atual) if token_atual else "$"

            # Caso 1: Topo é terminal - deve combinar
            if self._is_terminal(topo):
                if topo == terminal_atual:
                    print(f"Combina: {topo}")
                    self._get_next_token()
                    self.pilha_analise.pop()
                else:
                    self._add_erro(esperado=topo, encontrado=terminal_atual)
                    return self._construir_resultado(sucesso=False)

            # Caso 2: Topo é $ (marcador de fim)
            elif topo == "$":
                if terminal_atual == "$":
                    print("Programa reconhecido")
                    self.pilha_analise.pop()
                else:
                    self._add_erro(esperado="EOF", encontrado=terminal_atual)
                    return self._construir_resultado(sucesso=False)

            # Caso 3: Topo é não-terminal - usar gramática
            else:
                regras = self.gramatica.get(topo, [])

                # Encontrar regra correta
                regra_aplicada = self._selecionar_regra(terminal_atual, regras)

                if regra_aplicada is None:
                    self._add_erro(
                        esperado=f"Nao-terminal '{topo}'",
                        encontrado=terminal_atual,
                    )
                    return self._construir_resultado(sucesso=False)

                # Aplicar regra: substituir topo por derivação (inverso)
                self.pilha_analise.pop()
                for simbolo in reversed(regra_aplicada):
                    if simbolo != "EPSILON":
                        self.pilha_analise.append(simbolo)

                self._add_derivacao(f"{topo} → {' '.join(regra_aplicada)}")

        return self._construir_resultado(sucesso=True)


if __name__ == "__main__":
    print("Rodando o PARSER LL(1)")

    print("\nEstruturas de dados:")
    no = NoArvore("Programa", "nao_terminal")
    print(f"   No: {no}")

    erro = ErroSintatico(
        1, 5, "NUMERO", "VARIAVEL", "Esperado NUMERO, encontrado VARIAVEL"
    )
    print(f"   Erro: {erro}")

    print("\nClasse ParserLL1:")
    parser = ParserLL1()
    print(f"   Não-terminais: {list(parser.gramatica.keys())}")
    print(
        f"   Total de regras: {sum(len(regras) for regras in parser.gramatica.values())}"
    )
