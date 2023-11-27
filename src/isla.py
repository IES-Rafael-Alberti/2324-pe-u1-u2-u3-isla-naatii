"""
Ejercicio: El Juego de la Búsqueda del Tesoro en la Isla

Descripción del Problema:

Los estudiantes están atrapados en una isla desierta y deben encontrar un tesoro escondido para escapar.

La isla está representada como una cuadrícula donde cada celda puede contener una pista que indica
la dirección general del tesoro, nada o una trampa que le impide el paso.

Los estudiantes deben usar su conocimiento de estructuras de datos y control de flujo para interpretar
las pistas, evitar las trampas y encontrar el tesoro.

Este es un ejemplo de mapa del tesoro con dimensión 5, con el tesoro en la posicion (0,0) y el jugador en la posicion (2,2)

El programa muestra lo siguiente al  usuario:

?   ?   ?
? ? ? ? ?
  ?   ?      
  ?   ? ?
? ? ?   ?
Tu posición es (2, 2)
Ingresa tu movimiento (formato: 'u:arriba', 'd:abajo', 'l:izquierda', 'r:derecha', q:salir):

Internamente tendréis una lista anidada para contener un mapa similar al siguiente:

columnas  0    1    2    3    4
filas
0       ["X", " ", "!", " ", "<"]
1       ["!", "^", "!", "<", "!"]
2       [" ", "^", " ", "<", " "]
3       [" ", "<", " ", "!", "^"]
4       ["!", "<", "!", " ", "^"]


Se pide realizar lo siguiente:

CORRECCIÓN DE ERRORES O PROBLEMAS:

* 1: El juego no se puede jugar()

* 2: Acaba la función generar_mapa() sino no vas a poder hacer nada.

* 3: Existen errores típicos de no declarar correctamente las funciones.

* 4: Las funciones pedir_movimiento() y obtener_nueva_posicion() tienen algo raro, ya que aparentemente parece que son correctas, pero dan problemas... igual depurando puedes aclararte y corregirlo.

* 5: Corrige otros errores sintácticos que te indique el IDE para evitar problemas y pasar a las mejoras.

MEJORAS:

* 1: Mostrar los números del tablero asociados a las filas y las columnas.
     Pero las filas y columnas que empiecen en el número 1 visualmente.

   1 2 3 4 5
  -----------
1 |? ? ? ? ?|
2 |?     ? ?|
3 |?       ?|
4 |? ? ? ? ?|
5 |  ? ? ? ?|
  -----------

* 2: Mostrar la posición del jugador con respecto a la numeración visual del mapa.

Tu posición es (3, 3)  #aunque internamente esté en la posición (2, 2)

* 3: Evitar que en la posición inicial del jugador en el mapa se genere una pista o una trampa.

* 4: Limpiar la consola cada vez que realices un movimiento y dejar el mensaje de la pista o trampa en la zona superior de la consola, justo arriba del mapa. Pero cuando se encuentra el tesoro no debe borrar la consola y el mensaje aparecerá abajo y finalizará el juego.

* 5 (DIFÍCIL): Mostrar un símbolo para el jugador. Para ello, una solución es cambiar el código de la función imprimir_mapa_oculto()
"""

import random
import os #* Lo usaré para limpiar la consola.

DIMENSIONES = 5

# Constantes para el mapa
CELDA_TESORO = "X"
CELDA_TRAMPA = "!"
CELDA_VACIA = " "
CELDA_JUGADOR = "🙍🏼"


# Constantes para las pistas de los movimientos
ARRIBA = "^"
ABAJO = "v"
DERECHA = ">"
IZQUIERDA = "<"

DESCONOCIDO = "?"

# Constantes para el resultado del movimiento
MOVIMIENTO_INVALIDO = 1
TESORO_ENCONTRADO = 2
TRAMPA_ENCONTRADA = 3
PISTA_ENCONTRADA = 4
VACIA_ENCONTRADA = 5
JUGADOR_ENCONTRADO = 6
MOVIMIENTOS_NO_PERMITIDO = [MOVIMIENTO_INVALIDO, TRAMPA_ENCONTRADA]

# Movimientos permitidos
SALIR = "q"
MOVIMIENTOS = {"u": (-1, 0), "d": (1, 0), "l": (0, -1), "r": (0, 1), SALIR: (0, 0)}
#? por qué salir es una constante y las demás no?
# Constantes para las posiciones
FILAS = 0
COLUMNAS = 1

# Código oculto del programador para realizar alguna acción que el usuario no sabe que existe. Si encuentras para qué se utiliza igual te sirve en tu aventura...
CODIGO_OCULTO_PROGRAMADOR = "s"
#! Esto sirve para revelar el mapa oculto.    

def inicializar_juego() -> tuple:
    """
    Inicializa el juego, mostrando el mapa y la posición del jugador.
    :return: El mapa y la posición del jugador.
    """
    posicion_jugador = posicion_inicial_del_jugador()
    mapa = generar_mapa()
    while mapa[posicion_jugador[FILAS]][posicion_jugador[COLUMNAS]] == CELDA_TESORO:
        mapa = generar_mapa()

    return mapa, posicion_jugador


