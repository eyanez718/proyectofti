import random
from automata.fa.nfa import NFA
from automata.base.exceptions import RejectionException
import colorama

# Función que crea el tablero generando un camino garantizado de X a 0
# el resto de las casillas las completa de forma aleatoria.
def crearTablero(n):
    tablero = [["*" for _ in range(n)] for _ in range(n)]

    xi, xj = random.randint(0, n - 1), random.randint(0, n - 1)
    oi, oj = random.randint(0, n - 1), random.randint(0, n - 1)
    while (xi, xj) == (oi, oj):
        oi, oj = random.randint(0, n - 1), random.randint(0, n - 1)

    camino = [(xi, xj)]
    i, j = xi, xj
    while (i, j) != (oi, oj):
        if i < oi:
            i += 1
        elif i > oi:
            i -= 1
        elif j < oj:
            j += 1
        elif j > oj:
            j -= 1
        camino.append((i, j))

    # Primero, abrir el camino garantizado
    for (ci, cj) in camino:
        tablero[ci][cj] = " "

    # Luego, rellenar las celdas que no están en el camino con "*" o " " al azar
    for i in range(n):
        for j in range(n):
            if (i, j) not in camino:
                tablero[i][j] = random.choice(["*", " "])

    # Colocar la X y el 0
    tablero[xi][xj] = "X"
    tablero[oi][oj] = "0"

    return tablero, (xi, xj)

# Función que crea escenarios fijos
def crearTableroFijo(n):
    if n == 3:
        simbolos = ["X", " ", " ", "*", " ", "*", "*", " ", "0"]

        # Convertir la lista en matriz 3x3
        tablero = [simbolos[i:i+3] for i in range(0, 9, 3)]

        return tablero, (0, 0)
    if n == 4:
        simbolos = ["X", " ", " ", "*", " ", "*", " ", " ", "*", " ", "*", " ", " ", "0", " ", " "]

        # Convertir la lista en matriz 3x3
        tablero = [simbolos[i:i+4] for i in range(0, 16, 4)]

        return tablero, (0, 0)
    if n == 5:
        simbolos = ["*", "*", " ", " ", "0", " ", " ", " ", "*", " ", " ", "*", "*", " ", " ", " ", " ", " ", "*", " ", "*", " ", "X", " ", " "]
        # Convertir la lista en matriz 3x3
        tablero = [simbolos[i:i+5] for i in range(0, 25, 5)]

        return tablero, (4, 2)


# Función que crea el autómata no determinista a partir del tablero
def crearAutomataDesdeTablero(tablero):
    filas = len(tablero)
    columnas = len(tablero[0])

    # Armo los estados
    estados = [f"q{i}" for i in range(filas*columnas)]
    estadoInicial = None
    estadosFinales = set()

    for i in range(filas):
        for j in range(columnas):
            simbolo = tablero[i][j]
            idx = i * columnas + j
            if simbolo == "X":
                estadoInicial = f"q{idx}"
            elif simbolo == "0":
                estadosFinales.add(f"q{idx}")

    # Creo las transiciones
    simbolosPosibles = {"w", "s", "a", "d"}
    transiciones = {}

    # Agrego las direcciones
    direcciones = {
        'w': (-1,0),
        's': (1,0),
        'a': (0,-1),
        'd': (0,1)
    }

    # Recorro la matriz
    for i in range(filas):
        for j in range(columnas):
            contenido = tablero[i][j]
            idx = i * columnas + j
            estadoActual = f"q{idx}"

            # Solo celdas "X" o " " generan transiciones
            if contenido in ["X", " "]:
                transiciones[estadoActual] = {}
                for simbolo, (di,dj) in direcciones.items():
                    ni, nj = i+di, j+dj
                    if 0 <= ni < filas and 0 <= nj < columnas:
                        estadoVecino = f"q{ni*columnas + nj}"
                        transiciones[estadoActual][simbolo] = {estadoVecino}

    # Armo el autómata no determinista
    automata = NFA(
        states=set(estados),
        input_symbols=simbolosPosibles,
        transitions=transiciones,
        initial_state=estadoInicial,
        final_states=estadosFinales
    )
    return automata

