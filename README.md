# RA1_15 - Compilador RPN → ARMv7 Assembly

## Informações do Projeto

- **Matéria**: Linguagens Formais e Compiladores
- **Professor**: FRANK COELHO DE ALCANTARA
- **Faculdade**: PUCPR (Pontifícia Universidade Católica do Paraná)
- **Grupo**: RA1_15

## Descrição

Implementação de um compilador que processa expressões em notação RPN (Reverse Polish Notation) e gera código Assembly ARMv7 para a arquitetura Cpulator ARMv7 DEC1-SOC v16.1.

## Características

- **Aluno 1**: Vinicius Cordeiro Vogt
- **Aluno 2**: Andrei de Carvalho Bley
- **Aluno 3**: Vitor Matias Percegona Bilbao
- **Aluno 4**: Vinicius Cordeiro Vogt

## Operações Suportadas

- Operadores aritméticos: `+`, `-`, `*`, `/`, `//` (div. inteira), `%` (módulo), `^` (potência)
- Comandos: `MEM` (salvar em memória), `RES` (recuperar resultado anterior)
- Números em ponto flutuante (IEEE 754 64-bit)

## Como Executar

```bash
python main.py <arquivo_teste.txt>
```

**Exemplo**:
```bash
python main.py teste_1.txt
```

## Arquivos de Saída

- `token.txt`: Lista de tokens gerados pelo analisador léxico (analisador_lexico.py)
- `saida.s`: Código Assembly ARMv7 gerado (gerarAssembly.py)

## Estrutura de Arquivos

- `analisador_lexico.py`: Implementação da análise léxica (Vinicius Cordeiro Vogt)
- `geren_memo.py`: Processador RPN e gerenciador de memória (Andrei de Carvalho Bley)
- `gerarAssembly.py`: Gerador de código Assembly (Vitor Matias Percegona Bilbao)
- `main.py`: Orquestrador e interface (Vinicius Cordeiro Vogt)
- `teste_1.txt`, `teste_2.txt`, `teste_3.txt`: Arquivos de teste (todos)
