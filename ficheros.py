import os

color_verde = "\033[32m"
reset_color = "\033[0m"

def rutaValida(ruta):
    return os.path.exists(ruta)

def obtener_ruta():
    ruta_valida = False
    while not ruta_valida:
        ruta = input("Introduce la ruta (relativa/absoluta)con la que quieres trabajar (pulsa enter para salir): ").strip()
        if ruta == "":
            return None
        ruta_absoluta = os.path.abspath(ruta)
        ruta_valida = rutaValida(ruta_absoluta)
        if not ruta_valida:
            print("❌ La ruta no existe. Intente de nuevo.")
    return ruta_absoluta

def crear_fichero_carpeta(tipo, ruta, nombre):
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

def borrar_elemento(ruta):
    if os.path.isfile(ruta):
        os.remove(ruta)
        print(f"Fichero eliminado: {ruta}")

    elif os.path.isdir(ruta):
        for elemento in os.listdir(ruta):
            ruta_completa = os.path.join(ruta, elemento)
            borrar_elemento(ruta_completa)
        os.rmdir(ruta)
        print(f"Carpeta eliminada: {ruta}")

def listar_arbol(ruta, prefijo="", contador=None, mapeo_rutas=None, indice=False):
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

        # índice único global (cada elemento, en cualquier nivel, recibe uno)
        idx = contador[0]
        contador[0] += 1
        idx_texto = f"  ({idx})" if indice else ""

        # conector visual
        if i == len(elementos):
            conector = "└── "
            nuevo_prefijo = prefijo + "    "
        else:
            conector = "├── "
            nuevo_prefijo = prefijo + "│   "

        # imprimir
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
        titulo = "CARPETA"
        print(borde)
        print(" " * 10 + titulo + " " * 10)
        print(borde)
        print(f"{color_verde}   1.{reset_color} Crear fichero")
        print(f"{color_verde}   2.{reset_color} Crear carpeta")
        print(f"{color_verde}   3.{reset_color} Listar contenido")
        print(f"{color_verde}   4.{reset_color} Eliminar elemento")
        print(f"{color_verde}   5.{reset_color} Salir")
        print(borde)


while True:
    ruta_trabajo = obtener_ruta()
    if ruta_trabajo is None:
        break
    tipo_archivo = 'fichero' if os.path.isfile(ruta_trabajo) else 'carpeta'

    while True:
        menu_principal(tipo_archivo)
        opcion = input("\nSeleccione una opción: ").strip()
        match tipo_archivo:
            case 'fichero':
                match opcion:
                    case '1':
                        pass
                    case '2':
                        pass
                    case '3':
                        pass
                    case '4':
                        borrar_elemento(ruta_trabajo)
                        break
                    case '5':
                        print("Saliendo del programa...")
                        break

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
                            elemento_borrar = input("Introduce el numero del elemento que quieres borrar (0 para cancelar): ").strip()
                            if elemento_borrar == '0':
                                elemento_borrar = None
                                break
                            if elemento_borrar not in indices_validos:
                                print("Ese indice no existe. Vuelva a intentar")
                            else:
                                break
                        if elemento_borrar is not None:
                            borrar_elemento(rutas[int(elemento_borrar)])

                    case '5':
                        print("Saliendo del programa...")
                        break