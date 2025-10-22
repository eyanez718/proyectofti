import random

# Función que crea el tablero generando un camino garantizado de X a 0
# el resto de las casillas las completa de forma aleatoria.
def crear_tablero_con_camino(n):
    tablero = [["*" for _ in range(n)] for _ in range(n)]

    x_i, x_j = random.randint(0, n - 1), random.randint(0, n - 1)
    o_i, o_j = random.randint(0, n - 1), random.randint(0, n - 1)
    while (x_i, x_j) == (o_i, o_j):
        o_i, o_j = random.randint(0, n - 1), random.randint(0, n - 1)

    camino = [(x_i, x_j)]
    i, j = x_i, x_j
    while (i, j) != (o_i, o_j):
        if i < o_i:
            i += 1
        elif i > o_i:
            i -= 1
        elif j < o_j:
            j += 1
        elif j > o_j:
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
    tablero[x_i][x_j] = "X"
    tablero[o_i][o_j] = "0"

    return tablero, (x_i, x_j)

# Función que imprime el tablero
def mostrar_tablero(tablero):
    n = len(tablero)
    borde_horizontal = "+" + "---+" * n

    print(borde_horizontal) # Imprimo el borde superior
    for fila in tablero:
        fila_str = "| " + " | ".join(fila) + " |"
        print(fila_str) # Imprimo la fila
        print(borde_horizontal) # Imprimo el borde inferior a la fila
        
# Función que maneja el movimiento del jugador
def mover_jugador(tablero, pos, direccion):
    i, j = pos
    n = len(tablero)
    nueva_i, nueva_j = i, j

    if direccion == "w": # Moverse a arriba
        nueva_i -= 1
    elif direccion == "s": # Moverse a abajo
        nueva_i += 1
    elif direccion == "a": # Moverse a izquierda
        nueva_j -= 1
    elif direccion == "d": # Moverse a derecha
        nueva_j += 1
    else:
        print("Movimiento inválido. Usar: w (arriba), s (abajo), a (izquierda), d (derecha).")
        return pos, "invalido"

    if 0 <= nueva_i < n and 0 <= nueva_j < n:
        celda = tablero[nueva_i][nueva_j]

        if celda == "*":
            print("\nEncontraste un obstaculo. Perdiste.")
            tablero[i][j] = " "
            tablero[nueva_i][nueva_j] = "P"
            return (nueva_i, nueva_j), "perdio"
        elif celda == "0":
            print("\n¡Encontraste el objetivo! Ganaste.")
            tablero[i][j] = " "
            tablero[nueva_i][nueva_j] = "G"
            return (nueva_i, nueva_j), "gano"
        else:
            tablero[i][j] = " "
            tablero[nueva_i][nueva_j] = "X"
            return (nueva_i, nueva_j), "sigue"
    else:
        print("\nNo podés salir de los límites del tablero.")
        return pos, "invalido"

# Bloque principal, pide que se ingrese la dimensión del tablero,
# luego pide los movimientos hasta que se termina el juego
while True:
    try:
        n = int(input("Ingresar el tamaño del tablero de nxn donde n >= 3: "))
        if n >= 3:
            break
        else:
            print("n debe ser >= 3.")
    except ValueError:
        print("Número inválido.")

tablero, posicion_jugador = crear_tablero_con_camino(n)

print("Para moverse, usar: w (arriba), s (abajo), a (izquierda), d (derecha).\n")
mostrar_tablero(tablero)

while True:
    direccion = input("\nIngresar el siguiente movimiento: ").strip().lower()
    posicion_jugador, estado = mover_jugador(tablero, posicion_jugador, direccion)
    mostrar_tablero(tablero)

    if estado in ["gano", "perdio"]:
        break