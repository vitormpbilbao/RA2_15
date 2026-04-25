# Fase 2 - Analisador Sintático LL(1)
**Responsável:** Vitor Bilbao

## 1. Gramática EBNF Fatorada
A gramática foi desenhada e fatorada à esquerda para eliminar a recursão natural da notação RPN e evitar conflitos FIRST/FIRST (especialmente no tratamento do fim de arquivo `END` e nos aninhamentos). Isso garante o determinismo necessário para um *parser* LL(1) descendente recursivo.

*(Legenda: não-terminais em letras minúsculas, TERMINAIS em letras MAIÚSCULAS)*

programa -> PARENTESIS_ESQ START PARENTESIS_DIR lista_ou_fim
lista_ou_fim -> PARENTESIS_ESQ conteudo_ou_fim
conteudo_ou_fim -> END PARENTESIS_DIR | conteudo PARENTESIS_DIR lista_ou_fim
comando -> PARENTESIS_ESQ conteudo PARENTESIS_DIR
conteudo -> elemento resto_conteudo
resto_conteudo -> elemento cauda | RES | EPSILON
cauda -> OPERADOR | MEM | IF | WHILE
elemento -> NUMERO | VARIAVEL | comando

---

## 2. Conjuntos FIRST
Conjuntos calculados automaticamente pelo algoritmo de ponto fixo:

* **FIRST(programa)** = {'PARENTESIS_ESQ'}
* **FIRST(lista_ou_fim)** = {'PARENTESIS_ESQ'}
* **FIRST(conteudo_ou_fim)** = {'END', 'NUMERO', 'VARIAVEL', 'PARENTESIS_ESQ'}
* **FIRST(comando)** = {'PARENTESIS_ESQ'}
* **FIRST(conteudo)** = {'NUMERO', 'VARIAVEL', 'PARENTESIS_ESQ'}
* **FIRST(resto_conteudo)** = {'NUMERO', 'VARIAVEL', 'PARENTESIS_ESQ', 'RES', 'EPSILON'}
* **FIRST(cauda)** = {'OPERADOR', 'MEM', 'IF', 'WHILE'}
* **FIRST(elemento)** = {'NUMERO', 'VARIAVEL', 'PARENTESIS_ESQ'}

---

## 3. Conjuntos FOLLOW
Conjuntos mapeando os terminais esperados após a derivação de um não-terminal:

* **FOLLOW(programa)** = {'$'}
* **FOLLOW(lista_ou_fim)** = {'$'}
* **FOLLOW(conteudo_ou_fim)** = {'$'}
* **FOLLOW(comando)** = {'PARENTESIS_DIR', 'NUMERO', 'VARIAVEL', 'PARENTESIS_ESQ', 'OPERADOR', 'MEM', 'IF', 'WHILE', 'RES'}
* **FOLLOW(conteudo)** = {'PARENTESIS_DIR'}
* **FOLLOW(resto_conteudo)** = {'PARENTESIS_DIR'}
* **FOLLOW(cauda)** = {'PARENTESIS_DIR'}
* **FOLLOW(elemento)** = {'PARENTESIS_DIR', 'NUMERO', 'VARIAVEL', 'PARENTESIS_ESQ', 'OPERADOR', 'MEM', 'IF', 'WHILE', 'RES'}

---

## 4. Tabela de Análise LL(1)
A Tabela LL(1) foi gerada com sucesso via script Python (`tabela[nao_terminal][terminal]`). 

Abaixo encontra-se o mapeamento determinístico gerado na última execução. **Nenhum conflito de ambiguidade foi detectado**, provando que a gramática é apta para o *Parser*:

**[programa]**
* Se ler 'PARENTESIS_ESQ' -> Usar regra: `['PARENTESIS_ESQ', 'START', 'PARENTESIS_DIR', 'lista_ou_fim']`

**[lista_ou_fim]**
* Se ler 'PARENTESIS_ESQ' -> Usar regra: `['PARENTESIS_ESQ', 'conteudo_ou_fim']`

