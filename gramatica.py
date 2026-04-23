def construirGramatica():
    return {
        "Programa": [
            ["PARENTESIS_ESQ", "START", "PARENTESIS_DIR", "ListaCmd", "PARENTESIS_ESQ", "END", "PARENTESIS_DIR"]
        ],
        
        "ListaCmd": [
            ["Comando", "ListaCmd"],
            ["EPSILON"]
        ],
        
        "Comando": [
            ["PARENTESIS_ESQ", "Conteudo", "PARENTESIS_DIR"]
        ],
    
        "Conteudo": [
            ["Elemento", "RestoConteudo"]
        ],
        
        "RestoConteudo": [
            ["Elemento", "Cauda"],
            ["RES"],         
            ["EPSILON"]
        ],
        
        "Cauda": [
            ["OPERADOR"], ["MEM"], ["IF"], ["WHILE"]
        ],
        
        "Elemento": [
            ["NUMERO"], 
            ["VARIAVEL"], 
            ["Comando"]
        ]
    }

def calcularFirst(gramatica):
    #cria dict
    firsts = {nt: set() for nt in gramatica}
    
    #se n estiver na lista o código assume que é não terminal
    terminais = {
        "PARENTESIS_ESQ", "PARENTESIS_DIR", "START", "END", "EPSILON",
        "RES", "OPERADOR", "MEM", "IF", "WHILE", "NUMERO", "VARIAVEL"
    }
    #roda
    teve_mudanca = True
    while teve_mudanca:
        teve_mudanca = False
        
        for nt, regras in gramatica.items():
            for regra in regras:
                tamanho_antigo = len(firsts[nt])
                for simbolo in regra:
                    if simbolo in terminais: #se achar terminal cai aqui
                        firsts[nt].add(simbolo)
                        break
                    else: #caso encontre um não terminal
                        firsts_do_vizinho = firsts[simbolo]
                        firsts[nt].update(firsts_do_vizinho - {"EPSILON"})
                        if "EPSILON" not in firsts_do_vizinho:
                            break
                else:
                    firsts[nt].add("EPSILON")
                if len(firsts[nt]) > tamanho_antigo:
                    teve_mudanca = True

    return firsts

def calcularFollow(gramatica, firsts):
    pass

def construirTabelaLL1(gramatica, firsts, follows):
    pass