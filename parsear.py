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