def posicion_inicial_del_jugador() -> tuple:
    """ Devuelve la posición inicial del jugador. Actualmente es la posición central del mapa.
    :return: La posición inicial del jugador.
    """
    return DIMENSIONES // 2, DIMENSIONES // 2


def generar_mapa() -> list:
    """Genera un mapa de la isla con pistas y trampas correctamente colocadas. Con el siguiente contenido:
        - "X" indica el tesoro, y es única en el mapa.
        - "!" indica una trampa, y puede haber varias.
        - ^: indica que el tesoro esta una o mas filas arriba.
        - <: indica que el tesoro esta una o mas columnas a la izquierda.
        - >: indica que el tesoro esta una o mas columnas a la izquierda.
        - v: indica que el tesoro esta una o mas filas abajo.

    Genera mapas que puede que no tengan camino a la solución.
    :return: El mapa generado.
    """

    # Generar el mapa vacio y colocar el tesoro
    mapa = [[CELDA_VACIA for _ in range(DIMENSIONES)] for _ in range(DIMENSIONES)]
    tesoro_x, tesoro_y = random.randint(0, DIMENSIONES - 1), random.randint(0, DIMENSIONES - 1)
    mapa[tesoro_x][tesoro_y] = CELDA_TESORO

    # Colocar pistas y trampas
    for i in range(len(mapa)): #! Aquí he colocado 2 fors para recorrer el mapa y que se puedan recorrer las filas y columnas. 
        for j in range(i):
            if mapa[i][j] != CELDA_TESORO:
                # Decidir aleatoriamente si colocar una pista, una trampa o vacia.
                opciones = [genera_pista((tesoro_x, tesoro_y), (i, j))]
                opciones += [CELDA_TRAMPA]
                opciones += [CELDA_VACIA]
                mapa[i][j] = random.choice(opciones)

    return mapa

#! posicion_tesoro y posicion se declara en la función de arriba por lo que solo deberemos llamarla por parametro según los nombres que exiten dentro de la función.
def genera_pista(posicion_tesoro:tuple, posicion:tuple):
    """
    Genera una pista para el mapa, en función de donde se encuentre el tesoro.
    Decidirá si la pista es sobre la fila o la columna basada en la aleatoriedad. Ademas tiene en cuenta que
    si está en la misma fila que el tesoro, generará la pista para las columnas. Y si está en la misma columna
    generará la pista para la fila.
    :param posicion_tesoro: La posición del tesoro.
    :param posicion: La posición para la que se genera la pista.
    :return: La pista generada.
    """
    if random.choice([FILAS, COLUMNAS]) == FILAS:
        return genera_pista_filas(posicion_tesoro, posicion) or genera_pista_columnas(posicion_tesoro, posicion)
    else:
        return genera_pista_columnas(posicion_tesoro, posicion) or genera_pista_filas(posicion_tesoro, posicion)


def genera_pista_filas(posicion_tesoro: tuple, posicion: tuple):
    """Genera una pista basada en la comparación de filas.
    :param posicion_tesoro: La posición del tesoro.
    :param posicion: La posición para la que se genera la pista.
    :return: La pista generada.

    """
    if posicion_tesoro[FILAS] < posicion[FILAS]:
        return ARRIBA
    elif posicion_tesoro[FILAS] > posicion[FILAS]:
        return ABAJO
    return ""


def genera_pista_columnas(posicion_tesoro: tuple, posicion: tuple):
    """Genera una pista basada en la comparación de columnas.
    :param posicion_tesoro: La posición del tesoro.
    :param posicion: La posición para la que se genera la pista.
    :return: La pista generada.
    """
    if posicion_tesoro[COLUMNAS] < posicion[COLUMNAS]:
        return IZQUIERDA
    elif posicion_tesoro[COLUMNAS] > posicion[COLUMNAS]:
        return DERECHA
    return ""


def pedir_movimiento(mapa: list) -> str:
    """
    Pide al jugador su próximo movimiento y devuelve las coordenadas de desplazamiento.
    return: el movimiento del jugador
    """
    entrada_correcta = False
    # todo: Esto no recoge bien las posiciones
    entrada = input("Ingresa tu movimiento (formato: 'u:arriba', 'd:abajo', 'l:izquierda', 'r:derecha', q:salir): ")
    while entrada_correcta == False: #! quité la negación de la condición y le pregunté si es == False.
        if entrada in MOVIMIENTOS: 
            entrada_correcta = True
        elif entrada == CODIGO_OCULTO_PROGRAMADOR:
            imprimir_mapa(mapa)

        if not entrada_correcta:
            entrada = input(
                "Ingresa tu movimiento (formato: 'u:arriba', 'd:abajo', 'l:izquierda', 'r:derecha', q:salir): ")

    return entrada


