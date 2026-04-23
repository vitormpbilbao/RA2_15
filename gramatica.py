def construirGramatica():
    gramatica = {
        "Programa": [
            ["PARENTESIS_ESQ", "START", "PARENTESIS_DIR", "ListaCmd", "PARENTESIS_ESQ", "END", "PARENTESIS_DIR"]
        ],
    }
    
    return gramatica

def calcularFirst(gramatica):
    pass

def calcularFollow(gramatica, firsts):
    pass

def construirTabelaLL1(gramatica, firsts, follows):
    pass