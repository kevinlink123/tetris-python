from random import randint

ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1
CUBO = 0
Z = 1
S = 2
I = 3
L = 4
L_INV = 5
T = 6

PIEZAS = (
    ((0, 0), (1, 0), (0, 1), (1, 1)), # Cubo
    ((0, 0), (1, 0), (1, 1), (2, 1)), # Z (zig-zag)
    ((0, 0), (0, 1), (1, 1), (1, 2)), # S (-Z)
    ((0, 0), (0, 1), (0, 2), (0, 3)), # I (línea)
    ((0, 0), (0, 1), (0, 2), (1, 2)), # L
    ((0, 0), (1, 0), (2, 0), (2, 1)), # -L
    ((0, 0), (1, 0), (2, 0), (1, 1)), # T
)

def generar_pieza(pieza=None):
    """
    Genera una nueva pieza de entre PIEZAS al azar. Si se especifica el parámetro pieza
    se generará una pieza del tipo indicado. Los tipos de pieza posibles
    están dados por las constantes CUBO, Z, S, I, L, L_INV, T.

    El valor retornado es una tupla donde cada elemento es una posición
    ocupada por la pieza, ubicada en (0, 0). Por ejemplo, para la pieza
    I se devolverá: ( (0, 0), (0, 1), (0, 2), (0, 3) ), indicando que 
    ocupa las posiciones (x = 0, y = 0), (x = 0, y = 1), ..., etc.
    """

    #Retorna la pieza indicada si se especifica
    if(pieza):
        nuevaPieza = list(PIEZAS[pieza])        
        return tuple(nuevaPieza)

    
    piezaAleatoria = randint(0, len(PIEZAS))
    nuevaPieza = list(PIEZAS[piezaAleatoria])
    return tuple(nuevaPieza)

def trasladar_pieza(pieza, dx, dy):
    """
    Traslada la pieza de su posición actual a (posicion + (dx, dy)).

    La pieza está representada como una tupla de posiciones ocupadas,
    donde cada posición ocupada es una tupla (x, y). 
    Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
    el desplazamiento dx=2, dy=3 se devolverá la pieza 
    ( (2, 3), (2, 4), (2, 5), (2, 6) ).
    """
    #Lista mutable
    bloqueTransladado = []
    #( (0, 0), (1, 0), (2, 0), (1, 1) ) T

    #( (0, 0), (0, 1), (0, 2), (1, 2) ) L
    for bloque in pieza:
        if(bloque[0] + dx > ANCHO_JUEGO or bloque[1] + dy > ALTO_JUEGO):
            return pieza

        if(bloque[0] + dx < 0 or bloque[1] + dy < 0):
            return pieza

        bloqueTransladado.append( (bloque[0] + dx, bloque[1] + dy) )

    #Nueva tupla inmutable con nuevas cordenadas
    piezaTransladada = tuple(bloqueTransladado)
    return piezaTransladada

def crear_juego(pieza_inicial):
    """
    Crea un nuevo juego de Tetris.

    El parámetro pieza_inicial es una pieza obtenida mediante 
    pieza.generar_pieza. Ver documentación de esa función para más información.

    El juego creado debe cumplir con lo siguiente:
    - La grilla está vacía: hay_superficie da False para todas las ubicaciones
    - La pieza actual está arriba de todo, en el centro de la pantalla.
    - El juego no está terminado: terminado(juego) da False

    Que la pieza actual esté arriba de todo significa que la coordenada Y de 
    sus posiciones superiores es 0 (cero).
    """

    juego = {
        'grilla': [ [() for x in range(ANCHO_JUEGO)] for x in range(ALTO_JUEGO) ],
        'pieza_actual': pieza_inicial
    }

    return juego

def dimensiones(juego):
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """
    return (ANCHO_JUEGO, ALTO_JUEGO)

def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """ 

    return juego['pieza_actual']