def obtener_nueva_posicion(posicion_jugador: tuple, movimiento: str) -> tuple:
    """
    Realiza el movimiento del jugador y devuelve la nueva posición.

    :param posicion_jugador: La posición actual del jugador.
    :param movimiento: El movimiento a realizar.
    :return: La nueva posición del jugador.
    """

    direccion = MOVIMIENTOS[movimiento] #! cambié los parentesis por unos corchetes para acceder al valor de cada movimiento.
    nueva_posicion = (posicion_jugador[FILAS] + direccion[FILAS], posicion_jugador[COLUMNAS] + direccion[COLUMNAS])
    return nueva_posicion

def procesar_movimiento(posicion: tuple, mapa: list) -> int:
    """Procesa el movimiento del jugador y devuelve el código de resultado.
    :param posicion: La posición a la que se mueve el jugador.
    :param mapa: El mapa del juego.
    :return: El código de resultado del movimiento.

    """

    resultado = VACIA_ENCONTRADA
    if not (0 <= posicion[FILAS] < DIMENSIONES and 0 <= posicion[COLUMNAS] < DIMENSIONES):
        resultado = MOVIMIENTO_INVALIDO  # Código de error para movimiento fuera de rango
    elif mapa[posicion[FILAS]][posicion[COLUMNAS]] == CELDA_TESORO:
        resultado = TESORO_ENCONTRADO  # Código para tesoro encontrado
    elif mapa[posicion[FILAS]][posicion[COLUMNAS]] == CELDA_TRAMPA:
        resultado = TRAMPA_ENCONTRADA  # Código para trampa encontrada
    elif mapa[posicion[FILAS]][posicion[COLUMNAS]] != CELDA_VACIA:
        resultado = PISTA_ENCONTRADA  # Código para pista encontrada
    
    return resultado


def simbolo_celda(celda:str):
    """Retorna el símbolo a pintar en la celda"""
    if celda != CELDA_VACIA: #! Bloque de código reparado, faltaban los :
        return DESCONOCIDO
    else:
        return CELDA_VACIA 


def imprimir_mapa_oculto(mapa: list):
    """Imprime el mapa sin revelar el tesoro ni las trampas."""
    print(" ".join(str(i + 1) for i in range(len(mapa))))
    for fila in mapa:
        print(" ".join([simbolo_celda(celda) for celda in fila]))


def imprimir_mapa(mapa: list):
    """
    Imprime el mapa.
    :param mapa: El mapa a imprimir.
    """
    
    for fila in mapa:
        print(fila) #! Bloque de código reparado faltaba el parentesis de la función print().


def muestra_resultado_del_movimiento(resultado: int, nueva_posicion: tuple, mapa: list):
    """
    Muestra en consola el resultado del movimiento del jugador.
    :param resultado: El resultado del movimiento.
    :param nueva_posicion: La nueva posición del jugador.
    :param mapa: El mapa del juego.

    """
    if resultado == MOVIMIENTO_INVALIDO:
        print("Movimiento inválido. Estás intentando salir del mapa.")
    elif resultado == TESORO_ENCONTRADO:
        print("¡Has encontrado el tesoro y ganado el juego!")
    elif resultado == TRAMPA_ENCONTRADA:
        print("Es una trampa. Intenta de nuevo.")
    elif resultado == PISTA_ENCONTRADA:
        pista = mapa[nueva_posicion[FILAS]][nueva_posicion[COLUMNAS]]
        print(f"Hay una pista!!!! La pista es: {pista}")


def muestra_estado_mapa(mapa, posicion_jugador):
    """Muestra el mapa y la posición del jugador."""

    imprimir_mapa_oculto(mapa)
    print(f"Tu posición es {posicion_jugador}")


def jugar():
    """Función principal para iniciar el juego."""

    # Iniciar el mapa y al jugador en el centro del mapa
    mapa, posicion_jugador = inicializar_juego()
    muestra_estado_mapa(mapa, posicion_jugador)

    movimiento = pedir_movimiento(mapa)
    resultado_movimiento = None
    # Loop principal del juego. El juego termina cuando el jugador realizar movimiento SALIR.
    while movimiento != SALIR and resultado_movimiento != TESORO_ENCONTRADO: #! cambié la comprobación de la condicion de resultado_movimiento de == a !=.

        # Obtener la nueva posición del jugador y procesar el movimiento
        nueva_posicion = obtener_nueva_posicion(posicion_jugador, movimiento)#! agregé el parametro movimiento.
        resultado_movimiento = procesar_movimiento(nueva_posicion, mapa)

        muestra_resultado_del_movimiento(resultado_movimiento, nueva_posicion, mapa)

        if resultado_movimiento != TESORO_ENCONTRADO:
            # Actualizar la posición del jugador si el movimiento es válido
            if resultado_movimiento not in MOVIMIENTOS_NO_PERMITIDO:
                posicion_jugador = nueva_posicion

            muestra_estado_mapa(mapa, posicion_jugador)
            movimiento = pedir_movimiento(mapa)


if __name__ == "__main__":
    jugar()