# Función que imprime el tablero
def mostrarTablero(tablero):
    colores = {
        "*": RED,
        "X": CYAN,
        "G": GREEN,
        "0": GREEN,
        "P": RED,
    }

    n = len(tablero)
    bordeHorizontal = "+" + "---+" * n

    print(bordeHorizontal)  # borde superior
    for fila in tablero:
        # Aplico el color a cada celda según su contenido
        fila_coloreada = []
        for celda in fila:
            color = colores.get(celda, "")
            celda_coloreada = f"{color}{celda}{RESET}"
            fila_coloreada.append(celda_coloreada)

        # Construyo la fila como antes
        filaStr = "| " + " | ".join(fila_coloreada) + " |"
        print(filaStr)
        print(bordeHorizontal)
#    n = len(tablero)
#    bordeHorizontal = "+" + "---+" * n

#    print(bordeHorizontal) # Imprimo el borde superior
#    for fila in tablero:
#        filaStr = "| " + " | ".join(fila) + " |"
#        print(filaStr) # Imprimo la fila
#        print(bordeHorizontal) # Imprimo el borde inferior a la fila
        
# Función que maneja el movimiento del jugador
def moverJugador(tablero, pos, direccion):
    i, j = pos
    n = len(tablero)
    nuevai, nuevaj = i, j

    if direccion == "w": # Moverse a arriba
        nuevai -= 1
    elif direccion == "s": # Moverse a abajo
        nuevai += 1
    elif direccion == "a": # Moverse a izquierda
        nuevaj -= 1
    elif direccion == "d": # Moverse a derecha
        nuevaj += 1
    else:
        print("Movimiento inválido. Usar: w (arriba), s (abajo), a (izquierda), d (derecha).")
        return pos, "invalido"

    if 0 <= nuevai < n and 0 <= nuevaj < n:
        celda = tablero[nuevai][nuevaj]

        if celda == "*":
            print("\nEncontraste un obstaculo. Perdiste.")
            tablero[i][j] = " "
            tablero[nuevai][nuevaj] = "P"
            return (nuevai, nuevaj), "perdio"
        elif celda == "0":
            print("\n¡Encontraste el objetivo! Ganaste.")
            tablero[i][j] = " "
            tablero[nuevai][nuevaj] = "G"
            return (nuevai, nuevaj), "gano"
        else:
            tablero[i][j] = " "
            tablero[nuevai][nuevaj] = "X"
            return (nuevai, nuevaj), "sigue"
    else:
        print("\nNo podés salir de los límites del tablero.")
        return pos, "invalido"

colorama.init()

RESET = "\033[0m"
RED = "\033[31m"
BLUE = "\033[34m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
GREEN = "\033[32m"

interfazGrafica = 0