def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.
    
    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    #Out of Bounds
    if(x >= ANCHO_JUEGO or y >= ALTO_JUEGO):
        return True

    #Si en el bloque con coordenadas x e y no hay una lista vacia, entonces ese lugar esta ocupado
    if(juego['grilla'][y][x] != ()):
        return True

    return False

def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado 
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """
    piezaActual = juego['pieza_actual'];
    #( (0, 0), (1, 0), (2, 0), (1, 1) )

    for bloque in piezaActual:
        #Chequea si sobrepasa el ancho de la grilla del juego
        if(bloque[0] + direccion < 0 ):
            return juego
        elif(bloque[0] + direccion > ANCHO_JUEGO):
            return juego
        
        #Chequea si tiene bloques adyacentes
        if(hay_superficie(juego, bloque[0] + direccion, bloque[1])):
            return juego
        
        juego['pieza_actual'] = trasladar_pieza(piezaActual, direccion, 0)
    return juego

def avanzar(juego, siguiente_pieza):
    """
    Avanza al siguiente estado de juego a partir del estado actual.
    
    Devuelve una tupla (juego_nuevo, cambiar_pieza) donde el primer valor
    es el nuevo estado del juego y el segundo valor es un booleano que indica
    si se debe cambiar la siguiente_pieza (es decir, se consolidó la pieza
    actual con la superficie).
    
    Avanzar el estado del juego significa:
     - Descender una posición la pieza actual.
     - Si al descender la pieza no colisiona con la superficie, simplemente
       devolver el nuevo juego con la pieza en la nueva ubicación.
     - En caso contrario, se debe
       - Consolidar la pieza actual con la superficie.
       - Eliminar las líneas que se hayan completado.
       - Cambiar la pieza actual por siguiente_pieza.

    Si se debe agregar una nueva pieza, se utilizará la pieza indicada en
    el parámetro siguiente_pieza. El valor del parámetro es una pieza obtenida 
    llamando a generar_pieza().

    **NOTA:** Hay una simplificación respecto del Tetris real a tener en
    consideración en esta función: la próxima pieza a agregar debe entrar 
    completamente en la grilla para poder seguir jugando, si al intentar 
    incorporar la nueva pieza arriba de todo en el medio de la grilla se
    pisara la superficie, se considerará que el juego está terminado.

    Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada, 
    se debe devolver el mismo juego que se recibió.
    """
    #((0, 0), (1, 0), (2, 0), (1, 1))
    if(terminado(juego)):
        return (juego, False)

    piezaActual = juego['pieza_actual']
    #Copia de la grilla original
    grilla = juego['grilla']

    cambiar_pieza = False

    for bloque in piezaActual:
        #Chequea si existe algun bloque debajo
        if(hay_superficie(juego, bloque[0], bloque[1] + 1)):
            cambiar_pieza = True
            break
    
    if(cambiar_pieza):
        #Llena los lugares correspondientes
        for bloque in piezaActual:
            #( (0, 14), (0, 15), (0, 16), (0, 17) )
            grilla[bloque[1]] [bloque[0]] = bloque

        juego_nuevo = {
            'pieza_actual': siguiente_pieza,
            'grilla': grilla
        }

        #Borra lineas completadas
        for y in range(ALTO_JUEGO):
            for x in range(ANCHO_JUEGO):
                if(not hay_superficie(juego_nuevo, x, ALTO_JUEGO - 1 - y)):
                    break
                
                if(x == 8):
                    filaVacia = []
                    for i in range(ANCHO_JUEGO):
                        filaVacia.append( () )
                    juego_nuevo['grilla'][ALTO_JUEGO - 1 - y] = filaVacia

    else:
        juego_nuevo = {
        'pieza_actual': trasladar_pieza(piezaActual, 0, 1),
        'grilla': grilla
        }
    
    

    return [juego_nuevo, cambiar_pieza]

def terminado(juego):

    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """
    piezaActual = juego['pieza_actual']


    #( (0, 0), (0, 1), (0, 2), (0, 3) )
    for bloque in piezaActual:
        if(hay_superficie(juego, bloque[0], bloque[1])):
            return True

    return False
