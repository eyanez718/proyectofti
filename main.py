import random
from automata.fa.nfa import NFA
from automata.base.exceptions import RejectionException

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
    n = len(tablero)
    bordeHorizontal = "+" + "---+" * n

    print(bordeHorizontal) # Imprimo el borde superior
    for fila in tablero:
        filaStr = "| " + " | ".join(fila) + " |"
        print(filaStr) # Imprimo la fila
        print(bordeHorizontal) # Imprimo el borde inferior a la fila
        
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

while True:
    try:
        auxContinuarJugando = input("\nDesea jugar? S = Sí - N = No: ")
        if auxContinuarJugando == "S" or auxContinuarJugando == "s":
            while True:
                try:
                    while True:
                        try:
                            n = int(input("\nIngresar el tamaño del tablero de nxn donde n >= 3: "))
                            if n >= 3:
                                break
                            else:
                                print("\nn debe ser >= 3.")
                        except ValueError:
                            print("\nNúmero inválido.")

                    auxModoJuego = int(input("\nSeleccione el modo de juego (1 = camino completo / 2 = Paso a paso / 0 = Cancelar): "))
                    #GENERO EL AUTOMATA
                    #n = 3 # BORRAR

                    tablero, posicionJugador = crearTablero(n)
                    automata = crearAutomataDesdeTablero(tablero)

                    #FIN GENEARCION AUTOMATA
                    if auxModoJuego == 1:
                        print("\nOpción seleccionada 'Camino completo'")
                        mostrarTablero(tablero)
                        auxCaminoElegido = input("\nIngrese una secuencia de movimientos, usar: w (arriba), s (abajo), a (izquierda), d (derecha): ")
                        if automata.accepts_input(auxCaminoElegido):
                            print("\n✅ Objetivo conseguido")
                        else:
                            print("\n❌ Objetivo no alcanzado")
                        break
                    else:
                        if auxModoJuego == 2:
                            print("\nOpción seleccionada 'Paso a paso'")
                            mostrarTablero(tablero)
                            print("\nPara moverse, usar: w (arriba), s (abajo), a (izquierda), d (derecha).")
                            auxEstadoActual = automata.initial_state
                            # Bucle interactivo
                            while True:
                                auxMovimiento = input("Ingresa el siguiente movimiento: ")

                                if not auxMovimiento:  # terminar la cadena
                                    break
                                
                                if auxMovimiento not in automata.input_symbols:
                                    print(f"\nSímbolo inválido. Solo se aceptan: {automata.input_symbols}")
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
                                    print("\n❌ Movimiento no permitido desde este estado")

                            # Resultado final
                            if auxEstadoActual in automata.final_states:
                                print("\n✅ Objetivo alcanzado. Juego ganado.")
                            else:
                                print("\n❌ Objetivo no alcanzado. Juego perdido.")
                            break
                        else:
                            if auxModoJuego == 0:
                                break
                            else:
                                print("\nOpción inválida.")
                except ValueError:
                    print("\nOpción inválida.")
        else:
            if auxContinuarJugando == "N" or auxContinuarJugando == "n":
                break
            else:
                print("\nOpción no reconocida.")
    except ValueError:
        print("\nOpción inválida.")