# RA2_15 - Compilador RPN → ARMv7 Assembly (Fase 2)

## Informações do Projeto

- **Matéria**: Linguagens Formais e Compiladores
- **Professor**: FRANK COELHO DE ALCANTARA
- **Faculdade**: PUCPR (Pontifícia Universidade Católica do Paraná)
- **Grupo**: RA2_15

## Descrição

Implementação de um compilador completo baseado em uma gramática LL(1) fatorada. O sistema processa expressões em notação RPN (Reverse Polish Notation) integradas a estruturas de controle de fluxo e gera código Assembly ARMv7 compatível com a arquitetura Cpulator ARMv7 DEC1-SOC.

## Características da Fase 2

- **Gramática LL(1)**: Fatorada à esquerda para garantir determinismo e eliminar recursão.
- **Análise Sintática**: Implementação de um *parser* descendente recursivo que valida a estrutura do programa.
- **Árvore Sintática (AST)**: Geração e exportação da árvore de derivação em formato JSON.
- **Estruturas de Controle**: Suporte a blocos `IF` e laços `WHILE` aninhados.
- **Ponto Flutuante**: Operações realizadas via FPU (VFPv3) utilizando registradores de precisão dupla (64-bit).

## Responsabilidades

- **Aluno 1 (Gramática e Documentação LL1)**: Vitor Matias Percegona Bilbao
- **Aluno 2 (Parser Sintático)**: Vinicius Cordeiro Vogt
- **Aluno 3 (Analisador Léxico)**: Andrei de Carvalho Bley
- **Aluno 4 (Gerador de Assembly e Integração)**: Todos

## Operações e Comandos Suportados

- **Aritmética**: `+`, `-`, `*`, `/`, `//` (div. inteira), `%` (módulo), `^` (potência)
- **Relacional**: `>`, `<`, `>=`, `<=`, `==`, `!=`
- **Controle**: `START`, `END`, `IF`, `WHILE`
- **Memória**: `MEM` (armazenamento), `RES` (recuperação de resultado anterior)

## Como Executar

Certifique-se de que todos os arquivos `.py` estejam no mesmo diretório e execute:

```bash
python main.py <arquivo_teste.txt>
```


**Exemplo**:

```bash
python main.py teste_1.txt
```

## Arquivos de Saída

- `arvore.json`: Representação serializada da Árvore Sintática gerada.
- `saida.s`: Código Assembly ARMv7 final para execução no simulador.

## Estrutura de Arquivos

- `analisador_lexico.py`: DFA para reconhecimento de tokens, incluindo novas keywords e operadores relacionais.
- `gramatica.py`: Definição da gramática fatorada e lógica para tabelas LL(1).
- `parsear.py`: Motor de análise sintática que consome os tokens e constrói a AST.
- `gerarAssembly.py`: Tradutor da AST para instruções Assembly ARMv7 e manipulador de arquivos JSON.
- `main.py`: Orquestrador que executa as 5 fases da compilação.
- `documentacaoLL1.md`: Documentação técnica contendo os conjuntos FIRST, FOLLOW e a Tabela de Análise.
- `teste_1.txt`, `teste_2.txt`, `teste_3.txt`: Programas fonte para validação do compilador.