**[conteudo_ou_fim]**
* Se ler 'END' -> Usar regra: `['END', 'PARENTESIS_DIR']`
* Se ler 'VARIAVEL' -> Usar regra: `['conteudo', 'PARENTESIS_DIR', 'lista_ou_fim']`
* Se ler 'NUMERO' -> Usar regra: `['conteudo', 'PARENTESIS_DIR', 'lista_ou_fim']`
* Se ler 'PARENTESIS_ESQ' -> Usar regra: `['conteudo', 'PARENTESIS_DIR', 'lista_ou_fim']`

**[comando]**
* Se ler 'PARENTESIS_ESQ' -> Usar regra: `['PARENTESIS_ESQ', 'conteudo', 'PARENTESIS_DIR']`

**[conteudo]**
* Se ler 'VARIAVEL' -> Usar regra: `['elemento', 'resto_conteudo']`
* Se ler 'NUMERO' -> Usar regra: `['elemento', 'resto_conteudo']`
* Se ler 'PARENTESIS_ESQ' -> Usar regra: `['elemento', 'resto_conteudo']`

**[resto_conteudo]**
* Se ler 'VARIAVEL' -> Usar regra: `['elemento', 'cauda']`
* Se ler 'NUMERO' -> Usar regra: `['elemento', 'cauda']`
* Se ler 'PARENTESIS_ESQ' -> Usar regra: `['elemento', 'cauda']`
* Se ler 'RES' -> Usar regra: `['RES']`
* Se ler 'PARENTESIS_DIR' -> Usar regra: `['EPSILON']`

**[cauda]**
* Se ler 'OPERADOR' -> Usar regra: `['OPERADOR']`
* Se ler 'MEM' -> Usar regra: `['MEM']`
* Se ler 'IF' -> Usar regra: `['IF']`
* Se ler 'WHILE' -> Usar regra: `['WHILE']`

**[elemento]**
* Se ler 'NUMERO' -> Usar regra: `['NUMERO']`
* Se ler 'VARIAVEL' -> Usar regra: `['VARIAVEL']`
* Se ler 'PARENTESIS_ESQ' -> Usar regra: `['comando']`

---
## 5. Árvore Sintática — Geração e Estrutura
 
**Responsável:** Todos (integração final coordenada por Vitor, Andrei e Vinicius)
 
### 5.1. Como a árvore é construída
 
A árvore sintática é gerada em dois passos. Primeiro, o *parser* (`parsear.py`) produz um dicionário serializado com a derivação completa de cada instrução. Em seguida, a função `gerarArvore()` em `gerarAssembly.py` percorre esse dicionário recursivamente e reconstrói objetos `No` navegáveis.
 
Cada nó da árvore tem três campos:
- `rotulo`: nome do símbolo gramatical (ex: `Conteudo`, `OPERADOR`, `VARIAVEL`)
- `tipo`: `"terminal"` para folhas ou `"nao_terminal"` para nós internos
- `valor`: preenchido apenas para terminais (ex: `"+"`, `"3.14"`, `"MEM"`)
### 5.2. Exemplo de árvore — instrução `( A PI + )`
 
```
└─ Programa
   ├─ PARENTESIS_ESQ: '('
   ├─ START: 'START'
   ├─ PARENTESIS_DIR: ')'
   └─ ListaOuFim
      ├─ PARENTESIS_ESQ: '('
      └─ ConteudoOuFim
         ├─ Conteudo
         │  ├─ Elemento
         │  │  └─ VARIAVEL: 'A'
         │  └─ RestoConteudo
         │     ├─ Elemento
         │     │  └─ VARIAVEL: 'PI'
         │     └─ Cauda
         │        └─ OPERADOR: '+'
         ├─ PARENTESIS_DIR: ')'
         └─ ListaOuFim
            └─ ...
```
 
### 5.3. Exemplo de árvore — estrutura `IF`
 
```
└─ Conteudo
   ├─ Elemento
   │  └─ Comando           ← bloco da condição ( A PI > )
   │     ├─ PARENTESIS_ESQ: '('
   │     ├─ Conteudo
   │     │  ├─ Elemento
   │     │  │  └─ VARIAVEL: 'A'
   │     │  └─ RestoConteudo
   │     │     ├─ Elemento
   │     │     │  └─ VARIAVEL: 'PI'
   │     │     └─ Cauda
   │     │        └─ OPERADOR: '>'
   │     └─ PARENTESIS_DIR: ')'
   └─ RestoConteudo
      ├─ Elemento
      │  └─ Comando          ← bloco do corpo ( ( 1 FLAG MEM ) )
      └─ Cauda
         └─ IF: 'IF'         ← keyword que fecha a estrutura
```
 
