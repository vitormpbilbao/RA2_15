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
*COLOCA AS PARADAS DO ALUNO 4 AQUI, TMJ AMIGOS*