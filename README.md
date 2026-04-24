# RA1_15 - Compilador RPN → ARMv7 Assembly

## Informações do Projeto

- **Matéria**: Linguagens Formais e Compiladores
- **Professor**: FRANK COELHO DE ALCANTARA
- **Faculdade**: PUCPR (Pontifícia Universidade Católica do Paraná)
- **Grupo**: RA1_15 / RA2_15

## Descrição

Implementação de um compilador de 4 fases que processa expressões em notação RPN (Reverse Polish Notation) e gera código Assembly ARMv7 para a arquitetura Cpulator ARMv7 DEC1-SOC v16.1.

## Fases do Compilador

### ✅ Fase 1: Análise Léxica (Aluno 3 - analisador_lexico.py)
- Tokenização de entrada RPN
- Identificação de tokens válidos
- Saída: `token.txt`

### 🟡 Fase 2: Análise Sintática (Aluno 2 - parsear.py)
- Parser LL(1) não-recursivo
- Validação contra gramática
- Construção de árvore sintática
- Status: ✅ Implementado

### ⏳ Fase 3: Análise Semântica (Aluno 2 - funcoes_dummy.py)
- Gerenciamento de símbolos
- Validação semântica
- Status: 🔄 Em desenvolvimento

### ⏳ Fase 4: Geração de Código (Aluno 4 - gerarAssembly.py)
- Geração de Assembly ARMv7
- Saída: `saida.s`
- Status: 🔄 Em desenvolvimento

## Características

- **Operadores aritméticos**: `+`, `-`, `*`, `/`, `//` (div. inteira), `%` (módulo), `^` (potência)
- **Comandos**: `MEM` (salvar), `RES` (recuperar), `IF` (condicional), `WHILE` (loop), `IFELSE` (condicional alternativo)
- **Números**: Ponto flutuante (IEEE 754 64-bit)

## Como Executar

```bash
python main.py <arquivo_teste.txt>
```

## Estrutura de Arquivos

### Fase 1 (Análise Léxica)
- `analisador_lexico.py`: Tokenização (Aluno 3)
- `lerArquivo.py`: Leitura de tokens (Aluno 3)

### Fase 2 (Análise Sintática)
- `parsear.py`: **Parser LL(1) - Novo! (Aluno 2)**
- `test_parsear.py`: **Testes de integração (Aluno 2)**
- `gramatica.py`: Definição de gramática (Aluno 1 - na branch aluno-1)

### Fase 3-4 (Semântica e Código)
- `geren_memo.py`: Gerenciador de memória
- `gerarAssembly.py`: Gerador de Assembly
- `main.py`: Orquestrador

### Testes
- `teste_1.txt`, `teste_2.txt`, `teste_3.txt`: Fase 1
- `teste1fase2.txt`, `teste2fase2.txt`, `teste3fase2.txt`: Fase 2
- `token.txt`: Saída de tokens da Fase 1

---

## 🎯 Fase 2: Parser LL(1) - Documentação Detalhada

### Overview

O **Parser LL(1)** implementa análise sintática descendente não-recursiva usando algoritmo de pilha:

- **Entrada**: Tokens do Aluno 3 (`lerTokenStr()`)
- **Processamento**: Validação contra gramática LL(1) do Aluno 1
- **Saída**: Árvore sintática + derivações + erros (para Aluno 4)

### Componentes Principais

#### 1. Estruturas de Dados

```python
@dataclass
class NoArvore:
    rotulo: str                    # "Programa", "Comando", etc.
    tipo: str                      # "terminal" ou "nao_terminal"
    valor: str | None = None       # Valor para terminais
    filhos: list[NoArvore] = []   # Filhos na árvore

@dataclass
class ErroSintatico:
    numero_comando: int            # Qual comando (1-indexed)
    indice_token: int              # Posição no comando
    esperado: str                  # Esperado
    encontrado: str                # Encontrado
    mensagem: str                  # Descrição
```

#### 2. Classe ParserLL1

Implementa o algoritmo LL(1) com pilha:

```python
class ParserLL1:
    def parsearComando(tokens, num_comando) -> dict
    def _selecionar_regra(nao_terminal, terminal, regras) -> list
    def get_terminal(token) -> str
    def _is_terminal(simbolo) -> bool
    def _serializar_arvore(no) -> dict
```

#### 3. Funções Auxiliares

```python
def agruparTokensPorComando(tokens_planificados) -> list[list[dict]]
def parsear(tokens_planificados) -> dict
```

### Como Usar

#### Teste Rápido
```bash
python parsear.py
```

#### Teste de Integração
```bash
python test_parsear.py
```

#### Uso em Código
```python
from parsear import parsear
from lerArquivo import lerTokenStr

# Ler tokens
tokens = lerTokenStr('token.txt')

# Fazer parsing
resultado = parsear(tokens)

# Verificar resultado
if resultado['sucesso']:
    print("✅ Parsing bem-sucedido!")
else:
    print(f"❌ {resultado['resumo']}")
```

### Mapeamento Token → Terminal

| Token Tipo | Token Valor | Terminal |
|-----------|------------|----------|
| PARENTESIS | `(` | PARENTESIS_ESQ |
| PARENTESIS | `)` | PARENTESIS_DIR |
| NUMERO | `10`, `3.14` | NUMERO |
| VARIAVEL | `X`, `SOMA` | VARIAVEL |
| OPERADOR | `+`, `-`, `*`, `/`, `//`, `%`, `^` | OPERADOR |
| COMANDO | `MEM` | MEM |
| COMANDO | `RES` | RES |
| COMANDO | `IF` | IF |
| COMANDO | `WHILE` | WHILE |
| COMANDO | `IFELSE` | IFELSE |

### Gramática LL(1)

```
Programa    → ( START ) ListaOuFim
ListaOuFim  → ( ConteudoOuFim
ConteudoOuFim → END ) | Conteudo ) ListaOuFim
Comando     → ( Conteudo )
Conteudo    → Elemento RestoConteudo
RestoConteudo → Elemento Cauda | RES | ε
Cauda       → OPERADOR | MEM | IF | WHILE | IFELSE
Elemento    → NUMERO | VARIAVEL | Comando
```

### Exemplo de Saída

```python
{
    'sucesso': True,
    'resultados': [
        {
            'numero_comando': 1,
            'sucesso': True,
            'derivacoes': [
                'Programa → ( START ) ListaOuFim',
                'ListaOuFim → ( ConteudoOuFim',
                ...
            ],
            'arvore': {
                'rotulo': 'Programa',
                'tipo': 'nao_terminal',
                'valor': None,
                'filhos': [...]
            },
            'erros': []
        },
        ...
    ],
    'resumo': '9/9 comandos válidos'
}
```

---
