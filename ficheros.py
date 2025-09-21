import os, textwrap

color_verde = "\033[32m"
reset_color = "\033[0m"

def rutaValida(ruta):
    """
    Verifica si una ruta existe

    Args:
        ruta (str): Ruta relativa o absoluta
    
    Returns:
        bool: True si la ruta exista. False en caso contrario
    """
    return os.path.exists(ruta)

def obtener_ruta():
    """
    Obtiene la ruta del usuario

    Returns:
        str: Ruta absoluta
    """
    ruta_valida = False
    while not ruta_valida:
        ruta = input(f"Introduce la ruta (relativa/absoluta) | (pulsa {color_verde}<enter>{reset_color} para salir): ").strip()
        if ruta == "":
            return None
        ruta_absoluta = os.path.abspath(ruta)
        ruta_valida = rutaValida(ruta_absoluta)
        if not ruta_valida:
            print("❌ La ruta no existe. Intente de nuevo.")
    return ruta_absoluta

def crear_fichero_carpeta(tipo, ruta, nombre):
    """
    Crea un fichero/carpeta en la ruta que le indiques

    Args:
        tipo (str): tipo de archivo (fichero/carpeta)
        ruta (str): nombre de la ruta
        nombre (str): nombre del nuevo elemento
    """
    match tipo:
        case 'fichero':
            ruta_fichero = os.path.join(ruta, nombre) + '.txt'
            with open(ruta_fichero, "w", encoding="utf-8") as fichero:
                fichero.write("")
            print(f"Fichero creado en: {ruta_fichero}")

        case 'carpeta':
            ruta_carpeta = os.path.join(ruta, nombre)
            os.makedirs(ruta_carpeta, exist_ok=True)
            print(f"Carpeta creada en: {ruta_carpeta}")

def leer_fichero(ruta):
    """
    Devuelve el contenido del fichero en un str

    Args:
        ruta (str): nombre de la ruta del fichero
    """
    if not os.path.isfile(ruta):
        return None
    
    with open(ruta, 'r', encoding="utf-8") as fichero:
        return fichero.read()
    
def mostrar_fichero(nombre_fichero, texto):
    """
    Muestra por pantalla el texto del fichero que le pases con formato

    Args:
        nombre_fichero (str): nombre del fichero
        texto (str): texto plano del fichero
    """
    ancho = 60
    borde = color_verde + "+" + "-" * (ancho - 2) + "+" + reset_color

    print(borde)
    print(f"{color_verde}|{reset_color}" 
          + nombre_fichero.center(ancho - 2) 
          + f"{color_verde}|{reset_color}")
    
    print(borde)
    for linea in texto.splitlines():
        for sublinea in textwrap.wrap(linea, width=ancho - 4):
            print(f"{color_verde}|{reset_color} {sublinea.ljust(ancho - 4)} {color_verde}|{reset_color}")
        if not linea.strip():
            print(f"{color_verde}|{reset_color}" + " " * (ancho - 2) + f"{color_verde}|{reset_color}")
    print(borde)

def borrar_elemento(ruta):
    """
    Se encarga de borrar un fichero/carpeta

    Args:
        ruta (str): el nombre de la ruta donde se ubique el elemento
    """
    if os.path.isfile(ruta):
        os.remove(ruta)
        print(f"Fichero eliminado: {ruta}")

    elif os.path.isdir(ruta):
        for elemento in os.listdir(ruta):
            ruta_completa = os.path.join(ruta, elemento)
            borrar_elemento(ruta_completa)
        os.rmdir(ruta)
        print(f"Carpeta eliminada: {ruta}")

def mover_elemento(ruta_origen, ruta_destino):
    """
    Se encarga de mover archivos de una ruta a otra

    Args:
        ruta_origen (str): ruta original del elemento
        ruta_destino (str): ruta nueva del elemento
    """
    os.rename(ruta_origen, ruta_destino)
    print(f"Se ha movido {ruta_origen} a {ruta_destino}")
    

def listar_arbol(ruta, prefijo="", contador=None, mapeo_rutas=None, indice=False):
    """
    Se encarga de listar en un arbol de directorios todos los archivos que tenga en la ruta que se le indique

    Args:
        ruta (str): el nombre de la ruta
        prefijo (str): el espacio de separacion en los anidamientos visuales
        contador (list[int]): una lista que contenga el numero por el que se empezara a listar los archivos en el arbol
        mapeo_rutas (dict): diccionario que mapea cada una de las rutas con el contador unico
        indice (Bool): valor booleano que hace visible los indices si es True. False por defecto
    """
    if contador is None:
        contador = [1]

    if mapeo_rutas is None:
        mapeo_rutas = {}

    if prefijo == "":
        print("📂 " + os.path.basename(ruta) + "/")

    elementos = os.listdir(ruta)
    elementos.sort()

    for i, elemento in enumerate(elementos, start=1):
        ruta_completa = os.path.join(ruta, elemento)

        idx = contador[0]
        contador[0] += 1
        idx_texto = f"  ({idx})" if indice else ""

        if i == len(elementos):
            conector = "└── "
            nuevo_prefijo = prefijo + "    "
        else:
            conector = "├── "
            nuevo_prefijo = prefijo + "│   "

        if os.path.isdir(ruta_completa):
            print(prefijo + conector + "📂 " + elemento + "/" + idx_texto)
            mapeo_rutas[idx] = ruta_completa
            if os.listdir(ruta_completa):
                listar_arbol(ruta_completa, nuevo_prefijo, contador, mapeo_rutas, indice)
        else:
            print(prefijo + conector + "📄 " + elemento + idx_texto)
            mapeo_rutas[idx] = ruta_completa

    return mapeo_rutas