while True:
    try:
        print(f"\n{YELLOW}¿Desea iniciar una nueva partida?{RESET}")
        print("    S = Sí")
        print("    N = No")
        auxContinuarJugando = input("\nRta: ")
        if auxContinuarJugando == "S" or auxContinuarJugando == "s":
            while True:
                try:
                    print(f"\n{YELLOW}Seleccione el tipo de tablero:{RESET}")
                    print("    1 = Fijo")
                    print("    2 = Aleatorio")
                    print("    0 = Cancelar")
                    tipoEscenario = int(input("\nRta: "))
                    if tipoEscenario == 1 or tipoEscenario == 2:
                        if (tipoEscenario == 1):
                            while True:
                                try:
                                    print(f"\n{YELLOW}Seleccione la dimensión del escenario{RESET}")
                                    print("    3 = 3x3")
                                    print("    4 = 4x4")
                                    print("    5 = 5x5")
                                    escenarioFijo = int(input("\nRta: "))
                                    if escenarioFijo == 3 or escenarioFijo == 4 or escenarioFijo == 5:
                                        tablero, posicionJugador = crearTableroFijo(escenarioFijo)
                                        break
                                    else:
                                        print(f"\n{RED}Opción inválida{RESET}")
                                except ValueError:
                                    print(f"\n{RED}Número inválido{RESET}")
                        else:
                            while True:
                                try:
                                    print(f"\n{YELLOW}Seleccione el tamaño del tablero de NxN donde N >= 3 y N <= 10{RESET}")
                                    n = int(input("\nRta: "))
                                    if n >= 3 and n <= 10:
                                        tablero, posicionJugador = crearTablero(n)
                                        break
                                    else:
                                        print(f"\n{RED}N debe ser >= 3 y <= 10{RESET}")
                                except ValueError:
                                    print(f"\n{RED}Número inválido{RESET}")

                        print(f"\n{YELLOW}Seleccione el modo de juego{RESET}")
                        print("    1 = Camino completo")
                        print("    2 = Paso a paso")
                        print("    0 = Cancelar")
                        auxModoJuego = int(input("\nRta: "))

                        automata = crearAutomataDesdeTablero(tablero)

                        if auxModoJuego == 1:
                            print(f"\n{CYAN}Opción seleccionada 'Camino completo'{RESET}\n")
                            mostrarTablero(tablero)
                            print(f"\n{YELLOW}Ingrese una secuencia de movimientos, usando: w (arriba), s (abajo), a (izquierda), d (derecha){RESET}")
                            auxCaminoElegido = input("Secuencia: ")
                            if automata.accepts_input(auxCaminoElegido):
                                print(f"\n{GREEN}Objetivo conseguido{RESET}")
                            else:
                                print(f"\n{RED}Objetivo no alcanzado{RESET}")
                            break
                        else:
                            if auxModoJuego == 2:
                                print(f"\n{CYAN}Opción seleccionada 'Paso a paso'{RESET}\n")
                                mostrarTablero(tablero)
                                print(f"\n{YELLOW}Para moverse, usar: w (arriba), s (abajo), a (izquierda), d (derecha) o ENTER para finalizar{RESET}")
                                auxEstadoActual = automata.initial_state
                                # Bucle interactivo
                                while True:
                                    auxMovimiento = input("\nIngrese el siguiente movimiento: ")

                                    if not auxMovimiento:  # terminar la cadena
                                        break
                                    
                                    if auxMovimiento not in automata.input_symbols:
                                        print(f"\n{RED}Símbolo inválido. Solo se aceptan: {automata.input_symbols}{RESET}")
                                        continue

                                    # Aplicar transición
                                    if auxMovimiento in automata.transitions[auxEstadoActual]:
                                        auxEstadoActual = next(iter(automata.transitions[auxEstadoActual][auxMovimiento]))

                                        posicionJugador, estado = moverJugador(tablero, posicionJugador, auxMovimiento)
                                        mostrarTablero(tablero)
                                        # Resultado final
                                        if auxEstadoActual in automata.final_states:
                                            break
                                        else:
                                            if estado == 'perdio':
                                                break
                                    else:
                                        print(f"\n{RED}Movimiento no permitido desde este estado{RESET}")

                                # Resultado final
                                if auxEstadoActual in automata.final_states:
                                    print(f"\n{GREEN}Objetivo alcanzado. Juego ganado{RESET}")
                                else:
                                    print(f"\n{RED}Objetivo no alcanzado. Juego perdido{RESET}")
                                break
                            else:
                                if auxModoJuego == 0:
                                    break
                                else:
                                    print(f"\n{RED}Opción inválida{RESET}")
                    else:
                        if tipoEscenario == 0:
                            break
                        else:
                            print(f"\n{RED}Opción inválida.{RESET}")
                except ValueError:
                    print(f"\n{RED}Opción inválida{RESET}")
        else:
            if auxContinuarJugando == "N" or auxContinuarJugando == "n":
                break
            else:
                print(f"\n{RED}Opción no reconocida{RESET}")
    except ValueError:
        print(f"\n{RED}Opción inválida{RESET}")