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
    pass

def calcularFollow(gramatica, firsts):
    pass

def construirTabelaLL1(gramatica, firsts, follows):
    pass