def menu_principal(tipo):
    ancho = 27  # ancho total del menú
    borde = color_verde + "+" + "-" * (ancho - 2) + "+" + reset_color

    if tipo == 'fichero':
        titulo = color_verde + "FICHERO"
        print()
        print(borde)
        print(" " * 10 + titulo + " " * 10)  # centra el título
        print(borde)
        print(f"{color_verde}   1.{reset_color} Ver contenido")
        print(f"{color_verde}   2.{reset_color} Modificar contenido")
        print(f"{color_verde}   3.{reset_color} Mover fichero")
        print(f"{color_verde}   4.{reset_color} Eliminar fichero")
        print(f"{color_verde}   5.{reset_color} Salir")
        print(borde)

    elif tipo == 'carpeta':
        titulo = color_verde + "CARPETA"
        print()
        print(borde)
        print(" " * 10 + titulo + " " * 10)
        print(borde)
        print(f"{color_verde}   1.{reset_color} Crear fichero")
        print(f"{color_verde}   2.{reset_color} Crear carpeta")
        print(f"{color_verde}   3.{reset_color} Listar contenido")
        print(f"{color_verde}   4.{reset_color} Mover elemento")
        print(f"{color_verde}   5.{reset_color} Eliminar elemento")
        print(f"{color_verde}   6.{reset_color} Salir")
        print(borde)

while True:
    ruta_trabajo = obtener_ruta()
    if ruta_trabajo is None:
        print("Saliendo del programa...")
        break
    tipo_archivo = 'fichero' if os.path.isfile(ruta_trabajo) else 'carpeta'

    while True:
        menu_principal(tipo_archivo)
        opcion = input("\nSeleccione una opción: ").strip()
        match tipo_archivo:
            case 'fichero':
                match opcion:
                    case '1':
                        texto = leer_fichero(ruta_trabajo)
                        nombre_fichero = os.path.basename(ruta_trabajo)
                        mostrar_fichero(nombre_fichero, texto)

                    case '2':
                        pass

                    case '3':
                        ruta_origen = ruta_trabajo
                        ruta_destino = obtener_ruta()
                        if ruta_destino is not None:
                            nombre = os.path.basename(ruta_destino)
                            ruta_destino_final = os.path.join(ruta_destino, nombre)
                            mover_elemento(ruta_origen, ruta_destino_final)

                    case '4':
                        borrar_elemento(ruta_trabajo)
                        break

                    case '5':
                        break

                    case _:
                        print("Opcion no valida. Por favor, vuelva a intentar.")

            case 'carpeta':
                match opcion:
                    case '1':
                        nombre = ''
                        while not nombre:
                            nombre = input(f"Introduce el nombre para el fichero: ").strip()
                        crear_fichero_carpeta('fichero', ruta_trabajo, nombre)

                    case '2':
                        nombre = ''
                        while not nombre:
                            nombre = input(f"Introduce el nombre para la carpeta: ").strip()
                        crear_fichero_carpeta('carpeta', ruta_trabajo, nombre)

                    case '3':
                        print()
                        listar_arbol(ruta_trabajo)
                        print()
                    
                    case '4':
                        print()
                        rutas = listar_arbol(ruta_trabajo, indice=True)
                        print()
                        indices_validos = [str(i) for i in list(rutas.keys())]
                        while True:
                            elemento_mover = input("Introduce el numero del elemento que quieres mover (0 para cancelar): ").strip()
                            if elemento_mover == '0':
                                elemento_mover = None
                                break
                            if elemento_mover not in indices_validos:
                                print("Ese indice no existe. Vuelva a intentar")
                            else:
                                break
                        if elemento_mover is None:
                            print("Operacion cancelada.")

                        if elemento_mover is not None:
                            ruta_origen = rutas[int(elemento_mover)]
                            ruta_destino = obtener_ruta()
                            
                            if ruta_destino is not None:
                                nombre = os.path.basename(ruta_origen)
                                ruta_destino_final = os.path.join(ruta_destino, nombre)
                                mover_elemento(ruta_origen, ruta_destino_final)

                    case '5':
                        print()
                        rutas = listar_arbol(ruta_trabajo, indice=True)
                        print()
                        indices_validos = [str(i) for i in list(rutas.keys())]
                        while True:
                            elemento_borrar = input("Introduce el numero del elemento que quieres borrar (0 para cancelar): ").strip()
                            if elemento_borrar == '0':
                                elemento_borrar = None
                                break
                            if elemento_borrar not in indices_validos:
                                print("Ese indice no existe. Vuelva a intentar")
                            else:
                                break

                        if elemento_borrar is None:
                            print("Operacion cancelada.")

                        if elemento_borrar is not None:
                            borrar_elemento(rutas[int(elemento_borrar)])

                    case '6':
                        break

                    case _:
                        print("Opcion no valida. Por favor, vuelva a intentar.")