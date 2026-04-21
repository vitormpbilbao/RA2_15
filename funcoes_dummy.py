# Nome | apelido no Github | link do Github
# Andrei de Carvalho Bley | TODO: inserir usuario/apelido do github aqui
# Vinicius Cordeiro Vogt | vinivaldox | https://github.com/vinivaldox
# Vitor Matias Percegona Bilbao | TODO: inserir usuario/apelido do github aqui

# Grupo: RA1 15
from dataclasses import dataclass
import random


@dataclass
class Token:
    """Classe que representa um token"""

    tipo: str  # "NUMERO", "OPERADOR", "PARENTESIS", "COMANDO", "VARIAVEL"
    valor: str  # valor real do token


def parseExpressao(linha: str) -> list:
    """DUMMY Aluno 1: Simula tokenização sem implementação real"""
    # Apenas simula alguns tokens genéricos
    tokens_simulados = [
        Token("PARENTESIS", "("),
        Token("NUMERO", "5"),
        Token("NUMERO", "3"),
        Token("OPERADOR", "+"),
        Token("PARENTESIS", ")"),
    ]
    return tokens_simulados


def ler_arquivo(nome_arquivo: str) -> list:
    """Lê arquivo .txt e retorna lista de linhas"""
    if not nome_arquivo.endswith(".txt"):
        raise ValueError("O arquivo deve ter extensão .txt")

    with open(nome_arquivo, "r", encoding="utf-8") as f:
        linhas = [linha.strip() for linha in f.readlines() if linha.strip()]
    return linhas


# ============================================================================
# FUNÇÕES DUMMY - ALUNO 2 E 3
# ============================================================================


def executarExpressao(tokens: list) -> float:
    """DUMMY Aluno 2: Retorna resultado simulado"""
    return round(random.uniform(0, 100), 1)


def gerarAssembly(tokens: list) -> str:
    """DUMMY Aluno 3: Retorna assembly simulado"""
    return "; Assembly ARM simulado (Aluno 3)\n"