### 5.4. Arquivo de saída
 
A árvore completa do último teste executado é salva em `arvore.json`. O formato é um array JSON onde cada objeto representa uma instrução do programa:
 
```json
[
  {
    "instrucao": 1,
    "arvore": {
      "rotulo": "Programa",
      "tipo": "nao_terminal",
      "valor": null,
      "filhos": [ ... ]
    }
  },
  {
    "instrucao": 5,
    "arvore": null,
    "erro": "instrução com erro sintático"
  }
]
```
 
---
 
## 6. Geração de Código Assembly ARMv7
 
**Responsável:** Todos (integração final coordenada por Vitor e Andrei)
 
### 6.1. Estratégia
 
O código assembly é gerado diretamente a partir da árvore sintática, sem representação intermediária. A função `gerarAssembly()` instancia a classe `GeradorAssembly`, que percorre cada nó da árvore com o método `_visitar()` e despacha para o gerador correto de acordo com o tipo e valor do nó.
 
Todas as operações usam a FPU (VFPv3) com registradores de precisão dupla (`d0`–`d7`). Os operandos são empilhados via `VPUSH` e desempilhados via `VPOP`, seguindo o modelo de pilha RPN herdado da Fase 1.
 
### 6.2. Mapeamento de operadores para instruções
 
| Operador | Instrução ARMv7 | Observação |
|---|---|---|
| `+` | `VADD.F64 d0, d2, d1` | |
| `-` | `VSUB.F64 d0, d2, d1` | |
| `*` | `VMUL.F64 d0, d2, d1` | |
| `/` e `\|` | `VDIV.F64 d0, d2, d1` | divisão real |
| `//` | `VDIV` + `VCVT` trunca | divisão inteira via FPU |
| `%` | `VDIV` + `VCVT` + `VMUL` + `VSUB` | resto via FPU |
| `^` | loop com `VMUL.F64` | potência por iteração |
| `>`, `<`, `>=`, `<=`, `==`, `!=` | `VCMPE.F64` + `VMRS` + desvio | coloca 1.0 ou 0.0 na pilha |
 
### 6.3. Geração de IF e WHILE
 
Para estruturas de controle, o gerador detecta o padrão `Conteudo → Elemento RestoConteudo` com uma `Cauda` contendo `IF` ou `WHILE`. Quando encontra esse padrão:
 
**IF:** avalia a condição (resultado fica no topo da pilha), compara com `0.0` usando `VCMPE.F64`, e desvia para `fim_if_N` se for falso.
 
```asm
    @ IF: testa condição no topo da pilha
    VPOP {d0}
    LDR r0, =zero_if_0
    VLDR.F64 d1, [r0]
    VCMPE.F64 d0, d1
    VMRS APSR_nzcv, FPSCR
    BEQ fim_if_0
    @ corpo do IF
    ...
fim_if_0:
```
 
**WHILE:** reavalia a condição no início de cada iteração. Se falsa, sai do loop com `BEQ fim_while_N`.
 
```asm
inicio_while_0:
    @ avalia condição
    ...
    VPOP {d0}
    LDR r0, =zero_while_0
    VLDR.F64 d1, [r0]
    VCMPE.F64 d0, d1
    VMRS APSR_nzcv, FPSCR
    BEQ fim_while_0
    @ corpo do WHILE
    ...
    B inicio_while_0
fim_while_0:
```
 
### 6.4. Seção `.data`
 
Literais numéricos e variáveis são declarados estaticamente na seção `.data`. O gerador cria entradas únicas para cada literal (`num_0`, `num_1`, ...) e inicializa variáveis com `0.0`. Constantes auxiliares para comparações (`zero_if_N`, `rel_true_N`, `rel_false_N`) também são emitidas dinamicamente conforme necessário.