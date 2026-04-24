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

    def serializar(self):
        """Converte nó para dicionário (JSON-compatível)."""
        return {
            "rotulo": self.rotulo,
            "tipo": self.tipo,
            "valor": self.valor,
            "filhos": [filho.serializar() for filho in self.filhos],
        }


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
    def __init__(self, gramatica):
        self.gramatica = gramatica
        # Variáveis padronizadas para evitar AttributeError
        self.tokens = []
        self.posicao = 0
        self.derivacoes = []
        self.erros = []
        self.numero_comando = 0

    def get_terminal(self, token: dict) -> str:
        if not token:
            return "$"
        tipo = token.get("tipo", "")
        valor = str(token.get("valor", "")).upper()

        if tipo == "PARENTESIS":
            return "PARENTESIS_ESQ" if valor == "(" else "PARENTESIS_DIR"
        elif tipo == "NUMERO":
            return "NUMERO"
        elif tipo == "VARIAVEL":
            return "VARIAVEL"
        elif tipo == "OPERADOR":
            return "OPERADOR"
        elif tipo in ["COMANDO", "KEYWORD"]:
            # Mapeia START, END, MEM, RES, IF, WHILE
            return valor
        else:
            return "DESCONHECIDO"

    def _next_token(self) -> dict | None:
        if self.indice_token < len(self.tokens_atuais):
            return self.tokens_atuais[self.indice_token]
        return None

    def _get_next_token(self) -> dict | None:
        token = self._next_token()
        if token:
            self.indice_token += 1
        return token

    def _add_erro(self, esperado: str, encontrado: str, contexto: str):
        erro = ErroSintatico(
            numero_comando=self.numero_comando,
            indice_token=self.indice_token,
            esperado=esperado,
            encontrado=encontrado,
            mensagem=f"Cmd {self.numero_comando}[{self.indice_token}]: "
            f"Esperado '{esperado}', encontrado '{encontrado}' ({contexto})",
        )
        self.erros.append(erro)

    def _combinar_terminal(self, esperado, contexto, no):
        """Combina um terminal esperado com o próximo token."""
        token = self._next_token()
        terminal = self.get_terminal(token)

        if terminal == esperado:
            self._get_next_token()
            no_terminal = NoArvore(esperado, "terminal", valor=token.get("valor", ""))
            no.filhos.append(no_terminal)
            return True
        else:
            self._add_erro(esperado, terminal, contexto)
            return False

    def _add_derivacao(self, derivacao: str):
        self.derivacoes.append(derivacao)

    def parser_programa(self):
        no = NoArvore("Programa", "nao_terminal")
        if not self._combinar_terminal("PARENTESIS_ESQ", "início", no):
            return None
        if not self._combinar_terminal("START", "palavra START", no):
            return None
        if not self._combinar_terminal("PARENTESIS_DIR", "fim START", no):
            return None

        lista_no = self.parser_lista_ou_fim()
        if lista_no:
            no.filhos.append(lista_no)
        return no

    def parser_lista_ou_fim(self):
        no = NoArvore("ListaOuFim", "nao_terminal")
        if not self._combinar_terminal("PARENTESIS_ESQ", "início de bloco", no):
            return None

        conteudo_no = self.parser_conteudo_ou_fim()
        if conteudo_no:
            no.filhos.append(conteudo_no)
        return no

    def parser_conteudo_ou_fim(self):
        no = NoArvore("ConteudoOuFim", "nao_terminal")
        token = self._next_token()
        terminal = self.get_terminal(token)

        if terminal == "END":
            self._combinar_terminal("END", "palavra END", no)
            self._combinar_terminal("PARENTESIS_DIR", "fim END", no)
            self._add_derivacao("ConteudoOuFim -> END )")
        else:
            conteudo_no = self.parser_conteudo()
            if conteudo_no:
                no.filhos.append(conteudo_no)
            self._combinar_terminal("PARENTESIS_DIR", "fim de comando", no)

            lista_no = self.parser_lista_ou_fim()
            if lista_no:
                no.filhos.append(lista_no)
            self._add_derivacao("ConteudoOuFim -> Conteudo ) ListaOuFim")
        return no

    def parser_comando(self):
        no = NoArvore("Comando", "nao_terminal")
        if not self._combinar_terminal("PARENTESIS_ESQ", "início comando", no):
            return None
        conteudo_no = self.parser_conteudo()
        if conteudo_no:
            no.filhos.append(conteudo_no)
        if not self._combinar_terminal("PARENTESIS_DIR", "fim comando", no):
            return None
        return no

    def parser_conteudo(self):
        no = NoArvore("Conteudo", "nao_terminal")
        elem_no = self.parser_elemento()
        if elem_no:
            no.filhos.append(elem_no)
        resto_no = self.parser_resto_conteudo()
        if resto_no:
            no.filhos.append(resto_no)
        return no

    def parser_resto_conteudo(self):
        no = NoArvore("RestoConteudo", "nao_terminal")
        token = self._next_token()
        terminal = self.get_terminal(token)

        if terminal == "RES":
            self._combinar_terminal("RES", "comando RES", no)
        elif terminal in ["NUMERO", "VARIAVEL", "PARENTESIS_ESQ"]:
            elem_no = self.parser_elemento()
            if elem_no:
                no.filhos.append(elem_no)
            cauda_no = self.parser_cauda()
            if cauda_no:
                no.filhos.append(cauda_no)
        return no  # Se não entrar nos ifs, é EPSILON

    def parser_cauda(self):
        no = NoArvore("Cauda", "nao_terminal")
        token = self._next_token()
        terminal = self.get_terminal(token)
        if terminal in ["OPERADOR", "MEM", "IF", "WHILE"]:
            self._combinar_terminal(terminal, "ação", no)
        return no

    def parser_elemento(self):
        no = NoArvore("Elemento", "nao_terminal")
        token = self._next_token()
        terminal = self.get_terminal(token)

        if terminal == "NUMERO":
            self._combinar_terminal("NUMERO", "valor", no)
        elif terminal == "VARIAVEL":
            self._combinar_terminal("VARIAVEL", "id", no)
        elif terminal == "PARENTESIS_ESQ":
            cmd_no = self.parser_comando()
            if cmd_no:
                no.filhos.append(cmd_no)
        return no

    def parser_comando_completo(self, tokens, num_comando):
        self.tokens = tokens
        self.posicao = 0
        self.numero_comando = num_comando
        self.erros = []
        arvore = self.parser_programa()
        return {
            "numero_comando": num_comando,
            "sucesso": arvore is not None and len(self.erros) == 0,
            "arvore": arvore.serializar() if arvore else None,
            "erros": [vars(e) for e in self.erros],
        }


def parsear(tokens_planificados: list[dict], gramatica: dict) -> dict:
    """Processa o programa completo conforme a tua gramática."""
    parser = ParserLL1(gramatica)
    # passamos todos os tokens de uma vez porque o programa
    # engloba o START, Lista de Comandos e o END.
    resultado = parser.parser_comando_completo(tokens_planificados, 1)

    return {
        "sucesso": resultado["sucesso"],
        "resultados": [resultado],
        "resumo": "Processamento do programa completo",
    }
